# 모바일에서 바로 열기

로컬 `localhost`는 폰에서 안 열립니다. **공개 HTTPS 주소**가 필요합니다.

---

## ⭐ 등록 없이 바로 쓰기 (호스트 가입 불필요)

**GitHub / Streamlit / ngrok 가입 없이** PC만으로 공개 URL을 쓸 수 있습니다.  
Cloudflare **Quick Tunnel**은 계정 없이 `https://xxxx.trycloudflare.com` 주소를 잠깐 열어 줍니다.

### Windows

1. 한 번만: `pip install -r requirements.txt`
2. **`start_public.bat`** 더블클릭  
   - 처음에 `cloudflared.exe`를 이 폴더 `bin\` 에 자동 다운로드합니다 (가입 없음).
   - Streamlit 창 + 터널 창이 뜹니다.
3. 터널 창에 나오는 **`https://….trycloudflare.com`** 를 **폰 브라우저**에 입력.

### Mac / Linux

```bash
chmod +x start_public.sh
./start_public.sh
```

같은 방식으로 터미널에 나온 **trycloudflare.com** 주소를 폰에서 엽니다.

### 특징

| 항목 | 설명 |
|------|------|
| 가입 | **없음** |
| 고정 주소 | 아님 — 실행할 때마다 URL이 바뀔 수 있음 |
| 유지 | **PC 켜 두고** 배치 파일/터널 창 유지 중에만 접속 가능 |
| 실시간 | 폰에서 버튼 누를 때마다 **이 PC**가 Yahoo 데이터 처리 |

---

## (선택) Node만 있을 때 — localtunnel

가입 없이: `npx localtunnel --port 8501`  
(PC에서 먼저 `streamlit run app.py --server.port 8501` 실행 후 다른 터미널에서.)

---

## 고정 주소가 필요할 때 (가입 필요)

| 방식 | 가입 | 주소 |
|------|------|------|
| Streamlit Cloud | GitHub | `xxx.streamlit.app` |
| ngrok | ngrok | `xxx.ngrok-free.app` |

---

**실시간 연동**: Quick Tunnel로 열린 주소로 접속하면, 스크리닝 실행 시점의 데이터가 그대로 반영됩니다.
