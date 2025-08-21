@echo off
cd /d "%~dp0"
echo ================================================
echo   Receptionist Distribution Package Creator
echo ================================================
echo.

:: Check if dist folder exists
if not exist dist\Receptionist.exe (
    echo ERROR: Receptionist.exe not found in dist folder.
    echo Please run build_standalone.bat first to create the executable.
    echo.
    pause
    exit /b 1
)

echo Creating distribution package...

:: Create a distribution folder
set DIST_FOLDER=Receptionist_Standalone
if exist %DIST_FOLDER% (
    echo Removing existing distribution folder...
    rmdir /s /q %DIST_FOLDER%
)

:: Create the folder structure
mkdir %DIST_FOLDER%

:: Copy the executable
echo Copying executable...
copy dist\Receptionist.exe %DIST_FOLDER%\

:: Create a launcher
echo Creating launcher shortcut...
echo @echo off > %DIST_FOLDER%\Start_Receptionist.bat
echo start Receptionist.exe >> %DIST_FOLDER%\Start_Receptionist.bat

:: Add a readme file
echo Creating readme file...
echo Receptionist Application > %DIST_FOLDER%\README.txt
echo ======================== >> %DIST_FOLDER%\README.txt
echo. >> %DIST_FOLDER%\README.txt
echo To start the application, double-click on "Receptionist.exe" >> %DIST_FOLDER%\README.txt
echo or use the "Start_Receptionist.bat" file. >> %DIST_FOLDER%\README.txt
echo. >> %DIST_FOLDER%\README.txt
echo If you encounter any issues, please contact the developer. >> %DIST_FOLDER%\README.txt

:: Zip the distribution folder if possible
where /q powershell
if %ERRORLEVEL% EQU 0 (
    echo Creating ZIP archive...
    powershell -command "Compress-Archive -Path '%DIST_FOLDER%' -DestinationPath '%DIST_FOLDER%.zip' -Force"
    echo Distribution package created: %DIST_FOLDER%.zip
) else (
    echo PowerShell not found, skipping ZIP creation.
    echo Distribution package created: %DIST_FOLDER% folder
)

echo.
echo Distribution package ready!
echo.
pause 