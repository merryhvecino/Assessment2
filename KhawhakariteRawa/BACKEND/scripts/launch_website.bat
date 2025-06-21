@echo off
echo Starting Kaiwhakarite Rawa Backend Server...
echo.

echo Starting Backend Server (FastAPI)...
start /min "Backend Server" cmd /k "cd .. && python scripts/run_server.py"

echo.
echo Backend server is starting...
echo Backend API: http://localhost:8000
echo.
echo Please wait a few seconds for the server to start.
echo Then you can access the API at http://localhost:8000
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.
pause 