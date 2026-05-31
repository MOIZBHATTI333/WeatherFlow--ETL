@echo off
REM Run the weather data scheduler in the background
cd /d %~dp0
pythonw scheduler.py
pause