#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patient Model for the Receptionist Application
Handles patient data operations
"""

import logging
from utils.excel_handler import ExcelHandler
from utils.print_handler import PrintHandler
from utils.stats_handler import StatsHandler

logger = logging.getLogger('receptionist.patient_model')

class PatientModel:
    """
    Patient Model class for the Receptionist Application
    Handles patient data operations
    """
    
    def __init__(self, settings):
        """
        Initialize the Patient Model
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.excel_handler = ExcelHandler(settings)
        self.print_handler = PrintHandler(settings)
        self.stats_handler = StatsHandler(self.excel_handler)
    
    def get_all_patients(self):
        """
        Get all patients
        
        Returns:
            pandas.DataFrame: DataFrame containing all patients
        """
        return self.excel_handler.get_all_patients()
    
    def get_patient_by_id(self, patient_id):
        """
        Get a patient by ID
        
        Args:
            patient_id (str): Patient ID
            
        Returns:
            dict: Patient data or None if not found
        """
        return self.excel_handler.get_patient_by_id(patient_id)
    
    def search_patients_by_name(self, name):
        """
        Search for patients by name (first or last)
        
        Args:
            name (str): Name to search for
            
        Returns:
            pandas.DataFrame: DataFrame containing matching patients
        """
        return self.excel_handler.get_patients_by_name(name)
    
    def add_patient(self, patient_data):
        """
        Add a new patient
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.excel_handler.add_patient(patient_data)
    
    def update_patient(self, patient_id, patient_data):
        """
        Update an existing patient
        
        Args:
            patient_id (str): Patient ID
            patient_data (dict): Updated patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.excel_handler.update_patient(patient_id, patient_data)
    
    def delete_patient(self, patient_id):
        """
        Delete a patient
        
        Args:
            patient_id (str): Patient ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.excel_handler.delete_patient(patient_id)
    
    def get_appointments_for_date(self, date):
        """
        Get all appointments for a specific date
        
        Args:
            date (str): Date in format YYYY-MM-DD
            
        Returns:
            pandas.DataFrame: DataFrame containing appointments for the date
        """
        return self.excel_handler.get_appointments_for_date(date)
    
    def get_appointments_for_doctor(self, doctor_name, date=None):
        """
        Get all appointments for a specific doctor
        
        Args:
            doctor_name (str): Doctor name
            date (str, optional): Date in format YYYY-MM-DD. Defaults to None.
            
        Returns:
            pandas.DataFrame: DataFrame containing appointments for the doctor
        """
        return self.excel_handler.get_appointments_for_doctor(doctor_name, date)
    
    def print_reception_slip(self, patient_data):
        """
        Generate and print a reception slip for a patient
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        return self.print_handler.print_reception_slip(patient_data)