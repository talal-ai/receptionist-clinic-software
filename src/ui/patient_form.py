#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Patient Form for the Receptionist Application
Provides a form for editing patient data
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

logger = logging.getLogger('receptionist.patient_form')

class PatientForm:
    """
    Patient Form class for the Receptionist Application
    Provides a form for editing patient data
    """
    
    def __init__(self, parent, settings, patient_model, on_save_callback=None, on_print_callback=None):
        """
        Initialize the Patient Form
        
        Args:
            parent: Parent widget
            settings: Application settings
            patient_model: Patient model
            on_save_callback: Callback function when a patient is saved
            on_print_callback: Callback function when a patient reception slip is printed
        """
        self.parent = parent
        self.settings = settings
        self.patient_model = patient_model
        self.on_save_callback = on_save_callback
        self.on_print_callback = on_print_callback
        
        # Current patient data
        self.current_patient = None
        
        # Create the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface"""
        # Create the main frame
        self.frame = ttk.LabelFrame(self.parent, text="Patient Information")
        
        # Configure the frame grid
        self.frame.columnconfigure(0, weight=0)  # Labels
        self.frame.columnconfigure(1, weight=1)  # Inputs
        self.frame.columnconfigure(2, weight=0)  # Additional labels
        self.frame.columnconfigure(3, weight=1)  # Additional inputs
        
        # Personal Information Section
        row = 0
        ttk.Label(self.frame, text="Personal Information", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 5))
        
        # Patient ID
        row += 1
        ttk.Label(self.frame, text="Patient ID:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.patient_id_var = tk.StringVar()
        self.patient_id_entry = ttk.Entry(self.frame, textvariable=self.patient_id_var, state='readonly')
        self.patient_id_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # First Name
        ttk.Label(self.frame, text="First Name:").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(self.frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Last Name
        row += 1
        ttk.Label(self.frame, text="Last Name:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(self.frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Phone Number
        ttk.Label(self.frame, text="Phone Number:").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.phone_number_var = tk.StringVar()
        self.phone_number_entry = ttk.Entry(self.frame, textvariable=self.phone_number_var)
        self.phone_number_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Email
        row += 1
        ttk.Label(self.frame, text="Email:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(self.frame, textvariable=self.email_var)
        self.email_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Address Section
        row += 1
        ttk.Label(self.frame, text="Address", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 5))
        
        # Address
        row += 1
        ttk.Label(self.frame, text="Address:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.address_var = tk.StringVar()
        self.address_entry = ttk.Entry(self.frame, textvariable=self.address_var)
        self.address_entry.grid(row=row, column=1, columnspan=3, sticky='ew', padx=5, pady=2)
        
        # City
        row += 1
        ttk.Label(self.frame, text="City:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.city_var = tk.StringVar()
        self.city_entry = ttk.Entry(self.frame, textvariable=self.city_var)
        self.city_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Postal Code
        ttk.Label(self.frame, text="Postal Code:").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.postal_code_var = tk.StringVar()
        self.postal_code_entry = ttk.Entry(self.frame, textvariable=self.postal_code_var)
        self.postal_code_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Appointment Section
        row += 1
        ttk.Label(self.frame, text="Appointment", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 5))
        
        # Doctor Name
        row += 1
        ttk.Label(self.frame, text="Doctor:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.doctor_name_var = tk.StringVar()
        self.doctor_name_var.set(self.settings.get("default_doctor", "Dr. Mukarram Faiz (MBBS FCPS Medicine)"))
        
        # Get the list of doctors from settings
        doctors = self.settings.get("doctors", ["Dr. Mukarram Faiz (MBBS FCPS Medicine)"])
        if doctors:
            self.doctor_name_combo = ttk.Combobox(self.frame, textvariable=self.doctor_name_var, values=doctors)
        else:
            self.doctor_name_combo = ttk.Combobox(self.frame, textvariable=self.doctor_name_var)
        
        self.doctor_name_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Appointment Date
        ttk.Label(self.frame, text="Date:").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.appointment_date_var = tk.StringVar()
        self.appointment_date_entry = DateEntry(
            self.frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            textvariable=self.appointment_date_var
        )
        self.appointment_date_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Appointment Time
        row += 1
        ttk.Label(self.frame, text="Time:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.appointment_time_var = tk.StringVar()
        
        # Create time options in 30-minute intervals with AM/PM format only
        time_options = []
        for hour in range(24):
            # Convert to AM/PM format
            if hour == 0:
                hour_ampm = "12 AM"
            elif hour < 12:
                hour_ampm = f"{hour} AM"
            elif hour == 12:
                hour_ampm = "12 PM"
            else:
                hour_ampm = f"{hour-12} PM"
                
            # Add AM/PM format times
            time_options.append(f"{hour_ampm}:00")
            time_options.append(f"{hour_ampm}:30")
        
        # Set default time to current time rounded to nearest 30 minutes
        now = datetime.now()
        minutes = now.minute
        if minutes < 30:
            minutes = 30
        else:
            minutes = 0
            now = now.replace(hour=now.hour + 1 if now.hour < 23 else 0)
            
        # Format the time with AM/PM format only
        if now.hour == 0:
            hour_ampm = "12 AM"
        elif now.hour < 12:
            hour_ampm = f"{now.hour} AM"
        elif now.hour == 12:
            hour_ampm = "12 PM"
        else:
            hour_ampm = f"{now.hour-12} PM"
            
        formatted_time = f"{hour_ampm}:{minutes:02d}"
        self.appointment_time_var.set(formatted_time)
        
        # Create combobox for time selection
        self.appointment_time_entry = ttk.Combobox(
            self.frame, 
            textvariable=self.appointment_time_var,
            values=time_options,
            state="readonly"
        )
        self.appointment_time_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Add binding to move focus to next field when time is selected
        self.appointment_time_entry.bind("<<ComboboxSelected>>", self._on_time_selected)
        
        # Appointment Duration
        ttk.Label(self.frame, text="Duration (mins):").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.appointment_duration_var = tk.StringVar()
        self.appointment_duration_var.set(str(self.settings.get("appointment_duration_mins", 30)))
        self.appointment_duration_entry = ttk.Spinbox(
            self.frame,
            from_=5,
            to=120,
            increment=5,
            textvariable=self.appointment_duration_var
        )
        self.appointment_duration_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Fees
        row += 1
        ttk.Label(self.frame, text="Fees:").grid(row=row, column=0, sticky='e', padx=5, pady=2)
        self.fees_var = tk.StringVar()
        self.fees_entry = ttk.Entry(self.frame, textvariable=self.fees_var)
        self.fees_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Reason for Visit
        row += 1
        ttk.Label(self.frame, text="Reason for Visit:").grid(row=row, column=2, sticky='e', padx=5, pady=2)
        self.reason_for_visit_var = tk.StringVar()
        self.reason_for_visit_entry = ttk.Entry(self.frame, textvariable=self.reason_for_visit_var)
        self.reason_for_visit_entry.grid(row=row, column=3, sticky='ew', padx=5, pady=2)
        
        # Notes Section
        row += 1
        ttk.Label(self.frame, text="Notes", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=4, sticky='w', padx=5, pady=(10, 5))
        
        # Notes
        row += 1
        self.notes_text = tk.Text(self.frame, height=5, width=50)
        self.notes_text.grid(row=row, column=0, columnspan=4, sticky='nsew', padx=5, pady=2)
        
        # Add a scrollbar to the notes
        notes_scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.notes_text.yview)
        notes_scrollbar.grid(row=row, column=4, sticky='ns')
        self.notes_text['yscrollcommand'] = notes_scrollbar.set
        
        # Make the notes row expandable
        self.frame.rowconfigure(row, weight=1)
        
        # Button Section
        row += 1
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=row, column=0, columnspan=4, sticky='ew', padx=5, pady=(10, 5))
        
        # Configure button frame columns
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        button_frame.columnconfigure(2, weight=1)
        
        # Clear Button
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear)
        self.clear_button.grid(row=0, column=0, padx=5, pady=5)
        
        # Save Button
        self.save_button = ttk.Button(button_frame, text="Save", command=self.save)
        self.save_button.grid(row=0, column=1, padx=5, pady=5)
        
        # Print Button
        self.print_button = ttk.Button(button_frame, text="Print Reception Slip", command=self.print_reception_slip)
        self.print_button.grid(row=0, column=2, padx=5, pady=5)
        
        # Bind validation events
        self._bind_validation_events()
    
    def _bind_validation_events(self):
        """Bind validation events to form fields"""
        # Phone number validation
        self.phone_number_entry.bind("<FocusOut>", self._validate_phone_number)
        
        # Email validation
        self.email_entry.bind("<FocusOut>", self._validate_email)
    
    def _validate_phone_number(self, event=None):
        """Validate phone number"""
        phone = self.phone_number_var.get().strip()
        if phone:
            # Simple validation - ensure it contains only digits, spaces, dashes, parentheses
            if not all(c.isdigit() or c in ' -()' for c in phone):
                messagebox.showwarning("Invalid Phone Number", 
                                       "Phone number should contain only digits, spaces, dashes, and parentheses.")
                self.phone_number_entry.focus()
    
    def _validate_email(self, event=None):
        """Validate email"""
        email = self.email_var.get().strip()
        if email:
            # Simple validation - ensure it contains @ and at least one dot after @
            if '@' not in email or '.' not in email.split('@')[1]:
                messagebox.showwarning("Invalid Email", 
                                       "Email should be in the format user@domain.com")
                self.email_entry.focus()
    
    def _on_time_selected(self, event):
        """Handle time selection from combobox"""
        # Move focus to the appointment duration field
        self.appointment_duration_entry.focus()
    
    def clear(self):
        """Clear the form"""
        # Clear all form fields
        self.patient_id_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_number_var.set("")
        self.email_var.set("")
        self.address_var.set("")
        self.city_var.set("")
        self.postal_code_var.set("")
        
        # Set default doctor
        self.doctor_name_var.set(self.settings.get("default_doctor", "Dr. Mukarram Faiz (MBBS FCPS Medicine)"))
        
        # Set default time to current time rounded to nearest 30 minutes
        now = datetime.now()
        minutes = now.minute
        if minutes < 30:
            minutes = 30
        else:
            minutes = 0
            now = now.replace(hour=now.hour + 1 if now.hour < 23 else 0)
            
        # Format the time with AM/PM format only
        if now.hour == 0:
            hour_ampm = "12 AM"
        elif now.hour < 12:
            hour_ampm = f"{now.hour} AM"
        elif now.hour == 12:
            hour_ampm = "12 PM"
        else:
            hour_ampm = f"{now.hour-12} PM"
            
        formatted_time = f"{hour_ampm}:{minutes:02d}"
        self.appointment_time_var.set(formatted_time)
        
        self.appointment_duration_var.set(str(self.settings.get("appointment_duration_mins", 30)))
        self.fees_var.set("")
        self.reason_for_visit_var.set("")
        self.notes_text.delete(1.0, tk.END)
        
        # Set today's date
        self.appointment_date_entry.set_date(datetime.now())
        
        # Reset current patient
        self.current_patient = None
    
    def set_default_appointment(self, dt):
        """
        Set default appointment date and time
        
        Args:
            dt (datetime): Date and time
        """
        # Set the date
        self.appointment_date_entry.set_date(dt)
        
        # Set the time (rounded to nearest half hour)
        minutes = dt.minute
        if minutes < 30:
            minutes = 30
        else:
            minutes = 0
            dt = dt.replace(hour=dt.hour + 1 if dt.hour < 23 else 0)
        
        # Format the time with AM/PM format only
        if dt.hour == 0:
            hour_ampm = "12 AM"
        elif dt.hour < 12:
            hour_ampm = f"{dt.hour} AM"
        elif dt.hour == 12:
            hour_ampm = "12 PM"
        else:
            hour_ampm = f"{dt.hour-12} PM"
            
        formatted_time = f"{hour_ampm}:{minutes:02d}"
        self.appointment_time_var.set(formatted_time)
    
    def load_patient(self, patient_data):
        """
        Load patient data into the form
        
        Args:
            patient_data (dict): Patient data
        """
        if patient_data is None:
            self.clear()
            return
        
        # Store the current patient
        self.current_patient = patient_data
        
        # Load data into form fields
        self.patient_id_var.set(patient_data.get('patient_id', ''))
        self.first_name_var.set(patient_data.get('first_name', ''))
        self.last_name_var.set(patient_data.get('last_name', ''))
        self.phone_number_var.set(patient_data.get('phone_number', ''))
        self.email_var.set(patient_data.get('email', ''))
        self.address_var.set(patient_data.get('address', ''))
        self.city_var.set(patient_data.get('city', ''))
        self.postal_code_var.set(patient_data.get('postal_code', ''))
        self.doctor_name_var.set(patient_data.get('doctor_name', ''))
        self.fees_var.set(patient_data.get('fees', ''))
        
        # Set appointment date
        appointment_date = patient_data.get('appointment_date', '')
        if appointment_date:
            try:
                date_obj = datetime.strptime(appointment_date, '%Y-%m-%d')
                self.appointment_date_entry.set_date(date_obj)
            except ValueError:
                # If the date is invalid, set to today
                self.appointment_date_entry.set_date(datetime.now())
        else:
            # If no date, set to today
            self.appointment_date_entry.set_date(datetime.now())
        
        # Set appointment time
        appointment_time = patient_data.get('appointment_time', '')
        if appointment_time:
            # Try to find the time in the dropdown values
            found = False
            
            # If it's in 24-hour format (HH:MM), convert to AM/PM
            if ':' in appointment_time and len(appointment_time) <= 5:
                try:
                    hour, minute = map(int, appointment_time.split(':'))
                    
                    # Convert to AM/PM format
                    if hour == 0:
                        hour_ampm = "12 AM"
                    elif hour < 12:
                        hour_ampm = f"{hour} AM"
                    elif hour == 12:
                        hour_ampm = "12 PM"
                    else:
                        hour_ampm = f"{hour-12} PM"
                        
                    am_pm_time = f"{hour_ampm}:{minute:02d}"
                    
                    # Check if this time is in our dropdown options
                    if am_pm_time in self.appointment_time_entry['values']:
                        self.appointment_time_var.set(am_pm_time)
                        found = True
                except:
                    pass
            
            # If not found yet, try direct match with dropdown values
            if not found:
                for option in self.appointment_time_entry['values']:
                    if appointment_time in option:
                        self.appointment_time_var.set(option)
                        found = True
                        break
        
        # If no valid time was found or set, use the default
        if not appointment_time or not found:
            # Set default time to current time rounded to nearest 30 minutes
            now = datetime.now()
            minutes = now.minute
            if minutes < 30:
                minutes = 30
            else:
                minutes = 0
                now = now.replace(hour=now.hour + 1 if now.hour < 23 else 0)
                
            # Format the time with AM/PM format only
            if now.hour == 0:
                hour_ampm = "12 AM"
            elif now.hour < 12:
                hour_ampm = f"{now.hour} AM"
            elif now.hour == 12:
                hour_ampm = "12 PM"
            else:
                hour_ampm = f"{now.hour-12} PM"
                
            formatted_time = f"{hour_ampm}:{minutes:02d}"
            self.appointment_time_var.set(formatted_time)
        
        self.appointment_duration_var.set(
            str(patient_data.get('appointment_duration', self.settings.get("appointment_duration_mins", 30)))
        )
        self.reason_for_visit_var.set(patient_data.get('reason_for_visit', ''))
        
        # Set notes
        self.notes_text.delete(1.0, tk.END)
        if 'notes' in patient_data and patient_data['notes']:
            self.notes_text.insert(tk.END, patient_data['notes'])
    
    def get_form_data(self):
        """
        Get the form data
        
        Returns:
            dict: Form data
        """
        # Get notes from text widget
        notes = self.notes_text.get(1.0, tk.END).strip()
        
        # Convert AM/PM time format to 24-hour format for storage
        appointment_time = self.appointment_time_var.get().strip()
        if appointment_time:
            try:
                # Parse the AM/PM time
                time_parts = appointment_time.split(':')
                if len(time_parts) == 2:
                    hour_part = time_parts[0]
                    minute_part = time_parts[1]
                    
                    # Handle hour conversion
                    hour = 0
                    if "AM" in hour_part:
                        hour_str = hour_part.replace("AM", "").strip()
                        hour = int(hour_str)
                        # Convert 12 AM to 0
                        if hour == 12:
                            hour = 0
                    elif "PM" in hour_part:
                        hour_str = hour_part.replace("PM", "").strip()
                        hour = int(hour_str)
                        # Convert PM hours (except 12 PM)
                        if hour != 12:
                            hour += 12
                    
                    # Get minutes
                    minute = int(minute_part)
                    
                    # Format as 24-hour time
                    appointment_time = f"{hour:02d}:{minute:02d}"
            except:
                # If parsing fails, keep the original time
                pass
        
        # Build the form data
        form_data = {
            'patient_id': self.patient_id_var.get().strip(),
            'first_name': self.first_name_var.get().strip(),
            'last_name': self.last_name_var.get().strip(),
            'phone_number': self.phone_number_var.get().strip(),
            'email': self.email_var.get().strip(),
            'address': self.address_var.get().strip(),
            'city': self.city_var.get().strip(),
            'postal_code': self.postal_code_var.get().strip(),
            'doctor_name': self.doctor_name_var.get().strip(),
            'appointment_date': self.appointment_date_var.get().strip(),
            'appointment_time': appointment_time,
            'appointment_duration': self.appointment_duration_var.get().strip(),
            'fees': self.fees_var.get().strip(),
            'reason_for_visit': self.reason_for_visit_var.get().strip(),
            'notes': notes
        }
        
        return form_data
    
    def validate_form(self):
        """
        Validate the form
        
        Returns:
            bool: True if valid, False otherwise
        """
        # No required fields - all fields are optional now
        
        # Validate phone number if provided
        if self.phone_number_var.get().strip():
            self._validate_phone_number()
        
        # Validate email if provided
        if self.email_var.get().strip():
            self._validate_email()
        
        return True
    
    def save(self):
        """Save the patient data"""
        # Validate the form
        if not self.validate_form():
            return
        
        # Get the form data
        form_data = self.get_form_data()
        
        # Ensure empty fields are handled correctly
        for key, value in form_data.items():
            if value is None or value == 'nan' or value == 'NaN':
                form_data[key] = ''
        
        try:
            if self.current_patient and self.current_patient.get('patient_id'):
                # Update existing patient
                patient_id = self.current_patient.get('patient_id')
                success = self.patient_model.update_patient(patient_id, form_data)
                
                if success:
                    messagebox.showinfo("Success", "Patient updated successfully.")
                    logger.info(f"Updated patient: {patient_id}")
                    
                    # Call the callback if provided
                    if self.on_save_callback:
                        self.on_save_callback(form_data)
                else:
                    messagebox.showerror("Error", "Failed to update patient.")
            else:
                # Add new patient
                success = self.patient_model.add_patient(form_data)
                
                if success:
                    messagebox.showinfo("Success", "Patient added successfully.")
                    logger.info(f"Added new patient: {form_data.get('patient_id')}")
                    
                    # Load the patient data to get the assigned ID
                    self.load_patient(self.patient_model.get_patient_by_id(form_data.get('patient_id')))
                    
                    # Call the callback if provided
                    if self.on_save_callback:
                        self.on_save_callback(form_data)
                else:
                    messagebox.showerror("Error", "Failed to add patient.")
        except Exception as e:
            logger.error(f"Error saving patient: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")
    
    def print_reception_slip(self):
        """Print a reception slip for the current patient"""
        # Make sure we have a patient ID or at least allow printing without saving first
        if not self.current_patient and not self.patient_id_var.get():
            # Proceed anyway but warn the user
            response = messagebox.askyesno(
                "Warning", 
                "The patient data has not been saved. Do you want to print anyway?"
            )
            if not response:
                return
        
        try:
            # Get the current form data
            form_data = self.get_form_data()
            
            # Ensure empty fields are handled correctly
            for key, value in form_data.items():
                if value is None or value == 'nan' or value == 'NaN':
                    form_data[key] = ''
            
            # Print the reception slip
            success = self.patient_model.print_reception_slip(form_data)
            
            if success:
                # Call the callback if provided
                if self.on_print_callback:
                    self.on_print_callback(form_data)
            else:
                messagebox.showerror("Error", "Failed to print reception slip.")
        except Exception as e:
            logger.error(f"Error printing reception slip: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")