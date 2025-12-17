@echo off
REM One-click start for Indeed_Job_Scraper
REM This script will try to activate .venv if present, then run src\main.py with passed arguments.

:: Move to script directory
cd /d "%~dp0"

:: If .venv exists, try to activate it (PowerShell activation may be used)
if exist ".venv\Scripts\activate.bat" (
    echo Activating virtual environment .venv...
    call .venv\Scripts\activate.bat
) else (
    echo No .venv found. Using system Python.
)

:: Default arguments (can be overridden by passing args to this .bat)
set ARGS=--headless --port 5000

:: If user provided args, use them instead
if not "%*"=="" set ARGS=%*

:run_app
echo Starting Indeed Job Scraper with args: %ARGS%
python .\src\main.py %ARGS%

:cleanup
echo Exited. Press any key to close...
pause >nul
