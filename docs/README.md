# 모바일에서 항상 보기 (PC 서버 불필요)

이 폴더(`docs`)의 **`index.html`** 은 **순수 정적 페이지**입니다.  
GitHub Pages 등에 한 번만 올려 두면 **집 PC를 꺼도** 폰 브라우저에서 같은 주소로 계속 열 수 있습니다.

## 1) GitHub에 올리기 (무료, 고정 주소)

1. GitHub에서 새 저장소 생성 (예: `stock-rebound-screener`).
2. 이 프로젝트 전체를 푸시한 뒤, 저장소 **Settings → Pages**:
   - **Source:** Deploy from a branch  
   - **Branch:** `main` (또는 `master`)  
   - **Folder:** `/docs`  
3. 저장 후 1~2분 뒤 주소:  
   **`https://본인아이디.github.io/stock-rebound-screener/`**

폰에서 이 URL을 즐겨찾기하면 **서버 켤 필요 없음**.

## 2) 동작 방식

- 페이지가 **사용자 폰/PC 브라우저**에서 Yahoo 차트 API를 (CORS 우회 프록시 경유) 호출합니다.
- **스크리닝 실행**을 누를 때마다 그때 기준 데이터로 표·차트가 갱신됩니다.
- 프록시(allorigins / corsproxy)가 막히면 일시적으로 실패할 수 있습니다. 잠시 뒤 다시 시도하세요.

## 3) Streamlit과 차이

| | Streamlit (집 PC) | 이 정적 페이지 (Pages) |
|--|-------------------|-------------------------|
| PC 꺼도 접속 | ❌ | ✅ |
| 고정 URL | 로컬만 / 터널 | ✅ github.io |

투자 권유 아님 · 참고용입니다.
