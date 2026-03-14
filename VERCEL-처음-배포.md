# Vercel에 배포가 하나도 없을 때 (No deployments)

**Deployments가 비어 있으면** 아직 이 저장소로 **한 번도 배포가 안 된 것**입니다.  
아래 순서대로 **새 프로젝트로 Import** 하면 첫 배포가 생깁니다.

---

## 1. 필터 먼저 제거

Deployments 화면에서 **Clear Filters** 눌러 보세요.  
그래도 비어 있으면 → **2번**으로.

---

## 2. 새 프로젝트로 GitHub 연결 (필수)

1. **[vercel.com](https://vercel.com)** 로그인  
2. 오른쪽 위 **Add New…** → **Project**  
3. **Import Git Repository** 에서  
   **`wisemanida6969-arch/stock-rebound-screener`** 검색 → **Import**  
   (안 보이면 **Adjust GitHub App Permissions** 에서 저장소 접근 허용)

4. **Configure Project** 화면에서 **이렇게만** 맞추기:

| 설정 | 값 |
|------|-----|
| Framework Preset | **Other** |
| Root Directory | **./** (비우거나 점만 — **docs 아님**) |
| Build Command | **비움** |
| Output Directory | **비움** |
| Install Command | **비움** |

5. **Deploy** 클릭  

2~3분 뒤 **Congratulations** 나오면 성공.  
그때부터 **Deployments** 에 기록이 쌓입니다.

---

## 3. 폰 주소

배포 끝나면 나오는 주소 예:

`https://stock-rebound-screener-XXXX.vercel.app`

- 메인: 그 주소  
- 테스트: `.../hello.html` (초록 글 «배포 OK»)  
- API: `.../api/chart?ticker=AAPL&range=1d&interval=1m`  

---

## 4. 자주 하는 실수

- **다른 Vercel 팀/계정**에 들어가 있음 → 왼쪽 상단 팀 확인  
- **Root Directory를 `docs`로 둠** → 메인이 비어 보일 수 있음 → **루트 비움**  
- 저장소를 **Import 안 함** → Deployments 영원히 없음  

---

저장소 주소: **https://github.com/wisemanida6969-arch/stock-rebound-screener**
