@echo off
title Cryptex - Secure Note Manager
cls

echo.
echo  ╔═══════════════════════════════════════╗
echo  ║           CRYPTEX v2.0                ║
echo  ║      Secure Note Manager              ║
echo  ╚═══════════════════════════════════════╝
echo.

:: Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

:: Check if required packages are installed
echo [*] Checking requirements...
python -c "import PyQt6, cryptography, argon2" >nul 2>&1
if errorlevel 1 (
    echo [*] Installing required packages...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERROR] Failed to install requirements
        pause
        exit /b 1
    )
)

:: Start the application
echo [*] Starting Cryptex...
python main.py

:: Keep window open if there's an error
if errorlevel 1 (
    echo.
    echo [ERROR] Application crashed. Check the error above.
    pause
)