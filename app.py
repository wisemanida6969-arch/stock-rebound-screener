# -*- coding: utf-8 -*-
"""
미국 주식 저평가 + 반등 후보 스크리너
- 재무: P/E, P/B, 52주 고점 대비 하락률
- 기술: RSI, MACD 히스토그램 전환
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

# 유동성 있는 대형·중형주 샘플 (전체 스크리닝은 API 한계로 샘플 유니버스)
DEFAULT_TICKERS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM", "V",
    "UNH", "JNJ", "WMT", "PG", "MA", "HD", "DIS", "BAC", "XOM", "CVX",
    "ABBV", "PFE", "KO", "COST", "MRK", "PEP", "TMO", "CSCO", "ACN", "ADBE",
    "NFLX", "CRM", "AMD", "INTC", "QCOM", "IBM", "ORCL", "TXN", "AMAT", "MU",
    "GE", "CAT", "DE", "BA", "LMT", "NOC", "UPS", "FDX", "SBUX", "MCD",
    "NKE", "LOW", "TGT", "C", "WFC", "GS", "MS", "BLK", "SCHW", "AXP",
    "PM", "MO", "BMY", "GILD", "AMGN", "CVS", "CI", "HUM", "ELV", "DHR",
    "NEE", "SO", "DUK", "AEP", "SRE", "OXY", "SLB", "HAL", "FCX", "NEM",
    "F", "GM", "STLA", "RIVN", "LCID", "PYPL", "SQ", "SHOP", "ETSY", "ROKU",
    "DAL", "UAL", "AAL", "LUV", "MAR", "HLT", "BKNG", "ABNB", "EXPE", "NCLH",
]


def _one_info(t: str) -> dict:
    try:
        info = yf.Ticker(t).info
        return {
            "ticker": t,
            "name": info.get("shortName") or info.get("longName") or t,
            "sector": info.get("sector") or "-",
            "trailing_pe": info.get("trailingPE"),
            "forward_pe": info.get("forwardPE"),
            "pb": info.get("priceToBook"),
            "market_cap": info.get("marketCap"),
            "fifty_two_week_high": info.get("fiftyTwoWeekHigh"),
            "fifty_two_week_low": info.get("fiftyTwoWeekLow"),
            "current_price": info.get("currentPrice") or info.get("regularMarketPrice"),
            "revenue_growth": info.get("revenueGrowth"),
            "debt_to_equity": info.get("debtToEquity"),
        }
    except Exception:
        return {"ticker": t, "name": t}


@st.cache_data(ttl=1800)
def fetch_batch_info(tickers: tuple) -> pd.DataFrame:
    """병렬 info — 티커 많을 때 순차 대비 훨씬 빠름"""
    tickers = list(tickers)
    rows = []
    with ThreadPoolExecutor(max_workers=min(16, max(4, len(tickers)))) as ex:
        futs = {ex.submit(_one_info, t): t for t in tickers}
        for fut in as_completed(futs):
            rows.append(fut.result())
    order = {t: i for i, t in enumerate(tickers)}
    rows.sort(key=lambda r: order.get(r["ticker"], 999))
    return pd.DataFrame(rows)


@st.cache_data(ttl=900)
def fetch_ohlc_batch(tickers: tuple, months: int = 6) -> dict:
    """한 번에 여러 종목 일봉 — 네트워크 왕복 대폭 감소"""
    tickers = list(tickers)
    if not tickers:
        return {}
    end = datetime.now()
    start = end - timedelta(days=months * 31)
    s = " ".join(tickers)
    try:
        df = yf.download(s, start=start, end=end, progress=False, auto_adjust=True, threads=True, group_by="ticker")
    except Exception:
        return {}
    out = {}
    if isinstance(df.columns, pd.MultiIndex):
        lev0 = df.columns.get_level_values(0).unique()
        for t in tickers:
            try:
                if t not in lev0:
                    continue
                sub = df[t]
                if hasattr(sub, "columns") and len(sub) >= 10:
                    sub = sub.copy()
                    if isinstance(sub.columns, pd.MultiIndex):
                        sub.columns = [c[0] if isinstance(c, tuple) else c for c in sub.columns]
                    out[t] = sub
            except Exception:
                pass
    elif len(tickers) == 1 and len(df) >= 10:
        out[tickers[0]] = df
    missing = [t for t in tickers if t not in out]
    for t in missing:
        try:
            d = yf.download(t, start=start, end=end, progress=False, auto_adjust=True)
            if isinstance(d.columns, pd.MultiIndex):
                d.columns = [c[0] for c in d.columns]
            if len(d) >= 10:
                out[t] = d
        except Exception:
            pass
    return out


def rsi(series: pd.Series, period: int = 14) -> pd.Series:
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


def macd_hist(close: pd.Series):
    ema12 = close.ewm(span=12).mean()
    ema26 = close.ewm(span=26).mean()
    line = ema12 - ema26
    signal = line.ewm(span=9).mean()
    hist = line - signal
    return hist


@st.cache_data(ttl=1800)
def fetch_ohlc(ticker: str, months: int = 12) -> pd.DataFrame:
    end = datetime.now()
    start = end - timedelta(days=months * 31)
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df


def fetch_ohlc_intraday(ticker: str, interval: str = "5m") -> pd.DataFrame:
    """실시간에 가깝게: 최근 5거래일 분봉 (캐시 없음 → 매번 최신)"""
    df = yf.download(ticker, period="5d", interval=interval, progress=False, auto_adjust=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [c[0] for c in df.columns]
    return df


def compute_technical_score(df: pd.DataFrame) -> dict:
    if df is None or len(df) < 30:
        return {"rsi": None, "rsi_score": 0, "macd_turn": 0, "drawdown_score": 0}
    close = df["Close"].astype(float)
    r = rsi(close).iloc[-1]
    hist = macd_hist(close)
    # MACD 히스토그램: 최근 5일 중 음→양 전환 경향
    recent = hist.tail(8).dropna()
    macd_turn = 0
    if len(recent) >= 3:
        if recent.iloc[-1] > recent.iloc[-3]:
            macd_turn = min(25, (recent.iloc[-1] - recent.iloc[-3]) * 500)
        if recent.iloc[-1] > 0 and recent.iloc[-5] < 0:
            macd_turn += 15
    # RSI: 20~40 구간 = 과매도 쪽이면 반등 여지 가점 (극단 20 미만은 위험도 있어 중간 가점)
    rsi_score = 0
    if pd.notna(r):
        if 22 <= r <= 38:
            rsi_score = 30
        elif 38 < r <= 45:
            rsi_score = 18
        elif r < 22:
            rsi_score = 20
        elif 45 < r <= 55:
            rsi_score = 8
    return {"rsi": float(r) if pd.notna(r) else None, "rsi_score": rsi_score, "macd_turn": min(25, macd_turn), "drawdown_score": 0}


def fundamental_value_score(row: pd.Series) -> float:
    score = 0
    pe = row.get("forward_pe") or row.get("trailing_pe")
    if pe is not None and pe > 0 and pe < 15:
        score += 20
    elif pe is not None and pe > 0 and pe < 22:
        score += 12
    elif pe is not None and pe > 0 and pe < 30:
        score += 5
    pb = row.get("pb")
    if pb is not None and pb > 0 and pb < 1.5:
        score += 15
    elif pb is not None and pb > 0 and pb < 3:
        score += 8
    # 52주 고점 대비 하락 = 저평가·반등 후보
    high = row.get("fifty_two_week_high")
    price = row.get("current_price")
    if high and price and high > 0:
        dd = (high - price) / high * 100
        if dd > 25:
            score += 25
        elif dd > 15:
            score += 18
        elif dd > 8:
            score += 10
    return score


@st.fragment(run_every=90)
def render_live_chart(ticker: str, interval_label: str):
    """분봉 + 45초마다 자동 갱신 (장중·야간 프리/마켓 반영 지연 가능)"""
    df = fetch_ohlc_intraday(ticker, interval="5m")
    if df is None or len(df) < 20:
        df = fetch_ohlc_intraday(ticker, interval="15m")
    if df is None or len(df) == 0:
        st.warning(f"{ticker} 분봉을 불러오지 못했습니다. 일봉으로 대체합니다.")
        df = fetch_ohlc(ticker, months=3)
    if df is None or len(df) == 0:
        st.error("차트 데이터 없음")
        return
    close = df["Close"].astype(float)
    r = rsi(close)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[0.65, 0.35])
    fig.add_trace(
        go.Candlestick(
            x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"], name=ticker
        ),
        row=1,
        col=1,
    )
    fig.add_trace(go.Scatter(x=df.index, y=r, name="RSI(14)", line=dict(color="orange")), row=2, col=1)
    fig.add_hline(y=30, row=2, col=1, line_dash="dash", line_color="gray")
    fig.add_hline(y=70, row=2, col=1, line_dash="dash", line_color="gray")
    fig.update_layout(
        height=480,
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
        margin=dict(l=8, r=8, t=8, b=8),
        title=dict(text=f"{ticker} · {interval_label} · 갱신 {datetime.now().strftime('%H:%M:%S')}", font=dict(size=14)),
    )
    fig.update_yaxes(title_text="가격", row=1, col=1)
    fig.update_yaxes(title_text="RSI", row=2, col=1)
    st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": True, "displayModeBar": True})
    st.caption("5분봉 · 약 90초마다 갱신 (부하 줄임)")


def main():
    st.set_page_config(
        page_title="저평가·반등 스크리너",
        layout="wide",
        initial_sidebar_state="collapsed",
    )
    # 모바일: 뷰포트 + 터치 영역 + 표 스크롤
    st.markdown(
        """
        <meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=5, viewport-fit=cover">
        <style>
          /* 터치 버튼 크기 */
          div.stButton > button { min-height: 48px !important; font-size: 1.05rem !important; }
          /* 폰에서 표 가로 스크롤 */
          div[data-testid="stDataFrame"] { overflow-x: auto !important; -webkit-overflow-scrolling: touch; }
          @media (max-width: 600px) {
            h1 { font-size: 1.35rem !important; }
            .block-container { padding-top: 1rem !important; padding-left: 0.75rem !important; padding-right: 0.75rem !important; }
          }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.title("미국 주식 스크리너")
    st.caption("폰에서 그대로 사용 · 스크리닝 시 Yahoo 기준 · 참고용")

    # 모바일 우선: 메인 화면에만 설정 (사이드바 불필요)
    max_n = st.slider("분석 종목 수 (많을수록 느림)", 12, min(50, len(DEFAULT_TICKERS)), 20)
    with st.expander("추가 티커 (선택)", expanded=False):
        custom_in = st.text_input("쉼표 구분", placeholder="COIN, MRNA")
    run = st.button("스크리닝 실행", type="primary", use_container_width=True)
    rerun = st.button("다시 분석", use_container_width=True)

    tickers = DEFAULT_TICKERS[:max_n]
    if custom_in:
        extra = [x.strip().upper() for x in custom_in.replace("\n", ",").split(",") if x.strip()]
        tickers = list(dict.fromkeys(tickers + extra))[: max_n + len(extra) + 20]

    do_run = run or rerun
    if not do_run and "results" not in st.session_state:
        st.info(
            "**폰:** 위 **스크리닝 실행** 탭 한 번이면 됩니다. "
            "**외부에서 폰으로 열기:** PC에서 `start_public.bat` → 나온 `trycloudflare.com` 주소를 폰 브라우저에 입력."
        )
        return

    if do_run:
        with st.spinner("일괄 수집 중 (배치 다운로드)…"):
            base = fetch_batch_info(tuple(tickers))
            ohlc_map = fetch_ohlc_batch(tuple(tickers), months=6)
        results = []
        for _, row in base.iterrows():
            t = row["ticker"]
            try:
                ohlc = ohlc_map.get(t)
                if ohlc is None or len(ohlc) < 20:
                    ohlc = fetch_ohlc(t, months=6)
                tech = compute_technical_score(ohlc)
                fscore = fundamental_value_score(row)
                high = row.get("fifty_two_week_high")
                price = row.get("current_price")
                dd_pct = None
                if high and price and high > 0:
                    dd_pct = (high - price) / high * 100
                total = fscore + tech["rsi_score"] + min(25, tech["macd_turn"])
                results.append({
                    "티커": t,
                    "종목명": row.get("name", t),
                    "섹터": row.get("sector", "-"),
                    "재무점수": round(fscore, 1),
                    "RSI": round(tech["rsi"], 1) if tech["rsi"] else None,
                    "기술점수": round(tech["rsi_score"] + min(25, tech["macd_turn"]), 1),
                    "총점": round(total, 1),
                    "52주고점대비하락%": round(dd_pct, 1) if dd_pct is not None else None,
                    "PER(예상)": row.get("forward_pe"),
                    "PBR": row.get("pb"),
                })
            except Exception:
                results.append({"티커": t, "총점": 0})
        st.session_state["results"] = pd.DataFrame(results)
        st.session_state["base_df"] = base

    if "results" not in st.session_state:
        return
    out = st.session_state["results"].sort_values("총점", ascending=False)
    display_df = out.head(25).reset_index(drop=True)
    houbu = [""] * len(display_df)
    for i in range(min(5, len(display_df))):
        houbu[i] = f"★ 후보 {i + 1}"
    display_df = display_df.copy()
    display_df.insert(0, "후보", houbu)

    st.subheader("추천 순위 (후보1~5 = 당일 점수 상위 · 참고용)")
    top20 = out.head(20)["티커"].tolist()
    allowed = st.multiselect(
        "**실시간 차트에 넣을 종목 (체크)** — 체크한 것만 아래 차트로 볼 수 있습니다.",
        options=top20,
        default=st.session_state.get("chart_allowed", []),
        key="chart_allowed_ms",
    )
    st.session_state["chart_allowed"] = list(allowed)
    st.caption("표에서 **행 선택** → 체크 목록 안의 종목만 차트 표시")
    event = st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True,
        height=min(420, 56 * 12),
        on_select="rerun",
        selection_mode="single-row",
        key="rank_pick_df",
    )

    rows = event.selection.rows if event is not None and hasattr(event, "selection") else []
    if len(rows) > 0:
        cand = str(display_df.iloc[int(rows[0])]["티커"])
        if allowed and cand not in allowed:
            st.warning(f"**{cand}** 은(는) 위에서 체크하지 않았습니다. multiselect에 추가하거나 다른 행을 선택하세요.")
        st.session_state["chart_ticker"] = cand if (not allowed or cand in allowed) else (allowed[0] if allowed else cand)
    pick = st.session_state.get("chart_ticker") or (allowed[0] if allowed else str(display_df.iloc[0]["티커"]))
    if allowed and pick not in allowed:
        pick = allowed[0]
    if "chart_ticker" not in st.session_state or (allowed and st.session_state["chart_ticker"] not in allowed):
        st.session_state["chart_ticker"] = pick

    st.divider()
    if not allowed:
        st.subheader("실시간 차트")
        st.info("위 **multiselect** 에서 차트로 볼 종목을 **한 개 이상 체크**하세요.")
    else:
        pick = st.selectbox("차트 종목 (체크한 목록)", options=allowed, index=allowed.index(pick) if pick in allowed else 0, key="chart_pick_sb")
        st.session_state["chart_ticker"] = pick
        st.subheader(f"실시간 차트 · {pick}")
        render_live_chart(pick, "5분봉")

    st.caption("체크 목록만 차트 가능 · multiselect에서 종목 추가/제거")

    st.markdown("""
    **점수 의미 (참고)**  
    - **재무**: 낮은 PER/PBR, 52주 고점 대비 큰 조정 → 상대적 저평가·회복 여지 가정  
    - **기술**: RSI 과매도 구간 근처, MACD 히스토그램 개선 → 단기 반등 시그널 가능성  
    **면책**: 본 앱은 교육·분석용이며 특정 종목 매수·매도를 권하지 않습니다.
    """)


if __name__ == "__main__":
    main()
