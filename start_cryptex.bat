@echo off
title Cryptex - Secure Note Manager

:: Hide console window after startup
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

:: Change to script directory
cd /d "%~dp0"

:: Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo Python not found. Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

:: Install requirements silently
echo Installing requirements...
python -m pip install -r requirements.txt --quiet --disable-pip-version-check >nul 2>&1

:: Launch Cryptex
echo Starting Cryptex...
python main.py

:: Only pause if there was an error
if errorlevel 1 (
    echo.
    echo An error occurred. Press any key to exit.
    pause >nul
)