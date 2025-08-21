#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix imports for PyInstaller
Creates a temporary version of main.py that doesn't rely on sys.path manipulation
"""

import os
import sys
import shutil

def create_patched_main():
    """
    Create a patched version of main.py that doesn't use sys.path.append
    """
    print("Creating patched main.py for PyInstaller...")
    
    # Read the original main.py
    with open('main.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Backup the original file
    shutil.copy('main.py', 'main.py.bak')
    print("Created backup of main.py at main.py.bak")
    
    # Replace the sys.path.append line with direct imports
    patched_content = content.replace(
        "# Add the src directory to the path so we can import our modules\n"
        "sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))\n\n"
        "# Import our application modules\n"
        "from config.settings import Settings\n"
        "from ui.main_window import MainWindow",
        
        "# Import our application modules\n"
        "from src.config.settings import Settings\n"
        "from src.ui.main_window import MainWindow"
    )
    
    # Write the patched file
    with open('main.py', 'w', encoding='utf-8') as f:
        f.write(patched_content)
    
    print("Created patched main.py for PyInstaller build")
    return True

def restore_original_main():
    """
    Restore the original main.py from backup
    """
    if os.path.exists('main.py.bak'):
        shutil.copy('main.py.bak', 'main.py')
        os.remove('main.py.bak')
        print("Restored original main.py from backup")
        return True
    return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'restore':
        restore_original_main()
    else:
        create_patched_main() 