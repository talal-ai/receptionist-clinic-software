import os
import sys
import shutil
import subprocess

def run_pyinstaller():
    """
    Build a standalone executable using PyInstaller
    """
    print("Building standalone executable with PyInstaller...")
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("Using PyInstaller version:", PyInstaller.__version__)
    except ImportError:
        print("ERROR: PyInstaller is not installed.")
        print("Please install it first with: pip install --user pyinstaller")
        sys.exit(1)
    
    # Command to build a standalone executable
    pyinstaller_cmd = [
        sys.executable, 
        "-m", 
        "PyInstaller",
        "--name=Receptionist",
        "--onefile",  # Create a single file executable
        "--windowed",  # Don't show console window when app runs
        "--paths=src",  # Add src directory to Python path
        "--add-data=src;src",  # Include src directory and all its contents
        "--add-data=src/resources;src/resources",  # Include resources folder
        # Add hidden imports for modules that might not be detected
        "--hidden-import=config",
        "--hidden-import=config.settings",
        "--hidden-import=ui",
        "--hidden-import=ui.main_window",
        "--hidden-import=models",
        "--hidden-import=utils",
        "--hidden-import=PIL",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
        "--collect-all=config",
        "--collect-all=ui",
        "--collect-all=models",
        "--collect-all=utils",
        "--collect-all=PIL",
        "main.py"  # Main script
    ]
    
    # Run PyInstaller
    try:
        subprocess.check_call(pyinstaller_cmd)
        print("\nStandalone executable has been created in the 'dist' folder.")
        print("You can distribute the 'Receptionist.exe' file to your clients.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: PyInstaller failed with exit code {e.returncode}")
        print("Please check the error messages above.")
        return False

if __name__ == "__main__":
    success = run_pyinstaller()
    sys.exit(0 if success else 1) 