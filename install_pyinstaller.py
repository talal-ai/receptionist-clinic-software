import os
import sys
import tempfile
import urllib.request
import subprocess
from zipfile import ZipFile

def download_and_install_pyinstaller():
    """
    Download PyInstaller wheel file directly and install it
    """
    print("Downloading PyInstaller directly...")
    
    # PyInstaller version and URL - update as needed
    version = "6.14.1"
    
    # Determine the correct wheel file based on Python version
    py_version = f"{sys.version_info.major}{sys.version_info.minor}"
    
    # For 64-bit Windows
    wheel_filename = f"pyinstaller-{version}-py3-none-win_amd64.whl"
    url = f"https://files.pythonhosted.org/packages/73/d2/70db75a1b305cd06fa4d16cfe1c5e2bb3e2c9fcaef5e5de01f47ef57a16b/{wheel_filename}"
    
    try:
        # Create a temporary directory
        with tempfile.TemporaryDirectory() as temp_dir:
            wheel_path = os.path.join(temp_dir, wheel_filename)
            
            # Download the wheel file
            print(f"Downloading from {url}...")
            urllib.request.urlretrieve(url, wheel_path)
            
            # Install the wheel file
            print("Installing PyInstaller...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "--user", wheel_path])
            
            print("PyInstaller installed successfully!")
            return True
    except Exception as e:
        print(f"Error installing PyInstaller: {e}")
        return False

if __name__ == "__main__":
    if download_and_install_pyinstaller():
        print("\nYou can now run build_standalone.bat to create the executable.")
    else:
        print("\nInstallation failed. Please see PYINSTALLER_TROUBLESHOOTING.md for more options.") 