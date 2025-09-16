import os
import sys
import shutil
import subprocess
import argparse

def run_pyinstaller(mode: str = "prod") -> bool:
    """Build a standalone executable using PyInstaller.

    Modes:
    - fast:   Quicker developer build (onedir, no UPX, minimal datas)
    - prod:   Single-file exe for distribution (onefile)
    """
    if mode not in {"fast", "prod"}:
        print(f"Unknown mode '{mode}'. Use 'fast' or 'prod'.")
        return False

    print(f"Building standalone executable with PyInstaller (mode={mode})...")
    
    # Check if PyInstaller is available
    try:
        import PyInstaller
        print("Using PyInstaller version:", PyInstaller.__version__)
    except ImportError:
        print("ERROR: PyInstaller is not installed.")
        print("Please install it first with: pip install --user pyinstaller")
        sys.exit(1)
    
    # Base command
    pyinstaller_cmd = [sys.executable, "-m", "PyInstaller", "--name=Receptionist", "--windowed", "--paths=src"]

    # Data files (keep minimal to reduce build time)
    # IMPORTANT: Do NOT add the whole 'src' as data (it bloats and slows builds).
    pyinstaller_cmd += [
        "--add-data=src/resources;src/resources",
        "--add-data=src/assets;src/assets",
    ]

    # Hidden imports that PyInstaller sometimes misses
    pyinstaller_cmd += [
        "--hidden-import=config",
        "--hidden-import=config.settings",
        "--hidden-import=ui",
        "--hidden-import=ui.main_window",
        "--hidden-import=models",
        "--hidden-import=utils",
        "--hidden-import=PIL._tkinter_finder",
        "--hidden-import=PIL.Image",
        "--hidden-import=PIL.ImageTk",
    ]

    # FAST vs PROD configuration
    if mode == "fast":
        # Faster iterative builds: folder output, no UPX, fewer collects
        pyinstaller_cmd += [
            "--onedir",
            "--log-level=WARN",
            # Intentionally avoid --clean to leverage cache for speed
        ]
        # Avoid heavy collect-all for PIL; usually not needed for our usage
        pyinstaller_cmd += [
            "--collect-all=config",
            "--collect-all=ui",
            "--collect-all=models",
            "--collect-all=utils",
        ]
    else:  # prod
        # Distribution-friendly: single-file exe. Optionally disable UPX to speed build.
        pyinstaller_cmd += [
            "--onefile",
            # Disable UPX by default for speed; re-enable by adding --use-upx flag when needed
            "--noupx",
            "--collect-all=config",
            "--collect-all=ui",
            "--collect-all=models",
            "--collect-all=utils",
            # Avoid --collect-all=PIL to reduce size/time unless you need plugins beyond ImageTk
        ]

    # Entry point
    pyinstaller_cmd += ["main.py"]
    
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

def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Build Receptionist app with PyInstaller")
    parser.add_argument("--mode", choices=["fast", "prod"], default="prod", help="Build mode: fast (dev) or prod (distribution)")
    return parser.parse_args(argv)


if __name__ == "__main__":
    args = parse_args()
    success = run_pyinstaller(mode=args.mode)
    sys.exit(0 if success else 1)