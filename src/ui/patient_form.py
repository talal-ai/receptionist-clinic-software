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
import pandas as pd

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
        
        # Configure the frame grid - now only need 2 columns for label and input
        self.frame.columnconfigure(0, weight=0)  # Labels
        self.frame.columnconfigure(1, weight=1)  # Inputs
        
        # Personal Information Section
        row = 0
        ttk.Label(self.frame, text="Personal Information", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))
        
        # Patient ID
        row += 1
        ttk.Label(self.frame, text="Patient ID:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.patient_id_var = tk.StringVar()
        self.patient_id_entry = ttk.Entry(self.frame, textvariable=self.patient_id_var, state='readonly')
        self.patient_id_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Token Number
        row += 1
        ttk.Label(self.frame, text="Token Number:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.token_number_var = tk.StringVar()
        self.token_number_entry = ttk.Entry(self.frame, textvariable=self.token_number_var)
        self.token_number_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # First Name
        row += 1
        ttk.Label(self.frame, text="First Name:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(self.frame, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Last Name
        row += 1
        ttk.Label(self.frame, text="Last Name:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(self.frame, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Appointment Section
        row += 1
        ttk.Label(self.frame, text="Appointment", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))
        
        # Status (New/Old)
        row += 1
        ttk.Label(self.frame, text="Status:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.status_var = tk.StringVar()
        self.status_var.set("New")  # Default to New
        self.status_combo = ttk.Combobox(
            self.frame, 
            textvariable=self.status_var,
            values=["New", "Old"],
            state="readonly"
        )
        self.status_combo.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Doctor Name
        row += 1
        ttk.Label(self.frame, text="Doctor:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.doctor_name_var = tk.StringVar()
        self.doctor_name_var.set("Dr. Muhammad Sajid Sohail")
        self.doctor_name_entry = ttk.Entry(self.frame, textvariable=self.doctor_name_var, state='readonly')
        self.doctor_name_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Appointment Date
        row += 1
        ttk.Label(self.frame, text="Date:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.appointment_date_var = tk.StringVar()
        self.appointment_date_entry = DateEntry(
            self.frame,
            width=20,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            textvariable=self.appointment_date_var
        )
        self.appointment_date_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Arrival Time
        row += 1
        ttk.Label(self.frame, text="Arrival Time:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.arrival_time_var = tk.StringVar()
        
        # Set default time to current time with exact minutes
        self.update_arrival_time()
        
        # Create entry for arrival time (read-only)
        self.arrival_time_entry = ttk.Entry(
            self.frame, 
            textvariable=self.arrival_time_var,
            state="readonly"
        )
        self.arrival_time_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Start a timer to update the arrival time every second
        self._update_arrival_time_job = self.frame.after(1000, self._update_arrival_time_timer)
        
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
        
        # Checkup Time
        row += 1
        ttk.Label(self.frame, text="Checkup Time:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.appointment_time_var = tk.StringVar()
        
        # Create combobox for checkup time selection
        self.appointment_time_entry = ttk.Combobox(
            self.frame, 
            textvariable=self.appointment_time_var,
            values=time_options,
            state="readonly"
        )
        self.appointment_time_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Set default checkup time (rounded to next 30 minutes)
        self.set_default_checkup_time()
        
        # Fees
        row += 1
        ttk.Label(self.frame, text="Fees:").grid(row=row, column=0, sticky='w', padx=5, pady=2)
        self.fees_var = tk.StringVar()
        self.fees_entry = ttk.Entry(self.frame, textvariable=self.fees_var)
        self.fees_entry.grid(row=row, column=1, sticky='ew', padx=5, pady=2)
        
        # Remarks Section
        row += 1
        ttk.Label(self.frame, text="Remarks", font=("TkDefaultFont", 10, "bold")).grid(
            row=row, column=0, columnspan=2, sticky='w', padx=5, pady=(10, 5))
        
        # Remarks
        row += 1
        self.remarks_text = tk.Text(self.frame, height=5, width=50)
        self.remarks_text.grid(row=row, column=0, columnspan=2, sticky='nsew', padx=5, pady=2)
        
        # Add a scrollbar to the remarks
        remarks_scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.remarks_text.yview)
        remarks_scrollbar.grid(row=row, column=2, sticky='ns')
        self.remarks_text['yscrollcommand'] = remarks_scrollbar.set
        
        # Make the remarks row expandable
        self.frame.rowconfigure(row, weight=1)
        
        # Button Section
        row += 1
        button_frame = ttk.Frame(self.frame)
        button_frame.grid(row=row, column=0, columnspan=2, sticky='ew', padx=5, pady=(10, 5))
        
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
    
    def _on_time_selected(self, event):
        """Handle checkup time selection from combobox"""
        # Move focus to the appointment duration field
        self.appointment_duration_entry.focus()
    
    def clear(self):
        """Clear the form"""
        # Clear all form fields
        self.patient_id_var.set("")
        # Set the next token number for today
        self.set_next_token_number()
        self.first_name_var.set("")
        self.last_name_var.set("")
        
        # Always set the default doctor name
        self.doctor_name_var.set("Dr. Muhammad Sajid Sohail")
        
        # Set default status to New
        self.status_var.set("New")
        
        # Update arrival time to current time
        self.update_arrival_time()
        
        # Set default checkup time (rounded to next 30 minutes)
        self.set_default_checkup_time()
        
        self.fees_var.set("")
        self.remarks_text.delete(1.0, tk.END)
        
        # Set today's date
        self.appointment_date_entry.set_date(datetime.now())
        
        # Reset current patient
        self.current_patient = None
    
    def set_default_appointment(self, dt):
        """
        Set default appointment date and checkup time
        
        Args:
            dt (datetime): Date and time
        """
        # Set the date
        self.appointment_date_entry.set_date(dt)
        
        # Update arrival time to current time
        self.update_arrival_time()
        
        # Set the checkup time (rounded to nearest half hour)
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
        self.appointment_time_var.set(formatted_time)  # Checkup time
    
    def set_next_token_number(self):
        """
        Set the next token number for today's date
        """
        try:
            # Get today's date
            today = datetime.now().strftime('%Y-%m-%d')
            
            # Get today's appointments
            today_appointments = self.patient_model.get_appointments_for_date(today)
            
            # Find the highest token number
            if not today_appointments.empty and 'token_number' in today_appointments.columns:
                # Convert to numeric, ignoring errors
                today_appointments['token_number_numeric'] = pd.to_numeric(today_appointments['token_number'], errors='coerce')
                # Get the maximum, defaulting to 0 if all are NaN
                current_max = today_appointments['token_number_numeric'].max()
                # If max is NaN, start from 0
                if pd.isna(current_max):
                    current_max = 0
                # Set the next token number
                next_token = int(current_max) + 1
            else:
                # Start from 1 if no appointments today
                next_token = 1
            
            # Set the token number
            self.token_number_var.set(str(next_token))
            logger.info(f"Set next token number to {next_token} for date {today}")
            
        except Exception as e:
            logger.error(f"Error setting next token number: {e}")
            # Default to empty if there's an error
            self.token_number_var.set("")
    
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
        self.token_number_var.set(patient_data.get('token_number', ''))
        self.first_name_var.set(patient_data.get('first_name', ''))
        self.last_name_var.set(patient_data.get('last_name', ''))
        self.doctor_name_var.set(patient_data.get('doctor_name', ''))
        self.fees_var.set(patient_data.get('fees', ''))
        
        # Set status (New/Old)
        status = patient_data.get('status', '')
        if status and status in ["New", "Old"]:
            self.status_var.set(status)
        else:
            self.status_var.set("New")  # Default to New if not set or invalid
        
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
        
        # Set checkup time (stored as appointment_time)
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
            # Set default checkup time
            self.set_default_checkup_time()
        
        # For arrival time, always use the current time
        self.update_arrival_time()
        
        # Set remarks
        self.remarks_text.delete(1.0, tk.END)
        if 'remarks' in patient_data and patient_data['remarks']:
            self.remarks_text.insert(tk.END, patient_data['remarks'])
        # For backward compatibility with old data
        elif 'notes' in patient_data and patient_data['notes']:
            self.remarks_text.insert(tk.END, patient_data['notes'])
    
    def get_form_data(self):
        """
        Get the form data
        
        Returns:
            dict: Form data
        """
        # Get remarks from text widget
        remarks = self.remarks_text.get(1.0, tk.END).strip()
        
        # Update arrival time to current time before getting form data
        self.update_arrival_time()
        
        # Convert AM/PM checkup time format to 24-hour format for storage
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
        
        # Convert AM/PM arrival time format to 24-hour format for storage
        arrival_time = self.arrival_time_var.get().strip()
        if arrival_time:
            try:
                # Parse the AM/PM time
                time_parts = arrival_time.split(':')
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
                    arrival_time = f"{hour:02d}:{minute:02d}"
            except:
                # If parsing fails, keep the original time
                pass
        
        # Build the form data
        form_data = {
            'patient_id': self.patient_id_var.get().strip(),
            'token_number': self.token_number_var.get().strip(),
            'first_name': self.first_name_var.get().strip(),
            'last_name': self.last_name_var.get().strip(),
            'doctor_name': self.doctor_name_var.get().strip(),
            'status': self.status_var.get().strip(),
            'appointment_date': self.appointment_date_var.get().strip(),
            'appointment_time': appointment_time,
            'arrival_time': arrival_time,
            'fees': self.fees_var.get().strip(),
            'remarks': remarks
        }
        
        return form_data
    
    def get_patient_data(self):
        """
        Get the current patient data from the form fields.
        This is an alias for get_form_data to be used by external callers.
        """
        return self.get_form_data()
    
    def validate_form(self):
        """
        Validate the form
        
        Returns:
            bool: True if valid, False otherwise
        """
        # No required fields - all fields are optional now
        
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
                    
                    # Set the next token number for the next patient
                    self.set_next_token_number()
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
            # Update arrival time to current time before printing
            self.update_arrival_time()
            
            # Get the current form data
            form_data = self.get_form_data()
            
            # Ensure empty fields are handled correctly
            for key, value in form_data.items():
                if value is None or value == 'nan' or value == 'NaN':
                    form_data[key] = ''
            
            # Print the reception slip
            success = self.patient_model.print_reception_slip(form_data)
            
            if success:
                # Show success message
                patient_name = f"{form_data.get('first_name', '')} {form_data.get('last_name', '')}"
                messagebox.showinfo("Print Successful", 
                                  f"Reception slip for {patient_name} has been sent to the printer.")
                
                # Call the callback if provided
                if self.on_print_callback:
                    self.on_print_callback(form_data)
                    
                # If this was a new patient (not saved yet), set the next token number
                if not self.current_patient or not self.current_patient.get('patient_id'):
                    # After printing, automatically set the next token number
                    self.set_next_token_number()
                    messagebox.showinfo("Token Number Updated", 
                                      f"Token number has been updated to {self.token_number_var.get()} for the next patient.")
            else:
                messagebox.showerror("Error", "Failed to print reception slip.")
        except Exception as e:
            logger.error(f"Error printing reception slip: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def update_arrival_time(self):
        """Update the arrival time to the current time"""
        now = datetime.now()
        
        # Format the time with AM/PM format and exact minutes
        if now.hour == 0:
            hour_ampm = "12 AM"
        elif now.hour < 12:
            hour_ampm = f"{now.hour} AM"
        elif now.hour == 12:
            hour_ampm = "12 PM"
        else:
            hour_ampm = f"{now.hour-12} PM"
            
        formatted_time = f"{hour_ampm}:{now.minute:02d}"
        self.arrival_time_var.set(formatted_time)
    
    def _update_arrival_time_timer(self):
        """Timer function to update the arrival time every second"""
        self.update_arrival_time()
        # Schedule the next update in 1 second
        self._update_arrival_time_job = self.frame.after(1000, self._update_arrival_time_timer)
    
    def set_default_checkup_time(self):
        """Set the default checkup time (rounded to next 30 minutes)"""
        now = datetime.now()
        checkup_minutes = now.minute
        checkup_hour = now.hour
        
        if checkup_minutes < 30:
            checkup_minutes = 30
        else:
            checkup_minutes = 0
            checkup_hour = now.hour + 1 if now.hour < 23 else 0
            
        # Format the checkup time
        if checkup_hour == 0:
            checkup_hour_ampm = "12 AM"
        elif checkup_hour < 12:
            checkup_hour_ampm = f"{checkup_hour} AM"
        elif checkup_hour == 12:
            checkup_hour_ampm = "12 PM"
        else:
            checkup_hour_ampm = f"{checkup_hour-12} PM"
            
        checkup_formatted_time = f"{checkup_hour_ampm}:{checkup_minutes:02d}"
        self.appointment_time_var.set(checkup_formatted_time)

    def cleanup(self):
        """Clean up resources when the form is closed"""
        # Cancel the timer if it's running
        if hasattr(self, '_update_arrival_time_job') and self._update_arrival_time_job:
            self.frame.after_cancel(self._update_arrival_time_job)
            self._update_arrival_time_job = None