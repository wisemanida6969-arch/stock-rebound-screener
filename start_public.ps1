# 등록 없이 공개 URL로 열기 (Cloudflare Quick Tunnel — 계정 불필요)
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

$Port = 8501
$BinDir = Join-Path $Root "bin"
$CfExe  = Join-Path $BinDir "cloudflared.exe"

if (-not (Test-Path $BinDir)) { New-Item -ItemType Directory -Path $BinDir | Out-Null }

if (-not (Test-Path $CfExe)) {
    Write-Host "[1/3] cloudflared 다운로드 (최초 1회, 가입 없음)..." -ForegroundColor Cyan
    $url = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe"
    try {
        Invoke-WebRequest -Uri $url -OutFile $CfExe -UseBasicParsing
    } catch {
        Write-Host "다운로드 실패. 브라우저에서 받아 bin\cloudflared.exe 로 저장하세요:" -ForegroundColor Red
        Write-Host $url
        exit 1
    }
}

Write-Host "[2/3] Streamlit 시작 (포트 $Port)..." -ForegroundColor Cyan
$streamlitCmd = "Set-Location '$Root'; streamlit run app.py --server.port $Port --server.headless true"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $streamlitCmd -WindowStyle Normal
Start-Sleep -Seconds 6

Write-Host "[3/3] 공개 터널 연결 중..." -ForegroundColor Cyan
Write-Host ""
Write-Host ">>> 아래에 https://....trycloudflare.com 주소가 나오면 그걸 폰 브라우저에 입력 <<<" -ForegroundColor Yellow
Write-Host ">>> 이 창을 닫으면 주소가 끊깁니다. Streamlit 창도 함께 닫으면 됩니다. <<<" -ForegroundColor Gray
Write-Host ""

& $CfExe tunnel --url "http://127.0.0.1:$Port"
