#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings module for the Receptionist Application
Handles loading and managing application settings
"""

import os
import json
import logging
from pathlib import Path

logger = logging.getLogger('receptionist.settings')

class Settings:
    """
    Settings class for the Receptionist Application
    Handles loading and saving application settings
    """
    
    DEFAULT_SETTINGS = {
        "app_name": "Clinic Receptionist",
        "company_name": "Dr. Muhammad Sajid Sohail",
        "data_path": "./data",
        "excel_file": "patients.xlsx",
        "backup_interval_days": 7,
        "auto_backup": True,
        "date_format": "%d-%m-%Y",
        "time_format": "%H:%M",
        "receipt_template": "default_template.html",
        "printer_name": "",  # Default printer
        "logo_path": "",
        "appointment_duration_mins": 30,
        "default_doctor": "Dr. Muhammad Sajid Sohail",
        "doctors": ["Dr. Muhammad Sajid Sohail"],
        "doctor_qualifications": "Consultant Physician\nMBBS (K.E), FCPS (Medicine)",
        "doctor_phones": [
            "0300-5809938",
            "0347-9809938"
        ],
        "theme": "default"
    }
    
    def __init__(self, settings_file=None):
        """
        Initialize settings from file or defaults
        
        Args:
            settings_file (str, optional): Path to settings file. Defaults to None.
        """
        self.config_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'src', 'config')
        
        if settings_file is None:
            self.settings_file = os.path.join(self.config_dir, 'settings.json')
        else:
            self.settings_file = settings_file
        
        # Initialize with default settings
        self.settings = self.DEFAULT_SETTINGS.copy()
        
        # Load settings from file if it exists
        self.load_settings()
        
        # Ensure data directory exists
        self.ensure_data_path()
        
    def ensure_data_path(self):
        """Ensure the data directory exists"""
        data_path = Path(self.settings['data_path'])
        
        # If relative path, make it absolute relative to project root
        if not data_path.is_absolute():
            project_root = Path(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
            data_path = project_root / data_path
        
        # Create the directory if it doesn't exist
        if not data_path.exists():
            data_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created data directory: {data_path}")
            
        # Update the setting with the absolute path
        self.settings['data_path'] = str(data_path)
    
    def load_settings(self):
        """Load settings from file"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    loaded_settings = json.load(f)
                    # Update default settings with loaded settings
                    self.settings.update(loaded_settings)
                    logger.info(f"Settings loaded from {self.settings_file}")
            else:
                # Save default settings to file
                self.save_settings()
                logger.info(f"Created default settings at {self.settings_file}")
        except Exception as e:
            logger.error(f"Error loading settings: {e}")
            # Continue with default settings
    
    def save_settings(self):
        """Save settings to file"""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4)
            logger.info(f"Settings saved to {self.settings_file}")
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
    
    def get(self, key, default=None):
        """
        Get a setting value
        
        Args:
            key (str): Setting key
            default: Default value if key is not found
            
        Returns:
            The setting value or default
        """
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """
        Set a setting value and save settings
        
        Args:
            key (str): Setting key
            value: Setting value
        """
        self.settings[key] = value
        self.save_settings()
        
    def get_excel_path(self):
        """
        Get the full path to the Excel file
        
        Returns:
            str: Full path to the Excel file
        """
        return os.path.join(self.settings['data_path'], self.settings['excel_file'])
        
    def __str__(self):
        """String representation of settings"""
        return f"Settings: {json.dumps(self.settings, indent=2)}" 