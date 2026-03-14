# 폰으로 바로 접속: 같은 Wi-Fi + (선택) 인터넷 주소
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Docs = Join-Path $Root "docs"
$Port = 8080

if (-not (Test-Path (Join-Path $Docs "index.html"))) {
    Write-Host "docs\index.html 이 없습니다." -ForegroundColor Red
    exit 1
}

# 로컬 IP (Wi-Fi / 이더넷)
$ip = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object {
    $_.IPAddress -notlike "127.*" -and $_.PrefixOrigin -ne "WellKnown"
} | Select-Object -First 1).IPAddress
if (-not $ip) { $ip = "이_PC_IP" }

Write-Host ""
Write-Host "========== 폰으로 접속 ==========" -ForegroundColor Cyan
Write-Host ""
Write-Host " [같은 Wi-Fi 안에서]" -ForegroundColor Yellow
Write-Host "   폰 브라우저 주소창에 입력:" -ForegroundColor White
Write-Host ""
Write-Host "   http://${ip}:${Port}" -ForegroundColor Green
Write-Host ""
Write-Host " (PC 방화벽에서 Python 허용 안 되어 있으면 Windows 방화벽 알림에서 허용)" -ForegroundColor Gray
Write-Host ""

$http = "cd '$Docs'; python -m http.server $Port --bind 0.0.0.0"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $http -WindowStyle Normal

Start-Sleep -Seconds 2

$ext = Read-Host "데이터(LTE)로도 열까요? (y=Cloudflare 주소, n=Wi-Fi만) [n]"
if ($ext -eq "y" -or $ext -eq "Y") {
    $BinDir = Join-Path $Root "bin"
    $CfExe = Join-Path $BinDir "cloudflared.exe"
    if (-not (Test-Path $BinDir)) { New-Item -ItemType Directory -Path $BinDir | Out-Null }
    if (-not (Test-Path $CfExe)) {
        Write-Host "cloudflared 다운로드 중..." -ForegroundColor Cyan
        Invoke-WebRequest -Uri "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-windows-amd64.exe" -OutFile $CfExe -UseBasicParsing
    }
    Write-Host ""
    Write-Host " 아래에 https://....trycloudflare.com 가 나오면 그 주소를 폰에 입력 (가입 없음)" -ForegroundColor Yellow
    Write-Host ""
    & $CfExe tunnel --url "http://127.0.0.1:$Port"
} else {
    Write-Host "Wi-Fi 전용. 창 닫으면 접속 종료." -ForegroundColor Gray
}
