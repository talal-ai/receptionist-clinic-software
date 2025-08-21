#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Settings Dialog for the Receptionist Application
Provides a dialog for editing application settings
"""

import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import logging

logger = logging.getLogger('receptionist.settings_dialog')

class SettingsDialog:
    """
    Settings Dialog class for the Receptionist Application
    Provides a dialog for editing application settings
    """
    
    def __init__(self, parent, settings, callback=None):
        """
        Initialize the Settings Dialog
        
        Args:
            parent: Parent widget
            settings: Application settings
            callback: Callback function when settings are saved
        """
        self.parent = parent
        self.settings = settings
        self.callback = callback
        
        # Create the dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Settings")
        self.dialog.geometry("650x550")
        self.dialog.minsize(600, 500)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.focus_set()
        
        # Variables to store settings
        self.app_name_var = tk.StringVar(value=settings.get("app_name", "Clinic Receptionist"))
        self.company_name_var = tk.StringVar(value=settings.get("company_name", ""))
        self.clinic_address_var = tk.StringVar(value=settings.get("clinic_address", ""))
        self.clinic_phone_var = tk.StringVar(value=settings.get("clinic_phone", ""))
        self.data_path_var = tk.StringVar(value=settings.get("data_path", "./data"))
        self.excel_file_var = tk.StringVar(value=settings.get("excel_file", "patients.xlsx"))
        self.backup_interval_var = tk.StringVar(value=str(settings.get("backup_interval_days", 7)))
        self.auto_backup_var = tk.BooleanVar(value=settings.get("auto_backup", True))
        self.logo_path_var = tk.StringVar(value=settings.get("logo_path", ""))
        self.appointment_duration_var = tk.StringVar(value=str(settings.get("appointment_duration_mins", 30)))
        
        # Create doctor list with a text widget to allow multiline input
        self.doctors_text = None  # Will be initialized in _create_ui
        
        # Create the UI
        self._create_ui()
        
        # Center the dialog
        self._center_window()
        
    def _center_window(self):
        """Center the dialog on the screen"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def _create_ui(self):
        """Create the user interface"""
        # Create a notebook for tabs
        notebook = ttk.Notebook(self.dialog)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        self._create_general_tab(general_frame)
        
        # Clinic settings tab
        clinic_frame = ttk.Frame(notebook)
        notebook.add(clinic_frame, text="Clinic")
        self._create_clinic_tab(clinic_frame)
        
        # Doctors tab
        doctors_frame = ttk.Frame(notebook)
        notebook.add(doctors_frame, text="Doctors")
        self._create_doctors_tab(doctors_frame)
        
        # Data settings tab
        data_frame = ttk.Frame(notebook)
        notebook.add(data_frame, text="Data")
        self._create_data_tab(data_frame)
        
        # Button frame
        button_frame = ttk.Frame(self.dialog)
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Save button
        save_button = ttk.Button(button_frame, text="Save", command=self._on_save)
        save_button.pack(side=tk.RIGHT, padx=5)
        
        # Cancel button
        cancel_button = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        cancel_button.pack(side=tk.RIGHT, padx=5)
    
    def _create_general_tab(self, parent):
        """Create the general settings tab"""
        # Use a frame with padding
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        
        # Application Name
        row = 0
        ttk.Label(frame, text="Application Name:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        app_name_entry = ttk.Entry(frame, textvariable=self.app_name_var)
        app_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        # Appointment Duration
        row += 1
        ttk.Label(frame, text="Default Appointment Duration (mins):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        appointment_duration_entry = ttk.Spinbox(
            frame, 
            from_=5, 
            to=120, 
            increment=5,
            textvariable=self.appointment_duration_var
        )
        appointment_duration_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
    
    def _create_clinic_tab(self, parent):
        """Create the clinic settings tab"""
        # Use a frame with padding
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        
        # Clinic Name
        row = 0
        ttk.Label(frame, text="Clinic Name:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        company_name_entry = ttk.Entry(frame, textvariable=self.company_name_var)
        company_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        # Clinic Address
        row += 1
        ttk.Label(frame, text="Clinic Address:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        clinic_address_entry = ttk.Entry(frame, textvariable=self.clinic_address_var)
        clinic_address_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        # Clinic Phone
        row += 1
        ttk.Label(frame, text="Clinic Phone:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        clinic_phone_entry = ttk.Entry(frame, textvariable=self.clinic_phone_var)
        clinic_phone_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        # Logo Path
        row += 1
        ttk.Label(frame, text="Logo Path:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        
        # Create a frame for the logo path and browse button
        logo_frame = ttk.Frame(frame)
        logo_frame.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        logo_frame.columnconfigure(0, weight=1)
        
        logo_path_entry = ttk.Entry(logo_frame, textvariable=self.logo_path_var)
        logo_path_entry.grid(row=0, column=0, sticky='ew')
        
        browse_button = ttk.Button(logo_frame, text="Browse...", command=self._browse_logo)
        browse_button.grid(row=0, column=1, padx=(5, 0))
    
    def _create_doctors_tab(self, parent):
        """Create the doctors settings tab"""
        # Use a frame with padding
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(1, weight=1)
        
        # Instructions
        ttk.Label(frame, text="Enter each doctor's name on a new line:").grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        # Doctors list
        self.doctors_text = tk.Text(frame, height=10, width=50)
        self.doctors_text.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.doctors_text.yview)
        scrollbar.grid(row=1, column=1, sticky='ns')
        self.doctors_text['yscrollcommand'] = scrollbar.set
        
        # Load current doctors
        doctors = self.settings.get("doctors", [])
        if doctors:
            self.doctors_text.insert(tk.END, "\n".join(doctors))
    
    def _create_data_tab(self, parent):
        """Create the data settings tab"""
        # Use a frame with padding
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        frame.columnconfigure(0, weight=0)
        frame.columnconfigure(1, weight=1)
        
        # Data Path
        row = 0
        ttk.Label(frame, text="Data Directory:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        
        # Create a frame for the data path and browse button
        data_frame = ttk.Frame(frame)
        data_frame.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        data_frame.columnconfigure(0, weight=1)
        
        data_path_entry = ttk.Entry(data_frame, textvariable=self.data_path_var)
        data_path_entry.grid(row=0, column=0, sticky='ew')
        
        browse_button = ttk.Button(data_frame, text="Browse...", command=self._browse_data_path)
        browse_button.grid(row=0, column=1, padx=(5, 0))
        
        # Excel File
        row += 1
        ttk.Label(frame, text="Excel File:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        excel_file_entry = ttk.Entry(frame, textvariable=self.excel_file_var)
        excel_file_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=5)
        
        # Backup Interval
        row += 1
        ttk.Label(frame, text="Backup Interval (days):").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        backup_interval_entry = ttk.Spinbox(
            frame, 
            from_=1, 
            to=30, 
            increment=1,
            textvariable=self.backup_interval_var
        )
        backup_interval_entry.grid(row=row, column=1, sticky='w', padx=5, pady=5)
        
        # Auto Backup
        row += 1
        ttk.Label(frame, text="Auto Backup:").grid(row=row, column=0, sticky='w', padx=5, pady=5)
        auto_backup_check = ttk.Checkbutton(frame, variable=self.auto_backup_var, text="Enable automatic backups")
        auto_backup_check.grid(row=row, column=1, sticky='w', padx=5, pady=5)
    
    def _browse_logo(self):
        """Browse for logo file"""
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.gif"),
            ("All files", "*.*")
        ]
        filename = filedialog.askopenfilename(
            title="Select Logo Image",
            filetypes=filetypes
        )
        if filename:
            self.logo_path_var.set(filename)
    
    def _browse_data_path(self):
        """Browse for data directory"""
        directory = filedialog.askdirectory(
            title="Select Data Directory"
        )
        if directory:
            self.data_path_var.set(directory)
    
    def _on_save(self):
        """Save settings"""
        try:
            # Update settings with values from UI
            self.settings.set("app_name", self.app_name_var.get())
            self.settings.set("company_name", self.company_name_var.get())
            self.settings.set("clinic_address", self.clinic_address_var.get())
            self.settings.set("clinic_phone", self.clinic_phone_var.get())
            self.settings.set("data_path", self.data_path_var.get())
            self.settings.set("excel_file", self.excel_file_var.get())
            
            # Convert numeric values
            try:
                backup_interval = int(self.backup_interval_var.get())
                self.settings.set("backup_interval_days", backup_interval)
            except ValueError:
                messagebox.showerror("Error", "Backup interval must be a number")
                return
            
            try:
                appointment_duration = int(self.appointment_duration_var.get())
                self.settings.set("appointment_duration_mins", appointment_duration)
            except ValueError:
                messagebox.showerror("Error", "Appointment duration must be a number")
                return
            
            self.settings.set("auto_backup", self.auto_backup_var.get())
            self.settings.set("logo_path", self.logo_path_var.get())
            
            # Parse doctors from text widget
            doctors_text = self.doctors_text.get(1.0, tk.END).strip()
            doctors = [doctor.strip() for doctor in doctors_text.split('\n') if doctor.strip()]
            self.settings.set("doctors", doctors)
            
            # Save settings
            self.settings.save_settings()
            
            # Call callback if provided
            if self.callback:
                self.callback()
            
            # Close dialog
            self.dialog.destroy()
            
            # Show success message
            messagebox.showinfo("Settings Saved", "Settings have been saved successfully.")
            
        except Exception as e:
            logger.error(f"Error saving settings: {e}")
            messagebox.showerror("Error", f"An error occurred while saving settings: {e}") 