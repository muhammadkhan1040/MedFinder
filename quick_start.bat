@echo off
REM Quick Start - MedFinder Application
REM This starts both backend and frontend servers

echo Starting MedFinder...
echo.

REM Start Backend
start "MedFinder Backend" cmd /k "cd /d "%~dp0backend_api" && python app.py"

REM Wait 2 seconds
timeout /t 2 /nobreak > nul

REM Start Frontend
start "MedFinder Frontend" cmd /k "cd /d "%~dp0frontend" && npm run dev"

REM Wait 3 seconds
timeout /t 3 /nobreak > nul

REM Open browser
start http://localhost:5173

echo.
echo MedFinder started!
echo Backend: http://localhost:5000
echo Frontend: http://localhost:5173
echo.
