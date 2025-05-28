#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receptionist Application for Doctor's Clinic
Main Entry Point
"""

import os
import sys
import logging
from datetime import datetime

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Import our application modules
from config.settings import Settings
from ui.main_window import MainWindow

def setup_logging():
    """Set up logging configuration"""
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    log_file = os.path.join(log_dir, f'receptionist_{datetime.now().strftime("%Y%m%d")}.log')
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger('receptionist')

def main():
    """Main entry point for the application"""
    # Set up logging
    logger = setup_logging()
    logger.info("Starting Receptionist Application")
    
    try:
        # Load settings
        settings = Settings()
        
        # Start the UI
        app = MainWindow(settings)
        app.run()
        
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)
        return 1
    
    logger.info("Receptionist Application shutting down")
    return 0

if __name__ == "__main__":
    sys.exit(main()) 