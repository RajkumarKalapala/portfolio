@echo off
:: USBLOCKR Launcher – ensures Administrator privileges
:: Double-click this file to run USBLOCKR

net session >nul 2>&1
if %errorlevel% == 0 (
    echo Running as Administrator...
    python main.py
) else (
    echo Requesting Administrator privileges...
    powershell -Command "Start-Process cmd -ArgumentList '/c cd /d %~dp0 && python main.py && pause' -Verb RunAs"
)
