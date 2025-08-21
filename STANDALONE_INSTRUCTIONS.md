# Receptionist Standalone Application Instructions

This document explains how to create a standalone executable version of the Receptionist application that can be distributed to clients and run without installing Python or any dependencies.

## Building the Standalone Application

1. Make sure all requirements are installed on your development machine:
   ```
   pip install -r requirements.txt
   ```

2. Double-click the `build_standalone.bat` file to run the build process.
   - This will automatically install PyInstaller if needed
   - It will modify main.py temporarily to fix import issues
   - It will restore the original main.py after building

3. Wait for the process to complete. This may take a few minutes.

4. When finished, you'll find the standalone executable (`Receptionist.exe`) in the `dist` folder.

## Creating a Distribution Package

For a more professional distribution to clients:

1. After building the standalone executable, run `package_for_distribution.bat`

2. This will create:
   - A folder named `Receptionist_Standalone` containing the executable and helper files
   - A ZIP archive of this folder (if PowerShell is available)

3. You can distribute either the folder or the ZIP file to your clients.

## Distributing to Clients

Give your clients these instructions:

1. Extract the ZIP file (if provided) to a location of your choice.

2. To run the application, either:
   - Double-click `Receptionist.exe`, or
   - Double-click `Start_Receptionist.bat`

3. No installation process is needed - the application runs directly from the executable.

## Troubleshooting

If you encounter issues with building the standalone application:

1. Check the `PYINSTALLER_TROUBLESHOOTING.md` file for common problems and solutions.

2. If PyInstaller fails to install through the normal process, try:
   - Running `install_pyinstaller.bat` which uses a direct download method
   - Installing manually with `pip install --user pyinstaller`

If the client has issues with the standalone application:

1. Check if the client's antivirus is blocking the application.
2. Make sure the client has appropriate permissions to run executables.
3. If a specific error message appears, please document it and contact the developer.

## Additional Notes

- The standalone executable includes all required dependencies and Python runtime.
- When running the first time, it may take a few seconds to start as it extracts necessary files.
- The executable size will be larger than the original code due to including all dependencies. 