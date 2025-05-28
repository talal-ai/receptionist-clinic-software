@echo off
echo Starting Clinic Receptionist...
echo.

:: Check if wkhtmltopdf is installed
where wkhtmltopdf >nul 2>&1
if %errorlevel% neq 0 (
    echo NOTE: wkhtmltopdf is not installed. PDF reception slips will be displayed as HTML instead.
    echo You can install wkhtmltopdf from https://wkhtmltopdf.org/downloads.html for full PDF functionality.
    echo.
    echo Press any key to continue anyway...
    pause >nul
)

python main.py
pause