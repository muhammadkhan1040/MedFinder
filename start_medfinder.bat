@echo off
echo ============================================================
echo    MedFinder - Starting Full Application
echo ============================================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo [INFO] .env file not found - creating from template...
    if exist ".env.example" (
        copy ".env.example" ".env" > nul
        echo [✓] .env file created
        echo.
        echo [OPTIONAL] HF_TOKEN for AI validation:
        echo - Get from: https://huggingface.co/settings/tokens
        echo - App works WITHOUT this token (uses public APIs only)
        echo - You can add it later by editing .env file
        echo.
    ) else (
        echo [INFO] No .env.example found - continuing without .env
        echo The app will use public APIs only (no AI validation)
        echo.
    )
)

echo.
echo [1/2] Starting Backend Server (FastAPI)...
echo ============================================================
start "MedFinder Backend" cmd /k "cd /d "%~dp0backend_api" && echo Starting Backend on http://localhost:5000... && python app.py"

REM Wait a bit for backend to start
timeout /t 3 /nobreak > nul

echo.
echo [2/2] Starting Frontend Server (Vite + React)...
echo ============================================================
start "MedFinder Frontend" cmd /k "cd /d "%~dp0frontend" && echo Starting Frontend on http://localhost:5173... && npm run dev"

echo.
echo ============================================================
echo    MedFinder Application Started Successfully!
echo ============================================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo API Docs: http://localhost:5000/docs
echo.
echo Prescription Assistant: http://localhost:5173/prescription
echo.
echo Press any key to open MedFinder in your default browser...
pause > nul

REM Open frontend in default browser
start http://localhost:5173

echo.
echo Both servers are running in separate windows.
echo Close those windows to stop the servers.
echo.
echo Press any key to exit this window...
pause > nul
