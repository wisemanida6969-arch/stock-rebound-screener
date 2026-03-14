# Vercel 배포 (Yahoo 안정 프록시)

## 구성

| 경로 | 역할 |
|------|------|
| `api/chart.js` | 서버에서 Yahoo 차트 API 호출 → JSON 그대로 반환 (CORS `*`) |
| `index.html` | 모바일 앱 (먼저 `/api/chart` 호출, 실패 시 무료 프록시) |
| `manifest.json` / `sw.js` | PWA (선택) |

## 배포 순서

1. **GitHub**에 이 저장소 전체 푸시 (루트에 `api/` + `index.html` 있어야 함).
2. **[vercel.com](https://vercel.com)** 로그인 → **Add New… → Project**.
3. 저장소 선택 → **Import**.
4. **Framework Preset:** Other (또는 비워 둠). **Root Directory:** 비워 둠 (저장소 루트).
5. **Deploy**.

완료 후 주소 예: `https://stock-xxx.vercel.app`

- 브라우저에서 `https://주소/api/chart?ticker=AAPL&range=1d&interval=1m` 열어보면 JSON 나오면 성공.
- 폰에는 **`https://주소/`** 만 즐겨찾기하면 됩니다.

## 다른 정적 호스트만 쓰는 경우

GitHub Pages 등 **API 없는 주소**에서 쓰려면, 브라우저 콘솔에서 한 번:

```js
localStorage.setItem('API_ORIGIN', 'https://당신-vercel주소.vercel.app')
```

새로고침 후에는 그 API로만 Yahoo 데이터를 받습니다. (CORS 이미 허용됨)

## 무료 한도

Vercel 무료 플랜으로 개인용·가벼운 스크리닝에는 보통 충분합니다. 호출이 매우 많으면 한도 안내가 뜰 수 있습니다.
