@echo off
REM Launch script for Windows

echo Fantasy Sports App Launcher
echo ==========================

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not found in PATH
    echo Please install Python 3.8+ from https://python.org and try again
    pause
    exit /b 1
)

echo Using Python command: python

REM Check if requirements are installed
python -c "import flask" 2>nul
if %errorlevel% neq 0 (
    echo Installing dependencies...
    python -m pip install -r requirements.txt
)

echo.
echo Choose an option:
echo 1^) Run Console App
echo 2^) Run Web App
echo 3^) Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" (
    echo Starting console app...
    python main.py
) else if "%choice%"=="2" (
    echo Starting web app...
    echo Open http://localhost:5000 in your browser
    python app.py
) else if "%choice%"=="3" (
    echo Goodbye!
    exit /b 0
) else (
    echo Invalid choice. Exiting.
    pause
    exit /b 1
)

pause
