# PyInstaller Troubleshooting Guide

If you're experiencing issues with PyInstaller when building the standalone Receptionist application, here are some common problems and solutions:

## Installation Issues

### Connection Timeout

**Problem:** PyInstaller download fails with connection timeout errors.

**Solutions:**
1. Try using a more stable internet connection
2. Install with the `--user` flag: `pip install --user pyinstaller`
3. Download PyInstaller manually from [PyPI](https://pypi.org/project/pyinstaller/#files) and install with:
   ```
   pip install [downloaded-file-path]
   ```
4. Try setting a different PyPI mirror:
   ```
   pip install --user pyinstaller -i https://mirrors.aliyun.com/pypi/simple/
   ```

### Access Denied or File in Use

**Problem:** `Error: [WinError 32] The process cannot access the file because it is being used by another process`

**Solutions:**
1. Close any running Python processes or IDEs
2. Run Command Prompt as Administrator
3. Restart your computer
4. Install with `--user` flag: `pip install --user pyinstaller`

## Build Issues

### Missing Modules

**Problem:** When running the application, you get "No module named X" errors.

**Solutions:**
1. Add missing modules to the PyInstaller command with `--hidden-import=module_name`
2. Edit the build_standalone.py file to add these imports to the pyinstaller_cmd list

### Missing Files or Resources

**Problem:** The application can't find certain files or resources.

**Solution:**
Make sure all required files are included in the build by adding them to the `--add-data` option in build_standalone.py:
```python
"--add-data=path/to/file;destination/in/package"
```

### Antivirus Blocking

**Problem:** Antivirus software may flag or block PyInstaller-generated executables.

**Solutions:**
1. Add an exception in your antivirus software
2. Use a trusted signing certificate to sign your executable

## Distribution Issues

### DLL Missing Errors

**Problem:** Users see "Missing DLL" errors when running the executable.

**Solution:**
1. Try building with `--onefile` option (already in our script)
2. Include the Microsoft Visual C++ Redistributable with your application

### "Not a valid Win32 application" Error

**Problem:** Windows shows "not a valid Win32 application" error when running the exe.

**Solutions:**
1. Make sure you're building for the correct architecture (32-bit vs 64-bit)
2. Try rebuilding with a clean environment: `python -m PyInstaller --clean --onefile main.py`

## Manual Build Instructions

If the automated scripts aren't working, you can try building manually:

1. Install PyInstaller:
   ```
   pip install --user pyinstaller
   ```

2. Build the executable:
   ```
   python -m PyInstaller --name=Receptionist --onefile --windowed --add-data="src/resources;src/resources" main.py
   ```

3. Look for the generated executable in the `dist` folder. 