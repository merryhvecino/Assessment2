Write-Host "🚀 Kaiwhakarite Rawa - Quick Launch" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""

# Check if we're in the right directory
if (-not (Test-Path "scripts/launch_website.ps1")) {
    Write-Host "❌ Error: launch_website.ps1 not found in scripts directory" -ForegroundColor Red
    Write-Host "Please run this script from the project root directory" -ForegroundColor Yellow
    exit 1
}

Write-Host "📁 Project structure organized ✓" -ForegroundColor Green
Write-Host "🔧 Launching from scripts directory..." -ForegroundColor Cyan
Write-Host ""

# Execute the main launch script
& ".\scripts\launch_website.ps1"