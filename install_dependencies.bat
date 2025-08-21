@echo off
echo Installing dependencies for Receptionist Application...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Python is not installed or not in PATH. Please install Python 3.8 or higher.
    echo Visit https://www.python.org/downloads/ to download Python.
    pause
    exit /b 1
)

echo Installing required Python packages...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Checking for wkhtmltopdf installation...
where wkhtmltopdf >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo wkhtmltopdf is not installed or not in PATH.
    echo Please download and install wkhtmltopdf from:
    echo https://wkhtmltopdf.org/downloads.html
    echo.
    echo After installation, make sure it's added to your PATH.
)

echo.
echo Installation complete!
echo.
echo If you encounter any issues with printing:
echo 1. Make sure your printer is connected and set as default in Windows
echo 2. Try running the application as administrator
echo.
pause 