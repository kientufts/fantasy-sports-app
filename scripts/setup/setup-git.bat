@echo off
REM Git Setup Script for Personal Project - Windows
REM Run this script to configure git with your personal credentials

echo 🔧 Setting up git configuration for Fantasy Sports App
echo ======================================================

REM Get personal email from user
echo.
set /p personal_email="Enter your personal email address: "
set /p git_name="Enter your name for git commits: "

REM Configure git for this repository only (not global)
git config user.email "%personal_email%"
git config user.name "%git_name%"

echo.
echo ✅ Git configured with:
echo    Name: %git_name%
echo    Email: %personal_email%
echo.

REM Show current configuration
echo Current git config for this repository:
git config --local --list | findstr user

echo.
echo 🎉 Ready to commit! Your work credentials remain unchanged globally.
echo 📝 Next steps:
echo    1. git add .
echo    2. git commit -m "Initial commit: Fantasy Sports App"
echo    3. git remote add origin ^<your-repo-url^>
echo    4. git push -u origin main

pause
