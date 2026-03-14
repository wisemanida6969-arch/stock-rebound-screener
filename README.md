# 미국 주식 저평가 · 반등 후보 스크리너

Streamlit 기반 웹앱입니다. Yahoo Finance(`yfinance`)로 재무 지표와 가격 차트를 가져와 **저평가(낮은 밸류에이션, 52주 고점 대비 하락)** 와 **기술적 반등 여지(RSI, MACD)** 를 점수화해 순위를 보여줍니다.

## 설치

```bash
cd stock-rebound-screener
pip install -r requirements.txt
```

## 실행 (PC만)

```bash
streamlit run app.py
```

기본 `http://localhost:8501` — **폰에서는 안 열림**.

## 폰으로 바로 접속 (가장 쉬움)

1. **`폰으로열기.bat`** 더블클릭  
2. 뜬 창에 나오는 **`http://192.168.x.x:8080`** 을 **폰 브라우저**에 그대로 입력  
   - PC와 폰이 **같은 Wi-Fi** 여야 함  
3. 방화벽 창 뜨면 **Python 허용**  
4. **LTE로도** 열고 싶으면 물어볼 때 **`y`** → 나오는 **`https://….trycloudflare.com`** 을 폰에 입력  

→ 열리는 화면은 **서버 없이 쓰는 모바일용 페이지**(`docs/index.html`, 실시간 차트).

## 등록 없이 폰에서 바로 열기 (Streamlit까지)

**가입 없음** — GitHub / Streamlit / ngrok 계정 필요 없음.

1. `pip install -r requirements.txt` (최초 1회)  
2. **`start_public.bat`** 더블클릭 (Windows)  
3. 검은 창에 나오는 **`https://….trycloudflare.com`** 를 폰 브라우저에 입력  

PC와 터널 창을 켜 둔 동안만 접속됩니다. 자세한 설명은 **`DEPLOY_MOBILE.md`**.

### PC와 연결 없이 · 모바일만으로 (단독 가동)

집 PC를 켤 필요 **없음**. **한 번만** 웹에 올려 **고정 주소**를 받으면, 이후에는 **폰만**으로 계속 사용.

| 방법 | 설명 |
|------|------|
| **Netlify Drop** | [app.netlify.com/drop](https://app.netlify.com/drop) 에 `docs` 안 파일 ZIP 업로드 → `*.netlify.app` 주소를 폰에 저장 |
| **GitHub Pages** | 저장소 Pages에서 `/docs` → `github.io` 주소 |

자세한 단계 → **`모바일단독-가이드.md`**

### 모바일에서 안정적으로 (Vercel API)

프록시 실패를 줄이려면 **Vercel**에 올리면 서버가 Yahoo 대신 받아줍니다.  
→ **`VERCEL-배포.md`** · 루트에 `api/chart.js` + `index.html` 로 배포.

## 사용법 (폰 동일)

1. **스크리닝 실행** (큰 버튼) — 사이드바 안 열어도 됨.  
2. 표는 좌우로 스크롤 가능. **차트 종목 선택**에서 티커 고르기.  
3. **다시 분석**으로 최신 데이터. **추가 티커**는 펼치기 메뉴에서.

## 한계

- 무료 API라 요청이 많으면 지연이나 실패가 날 수 있습니다.
- 샘플 티커 리스트 기반이라 전 시장 스크리너는 아닙니다.
- 투자 결정은 본인 책임이며, 앱은 참고용입니다.
