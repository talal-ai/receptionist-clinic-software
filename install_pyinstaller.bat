@echo off
cd /d "%~dp0"
echo ============================================
echo   PyInstaller Direct Installation Helper
echo ============================================
echo.
echo This will attempt to download and install PyInstaller
echo directly without using pip's default installation method.
echo.
echo Press any key to continue or CTRL+C to cancel...
pause > nul

python install_pyinstaller.py

echo.
pause 