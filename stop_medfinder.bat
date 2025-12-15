@echo off
echo ============================================================
echo    MedFinder - Stopping All Servers
echo ============================================================
echo.

echo Stopping Node.js processes (Frontend)...
taskkill /F /IM node.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] Frontend server stopped
) else (
    echo [!] No Node.js processes found
)

echo.
echo Stopping Python processes (Backend)...
taskkill /F /IM python.exe /T 2>nul
if %ERRORLEVEL% EQU 0 (
    echo [✓] Backend server stopped
) else (
    echo [!] No Python processes found
)

echo.
echo ============================================================
echo    All MedFinder servers stopped!
echo ============================================================
echo.
pause
