# Kaiwhakarite HTTPS Server Launcher for iOS Safari Camera Support
# This script starts both backend and frontend with HTTPS to enable camera access on iOS Safari

Write-Host "🚀 Starting Kaiwhakarite with HTTPS for iOS Safari Camera Support..." -ForegroundColor Green
Write-Host "📱 This will enable camera access on iOS Safari devices!" -ForegroundColor Yellow
Write-Host ""

# Kill any existing processes on ports 8000 and 3000
Write-Host "🔄 Cleaning up existing processes..." -ForegroundColor Blue
Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Start backend server
Write-Host "🔧 Starting Backend API Server (Port 8000)..." -ForegroundColor Blue
$backendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\mdvec\anaconda3\envs\mse800\ASSESSMENT2\v2_KAIWHAKARITE"
    python scripts/run_server.py
}

# Wait a moment for backend to start
Start-Sleep -Seconds 3

# Start frontend with HTTPS
Write-Host "🌐 Starting Frontend with HTTPS (Port 3000)..." -ForegroundColor Blue
$frontendJob = Start-Job -ScriptBlock {
    Set-Location "C:\Users\mdvec\anaconda3\envs\mse800\ASSESSMENT2\v2_KAIWHAKARITE\client"
    $env:HTTPS = "true"
    $env:HOST = "0.0.0.0"
    $env:PORT = "3000"
    npm start
}

# Wait for servers to start
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "✅ Servers are starting up!" -ForegroundColor Green
Write-Host ""
Write-Host "📱 iOS Safari Camera Access:" -ForegroundColor Yellow
Write-Host "   🔗 Access via: https://192.168.1.4:3000" -ForegroundColor White
Write-Host "   ⚠️  You'll see a security warning - click 'Advanced' then 'Proceed'" -ForegroundColor Red
Write-Host "   📷 Camera should now work on iOS Safari!" -ForegroundColor Green
Write-Host ""
Write-Host "🖥️  Desktop Access:" -ForegroundColor Yellow
Write-Host "   🔗 Access via: https://localhost:3000" -ForegroundColor White
Write-Host ""
Write-Host "🔧 Backend API:" -ForegroundColor Yellow
Write-Host "   🔗 Running on: http://192.168.1.4:8000" -ForegroundColor White
Write-Host ""
Write-Host "Press Ctrl+C to stop all servers" -ForegroundColor Red
Write-Host ""

# Wait for user to stop
try {
    while ($true) {
        Start-Sleep -Seconds 1
    }
} finally {
    Write-Host "🛑 Stopping servers..." -ForegroundColor Red
    Stop-Job $backendJob -ErrorAction SilentlyContinue
    Stop-Job $frontendJob -ErrorAction SilentlyContinue
    Remove-Job $backendJob -ErrorAction SilentlyContinue
    Remove-Job $frontendJob -ErrorAction SilentlyContinue
    
    # Clean up processes
    Get-Process | Where-Object {$_.ProcessName -eq "python" -or $_.ProcessName -eq "node"} | Stop-Process -Force -ErrorAction SilentlyContinue
    
    Write-Host "✅ All servers stopped!" -ForegroundColor Green
} 