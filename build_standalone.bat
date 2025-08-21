@echo off
cd /d "%~dp0"
echo ================================================
echo   Receptionist Standalone Application Builder
echo ================================================
echo.

:: Check if PyInstaller is installed
python -c "import PyInstaller" 2>NUL
if %ERRORLEVEL% NEQ 0 (
    echo PyInstaller is not installed. Attempting to install...
    echo.
    
    :: Try with --user flag first
    echo Trying with --user flag...
    python -m pip install --user pyinstaller
    
    :: Check if installation was successful
    python -c "import PyInstaller" 2>NUL
    if %ERRORLEVEL% NEQ 0 (
        echo.
        echo Failed to install PyInstaller automatically.
        echo.
        echo Please try one of these options:
        echo 1. Run as administrator
        echo 2. Manually install with: pip install --user pyinstaller
        echo 3. Download PyInstaller from: https://pypi.org/project/pyinstaller/#files
        echo.
        pause
        exit /b 1
    ) else (
        echo PyInstaller installed successfully.
    )
) else (
    echo PyInstaller is already installed.
)

echo.
echo Fixing imports for PyInstaller...
python fix_imports.py
if %ERRORLEVEL% NEQ 0 (
    echo Failed to fix imports.
    pause
    exit /b 1
)

echo.
echo Building standalone executable...
echo.
python build_standalone.py

set BUILD_RESULT=%ERRORLEVEL%

echo.
echo Restoring original main.py...
python fix_imports.py restore

if %BUILD_RESULT% NEQ 0 (
    echo.
    echo Build process failed. Please check the errors above.
    echo.
    pause
    exit /b 1
)

echo.
echo Build completed successfully!
echo The standalone executable is in the 'dist' folder.
echo Simply copy the Receptionist.exe file to the client's computer.
echo.
pause 