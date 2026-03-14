#!/usr/bin/env bash
# 등록 없이 공개 URL (Mac/Linux) — cloudflared Quick Tunnel
set -e
cd "$(dirname "$0")"
PORT=8501
BIN="$(pwd)/bin"
CF="$BIN/cloudflared"
mkdir -p "$BIN"
if [[ ! -x "$CF" ]]; then
  echo "[1/3] cloudflared 다운로드..."
  OS=$(uname -s | tr '[:upper:]' '[:lower:]')
  ARCH=$(uname -m)
  if [[ "$OS" == "darwin" ]]; then
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-darwin-amd64.tgz"
    curl -sL "$URL" | tar xz -C "$BIN" 2>/dev/null || { echo "수동: $URL"; exit 1; }
    mv "$BIN/cloudflared" "$CF" 2>/dev/null || true
  else
    URL="https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
    curl -sL "$URL" -o "$CF" && chmod +x "$CF"
  fi
fi
echo "[2/3] Streamlit 시작..."
streamlit run app.py --server.port "$PORT" --server.headless true &
sleep 6
echo "[3/3] 공개 URL (trycloudflare.com) — 폰에서 이 주소로 접속"
exec "$CF" tunnel --url "http://127.0.0.1:$PORT"
