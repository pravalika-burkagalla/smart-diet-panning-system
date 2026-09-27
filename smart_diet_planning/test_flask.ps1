$ProgressPreference = 'SilentlyContinue'
try {
    $response = Invoke-WebRequest -Uri "http://127.0.0.1:5000/" -TimeoutSec 3 -UseBasicParsing
    Write-Host "[OK] HTTP 200 received"
    if ($response.Content -match "Enter Your Details") {
        Write-Host "[OK] Form found in index.html"
    }
} catch {
    Write-Host "[ERROR] Failed to connect: $_"
}
