#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Handler for the Receptionist Application
Handles reading and writing patient data to Excel
"""

import os
import logging
import pandas as pd
from datetime import datetime
import shutil
from pathlib import Path

logger = logging.getLogger('receptionist.excel_handler')

class ExcelHandler:
    """
    Excel Handler class for the Receptionist Application
    Handles reading and writing patient data to Excel
    """
    
    # Define the columns for the Excel file
    COLUMNS = [
        'patient_id', 
        'token_number',
        'first_name', 
        'last_name', 
        'guardian_relation',
        'address', 
        'city',
        'postal_code',
        'phone_number', 
        'email',
        'doctor_name', 
        'appointment_date', 
        'appointment_time',  # This is used for checkup time
        'arrival_time',
        'appointment_duration',
        'fees',
        'reason_for_visit',
        'notes',
        'created_at',
        'updated_at'
    ]
    
    def __init__(self, settings):
        """
        Initialize the Excel Handler
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.excel_path = settings.get_excel_path()
        self.ensure_excel_file()
        
    def ensure_excel_file(self):
        """Ensure the Excel file exists with proper structure"""
        try:
            if not os.path.exists(self.excel_path):
                # Create a new Excel file with the proper columns
                df = pd.DataFrame(columns=self.COLUMNS)
                
                # Save the DataFrame to Excel
                df.to_excel(self.excel_path, index=False)
                logger.info(f"Created new Excel file at {self.excel_path}")
            else:
                # Verify the Excel file has the proper columns
                df = pd.read_excel(self.excel_path)
                
                # Check if all required columns exist
                missing_columns = set(self.COLUMNS) - set(df.columns)
                
                if missing_columns:
                    # Add missing columns
                    for col in missing_columns:
                        df[col] = ''
                    
                    # Create a backup before modifying
                    self._create_backup()
                    
                    # Save the updated DataFrame to Excel
                    df.to_excel(self.excel_path, index=False)
                    logger.info(f"Added missing columns to Excel file: {missing_columns}")
        except Exception as e:
            logger.error(f"Error ensuring Excel file: {e}")
            raise
    
    def _create_backup(self):
        """Create a backup of the Excel file"""
        try:
            if os.path.exists(self.excel_path):
                # Create backups directory if it doesn't exist
                backup_dir = os.path.join(os.path.dirname(self.excel_path), 'backups')
                os.makedirs(backup_dir, exist_ok=True)
                
                # Create a backup filename with timestamp
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                backup_filename = f"patients_backup_{timestamp}.xlsx"
                backup_path = os.path.join(backup_dir, backup_filename)
                
                # Copy the Excel file to the backup path
                shutil.copy2(self.excel_path, backup_path)
                logger.info(f"Created backup at {backup_path}")
                
                # Clean up old backups if needed
                self._cleanup_old_backups(backup_dir)
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
    
    def _cleanup_old_backups(self, backup_dir, max_backups=10):
        """
        Clean up old backups, keeping only the most recent ones
        
        Args:
            backup_dir (str): Path to backups directory
            max_backups (int, optional): Maximum number of backups to keep. Defaults to 10.
        """
        try:
            # Get a list of backup files
            backup_files = sorted([
                os.path.join(backup_dir, f) 
                for f in os.listdir(backup_dir) 
                if f.startswith('patients_backup_') and f.endswith('.xlsx')
            ])
            
            # Remove old backups if there are too many
            if len(backup_files) > max_backups:
                files_to_remove = backup_files[:-max_backups]
                for file_path in files_to_remove:
                    os.remove(file_path)
                    logger.info(f"Removed old backup: {file_path}")
        except Exception as e:
            logger.error(f"Error cleaning up old backups: {e}")
    
    def get_all_patients(self):
        """
        Get all patients from the Excel file
        
        Returns:
            pandas.DataFrame: DataFrame containing all patients
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Replace NaN values with empty strings
            df = df.fillna('')
            
            return df
        except Exception as e:
            logger.error(f"Error getting all patients: {e}")
            return pd.DataFrame(columns=self.COLUMNS)
    
    def get_patient_by_id(self, patient_id):
        """
        Get a patient by ID
        
        Args:
            patient_id (str): Patient ID
            
        Returns:
            dict: Patient data or None if not found
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Replace NaN values with empty strings
            df = df.fillna('')
            
            patient = df[df['patient_id'] == patient_id]
            
            if len(patient) == 0:
                return None
                
            # Convert to dict
            patient_dict = patient.iloc[0].to_dict()
            
            # Ensure no NaN values in the dictionary
            for key, value in patient_dict.items():
                if pd.isna(value) or value == 'nan' or value == 'NaN':
                    patient_dict[key] = ''
            
            return patient_dict
        except Exception as e:
            logger.error(f"Error getting patient by ID: {e}")
            return None
    
    def get_patients_by_name(self, name):
        """
        Search for patients by name (first or last)
        
        Args:
            name (str): Name to search for
            
        Returns:
            pandas.DataFrame: DataFrame containing matching patients
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Replace NaN values with empty strings to avoid search errors
            df['first_name'].fillna('', inplace=True)
            df['last_name'].fillna('', inplace=True)
            
            # Search in first_name and last_name columns
            matches = df[
                df['first_name'].str.contains(name, case=False, na=False) |
                df['last_name'].str.contains(name, case=False, na=False)
            ]
            
            return matches
        except Exception as e:
            logger.error(f"Error searching patients by name: {e}")
            return pd.DataFrame(columns=self.COLUMNS)
    
    def add_patient(self, patient_data):
        """
        Add a new patient to the Excel file
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing data
            df = pd.read_excel(self.excel_path)
            
            # Generate a unique patient ID if not provided
            if 'patient_id' not in patient_data or not patient_data['patient_id']:
                # Simple ID generation - can be enhanced as needed
                now = datetime.now()
                patient_data['patient_id'] = f"P{now.strftime('%Y%m%d%H%M%S')}"
            
            # Generate sequential token number if not provided
            if 'token_number' not in patient_data or not patient_data['token_number']:
                # Find the current highest token number
                if 'token_number' in df.columns and not df.empty:
                    # Convert to numeric, ignoring errors (will convert non-numeric to NaN)
                    df['token_number_numeric'] = pd.to_numeric(df['token_number'], errors='coerce')
                    # Get the maximum, defaulting to 0 if all are NaN
                    current_max = df['token_number_numeric'].max()
                    # If max is NaN, start from 0
                    if pd.isna(current_max):
                        current_max = 0
                    # Set the new token number
                    patient_data['token_number'] = str(int(current_max) + 1)
                else:
                    # Start from 1 if no existing tokens
                    patient_data['token_number'] = "1"
            
            # Add timestamps
            now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            patient_data['created_at'] = now_str
            patient_data['updated_at'] = now_str
            
            # Ensure all required columns exist in patient_data
            for col in self.COLUMNS:
                if col not in patient_data:
                    patient_data[col] = ''
                elif pd.isna(patient_data[col]) or patient_data[col] == 'nan' or patient_data[col] == 'NaN':
                    patient_data[col] = ''
            
            # Append the new patient data
            df = pd.concat([df, pd.DataFrame([patient_data])], ignore_index=True)
            
            # Create a backup before saving
            self._create_backup()
            
            # Save the updated DataFrame to Excel
            df.to_excel(self.excel_path, index=False)
            logger.info(f"Added new patient: {patient_data['patient_id']} with token number: {patient_data['token_number']}")
            
            return True
        except Exception as e:
            logger.error(f"Error adding patient: {e}")
            return False
    
    def update_patient(self, patient_id, patient_data):
        """
        Update an existing patient in the Excel file
        
        Args:
            patient_id (str): Patient ID
            patient_data (dict): Updated patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing data
            df = pd.read_excel(self.excel_path)
            
            # Find the patient
            mask = df['patient_id'] == patient_id
            
            if not mask.any():
                logger.warning(f"Patient not found: {patient_id}")
                return False
            
            # Update timestamp
            patient_data['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Handle NaN values
            for key, value in patient_data.items():
                if pd.isna(value) or value == 'nan' or value == 'NaN':
                    patient_data[key] = ''
            
            # Update the patient data
            for key, value in patient_data.items():
                if key in df.columns:
                    df.loc[mask, key] = value
            
            # Create a backup before saving
            self._create_backup()
            
            # Save the updated DataFrame to Excel
            df.to_excel(self.excel_path, index=False)
            logger.info(f"Updated patient: {patient_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error updating patient: {e}")
            return False
    
    def delete_patient(self, patient_id):
        """
        Delete a patient from the Excel file
        
        Args:
            patient_id (str): Patient ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Read existing data
            df = pd.read_excel(self.excel_path)
            
            # Find the patient
            mask = df['patient_id'] == patient_id
            
            if not mask.any():
                logger.warning(f"Patient not found: {patient_id}")
                return False
            
            # Create a backup before deleting
            self._create_backup()
            
            # Remove the patient
            df = df[~mask]
            
            # Save the updated DataFrame to Excel
            df.to_excel(self.excel_path, index=False)
            logger.info(f"Deleted patient: {patient_id}")
            
            return True
        except Exception as e:
            logger.error(f"Error deleting patient: {e}")
            return False
    
    def get_appointments_for_date(self, date):
        """
        Get all appointments for a specific date
        
        Args:
            date (str): Date in format YYYY-MM-DD
            
        Returns:
            pandas.DataFrame: DataFrame containing appointments for the date
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Replace NaN values with empty strings
            df = df.fillna('')
            
            # Filter by date
            appointments = df[df['appointment_date'] == date]
            
            # Sort by time
            appointments = appointments.sort_values('appointment_time')
            
            return appointments
        except Exception as e:
            logger.error(f"Error getting appointments for date: {e}")
            return pd.DataFrame(columns=self.COLUMNS)
    
    def get_appointments_for_doctor(self, doctor_name, date=None):
        """
        Get all appointments for a specific doctor
        
        Args:
            doctor_name (str): Doctor name
            date (str, optional): Date in format YYYY-MM-DD. Defaults to None.
            
        Returns:
            pandas.DataFrame: DataFrame containing appointments for the doctor
        """
        try:
            df = pd.read_excel(self.excel_path)
            
            # Replace NaN values with empty strings
            df = df.fillna('')
            
            # Filter by doctor name
            appointments = df[df['doctor_name'] == doctor_name]
            
            # Further filter by date if provided
            if date:
                appointments = appointments[appointments['appointment_date'] == date]
            
            # Sort by date and time
            appointments = appointments.sort_values(['appointment_date', 'appointment_time'])
            
            return appointments
        except Exception as e:
            logger.error(f"Error getting appointments for doctor: {e}")
            return pd.DataFrame(columns=self.COLUMNS) 