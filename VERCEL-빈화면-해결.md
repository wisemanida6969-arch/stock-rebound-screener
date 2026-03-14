# Vercel 도메인에 아무것도 안 나올 때

## 1. Root Directory (가장 흔한 원인)

Vercel 프로젝트 → **Settings → General → Root Directory**

- **`docs` / `iphone` / 빈 폴더** 로 되어 있으면 **루트 `index.html`이 배포에 안 들어감** → 주소 열면 비어 있거나 404.
- **비우기** 또는 **`.`** 만 두세요. (저장소 **맨 위**가 배포 루트여야 함)

## 2. Build 설정

**Settings → General**

| 항목 | 값 |
|------|-----|
| Framework Preset | **Other** |
| Build Command | **비움** |
| Output Directory | **비움** |
| Install Command | **비움** (또는 `echo skip`) |

`npm run build` 같은 게 들어가 있으면 실패해서 배포가 깨질 수 있습니다.

## 3. 다시 배포

**Deployments → 맨 위 배포 ⋮ → Redeploy** (또는 Git에 아무 커밋 푸시)

## 4. 확인용 주소

배포 후 브라우저에서:

1. **`https://당신도메인.vercel.app/index.html`**  
   → 글자라도 보이면 정적 파일은 올라간 것.
2. **`https://당신도메인.vercel.app/api/chart?ticker=AAPL&range=1d&interval=1m`**  
   → JSON 나오면 API 정상.

둘 다 404면 **연결된 Git 저장소 / 브랜치 / Root Directory** 다시 확인.

## 5. 이 저장소에 꼭 있어야 하는 것 (루트 기준)

- `index.html`
- `api/chart.js`
- `iphone/index.html` (아이폰용은 `/iphone/`)

Root Directory를 `docs`만 쓰고 싶다면, 그 안에 `index.html`만 있고 **`api/`는 못 쓰므로** 차트 API는 따로 프로젝트를 쓰거나 루트 배포를 권장합니다.
