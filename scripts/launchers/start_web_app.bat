@echo off
cd /d "%~dp0"
title Fantasy Sports Web App

:start
echo Starting Fantasy Sports App...
echo Access at: http://127.0.0.1:5000
echo Press Ctrl+C to stop the app
echo.

C:\Users\trung\AppData\Local\Programs\Python\Python312\python.exe app.py

echo.
echo App stopped. Restarting in 5 seconds...
echo Press Ctrl+C now if you want to quit permanently.
timeout /t 5 /nobreak > nul
goto start
