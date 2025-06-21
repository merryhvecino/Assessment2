Write-Host "Starting Kaiwhakarite Rawa Backend Server..." -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    python --version | Out-Null
    Write-Host "✓ Python is available" -ForegroundColor Green
} catch {
    Write-Host "✗ Python not found. Please install Python first." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Starting Backend Server (FastAPI)..." -ForegroundColor Yellow

# Start backend server
$backendJob = Start-Job -ScriptBlock {
    Set-Location $args[0]
    Set-Location ..
    python scripts/run_server.py
} -ArgumentList (Get-Location)

Write-Host "Backend server started in background job" -ForegroundColor Green

# Wait for backend to start
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Backend server is starting..." -ForegroundColor Cyan
Write-Host "Backend API: http://localhost:8000" -ForegroundColor White
Write-Host ""
Write-Host "Please wait a few seconds for the server to start." -ForegroundColor Yellow
Write-Host "Then you can access the API at http://localhost:8000" -ForegroundColor Yellow
Write-Host ""

# Wait and check backend server
Write-Host "Waiting for backend server to start..." -ForegroundColor Cyan
Start-Sleep -Seconds 10

# Check backend
try {
    $backendResponse = Invoke-WebRequest -Uri "http://localhost:8000/health" -UseBasicParsing -TimeoutSec 5
    Write-Host "✓ Backend server is running (Status: $($backendResponse.StatusCode))" -ForegroundColor Green
} catch {
    Write-Host "⚠ Backend server not responding yet" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "API Documentation: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "Health Check: http://localhost:8000/health" -ForegroundColor Cyan
Write-Host ""
Write-Host "To stop the server, press Ctrl+C and run:" -ForegroundColor Cyan
Write-Host "Get-Job | Stop-Job; Get-Job | Remove-Job" -ForegroundColor White
Write-Host ""
Write-Host "Jobs running:" -ForegroundColor Cyan
Get-Job | Format-Table -AutoSize

Write-Host "Press Enter to exit (server will continue running)..."
Read-Host 