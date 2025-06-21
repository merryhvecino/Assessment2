@echo off
echo 🚀 Kaiwhakarite Rawa - Quick Launch
echo =================================
echo.

REM Check if we're in the right directory
if not exist "scripts\launch_website.bat" (
    echo ❌ Error: launch_website.bat not found in scripts directory
    echo Please run this script from the project root directory
    pause
    exit /b 1
)

echo 📁 Project structure organized ✓
echo 🔧 Launching from scripts directory...
echo.

REM Execute the main launch script
call "scripts\launch_website.bat" 