@echo off
cd /d "%~dp0"
title Cryptex - Secure Note Manager

:: Hide the console window
if not DEFINED IS_MINIMIZED set IS_MINIMIZED=1 && start "" /min "%~dpnx0" %* && exit

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Python is not installed. Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Install requirements silently
python -m pip install -r requirements.txt >nul 2>&1

:: Start Cryptex
python main.py

:: Keep window open only if there's an error
if errorlevel 1 (
    echo.
    echo Application error occurred. Press any key to exit.
    pause >nul
)