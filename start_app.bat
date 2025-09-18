@echo off
REM Windows batch file for Fantasy Sports App
REM This provides the same functionality as the PowerShell and bash versions

title Fantasy Sports App - Quick Start

echo Fantasy Sports App - Quick Start
echo =================================

REM Check for Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo Found Python: 
    python --version
) else (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later from python.org
    pause
    exit /b 1
)

REM Check if we're in the right directory
if not exist "launcher.py" (
    echo Error: Please run this script from the fantasy app directory
    echo Make sure launcher.py is in the current directory
    pause
    exit /b 1
)

echo Starting launcher...
python launcher.py

pause
