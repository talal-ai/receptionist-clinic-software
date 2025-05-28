#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Appointment View for the Receptionist Application
Displays appointments for a specific date
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkcalendar import DateEntry

logger = logging.getLogger('receptionist.appointment_view')

class AppointmentView:
    """
    Appointment View class for the Receptionist Application
    Displays appointments for a specific date
    """
    
    def __init__(self, parent, patient_model, on_patient_selected=None):
        """
        Initialize the Appointment View
        
        Args:
            parent: Parent widget
            patient_model: Patient model
            on_patient_selected: Callback function when a patient is selected
        """
        self.parent = parent
        self.patient_model = patient_model
        self.on_patient_selected = on_patient_selected
        
        # Current date
        self.current_date = datetime.now().strftime('%Y-%m-%d')
        
        # Create the UI
        self._create_ui()
    
    def _create_ui(self):
        """Create the user interface"""
        # Create the main frame
        self.frame = ttk.LabelFrame(self.parent, text="Appointments")
        
        # Configure the frame grid
        self.frame.columnconfigure(0, weight=0)  # Label
        self.frame.columnconfigure(1, weight=1)  # Date entry
        self.frame.columnconfigure(2, weight=0)  # Refresh button
        self.frame.rowconfigure(1, weight=1)  # Appointments tree
        
        # Date selection row
        ttk.Label(self.frame, text="Date:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        
        self.date_var = tk.StringVar()
        self.date_var.set(self.current_date)
        
        self.date_entry = DateEntry(
            self.frame,
            width=12,
            background='darkblue',
            foreground='white',
            borderwidth=2,
            date_pattern='yyyy-mm-dd',
            textvariable=self.date_var
        )
        self.date_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        # Bind date change event
        self.date_entry.bind("<<DateEntrySelected>>", self._on_date_changed)
        
        # Refresh button
        self.refresh_button = ttk.Button(self.frame, text="Refresh", command=self.refresh)
        self.refresh_button.grid(row=0, column=2, sticky='e', padx=5, pady=5)
        
        # Create the appointments treeview
        self.appointments_tree = ttk.Treeview(
            self.frame,
            columns=("Time", "Patient", "Doctor", "Duration", "Fees", "Reason"),
            show="headings"
        )
        
        # Define the columns
        self.appointments_tree.heading("Time", text="Time")
        self.appointments_tree.heading("Patient", text="Patient")
        self.appointments_tree.heading("Doctor", text="Doctor")
        self.appointments_tree.heading("Duration", text="Duration")
        self.appointments_tree.heading("Fees", text="Fees")
        self.appointments_tree.heading("Reason", text="Reason for Visit")
        
        # Configure column widths
        self.appointments_tree.column("Time", width=50)
        self.appointments_tree.column("Patient", width=150)
        self.appointments_tree.column("Doctor", width=100)
        self.appointments_tree.column("Duration", width=60)
        self.appointments_tree.column("Fees", width=60)
        self.appointments_tree.column("Reason", width=150)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.appointments_tree.yview)
        self.appointments_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.appointments_tree.grid(row=1, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)
        scrollbar.grid(row=1, column=3, sticky='ns')
        
        # Add delete button
        self.delete_button = ttk.Button(self.frame, text="Delete Selected Patient", command=self._on_delete_selected)
        self.delete_button.grid(row=2, column=0, columnspan=3, sticky='e', padx=5, pady=5)
        
        # Bind selection event
        self.appointments_tree.bind("<<TreeviewSelect>>", self._on_appointment_selected)
        
        # Load today's appointments
        self.show_appointments_for_date(self.current_date)
    
    def _on_date_changed(self, event):
        """
        Handle date change event
        
        Args:
            event: DateEntry selection event
        """
        # Update the current date
        self.current_date = self.date_var.get()
        
        # Show appointments for the selected date
        self.show_appointments_for_date(self.current_date)
    
    def _on_appointment_selected(self, event):
        """
        Handle selection of an appointment
        
        Args:
            event: Treeview selection event
        """
        # Get the selected item
        selection = self.appointments_tree.selection()
        
        if not selection:
            return
        
        # Get the patient ID from the selected item's tags
        item = self.appointments_tree.item(selection[0])
        tags = item['tags']
        
        if tags and len(tags) > 0:
            patient_id = tags[0]
            
            # Get the patient data
            patient_data = self.patient_model.get_patient_by_id(patient_id)
            
            # Call the callback if provided
            if self.on_patient_selected and patient_data:
                self.on_patient_selected(patient_data)
    
    def _on_delete_selected(self):
        """Handle delete button click"""
        selection = self.appointments_tree.selection()
        
        if not selection:
            messagebox.showinfo("Selection Required", "Please select an appointment to delete.")
            return
        
        # Get the patient ID from the selected item's tags
        item = self.appointments_tree.item(selection[0])
        tags = item['tags']
        
        if tags and len(tags) > 0:
            patient_id = tags[0]
            patient_name = item['values'][1]  # Patient name is in the second column
            
            # Confirm deletion
            confirm = messagebox.askyesno(
                "Confirm Deletion",
                f"Are you sure you want to delete patient {patient_name} (ID: {patient_id})?\n\n"
                "This action cannot be undone."
            )
            
            if confirm:
                # Delete the patient
                success = self.patient_model.delete_patient(patient_id)
                
                if success:
                    messagebox.showinfo("Success", f"Patient {patient_name} has been deleted.")
                    # Refresh the appointments
                    self.refresh()
                else:
                    messagebox.showerror("Error", f"Failed to delete patient {patient_name}.")
    
    def refresh(self):
        """Refresh the appointments view"""
        self.show_appointments_for_date(self.current_date)
    
    def show_appointments_for_date(self, date):
        """
        Show appointments for a specific date
        
        Args:
            date (str): Date in format YYYY-MM-DD
        """
        # Update the current date
        self.current_date = date
        self.date_var.set(date)
        
        # Clear the treeview
        for item in self.appointments_tree.get_children():
            self.appointments_tree.delete(item)
        
        # Get appointments for the date
        appointments = self.patient_model.get_appointments_for_date(date)
        
        # Sort by time
        appointments = appointments.sort_values('appointment_time')
        
        # Add the appointments to the treeview
        for _, appointment in appointments.iterrows():
            # Get patient name
            patient_name = f"{appointment.get('first_name', '')} {appointment.get('last_name', '')}"
            
            # Get appointment time
            appointment_time = appointment.get('appointment_time', '')
            
            # Get appointment duration
            appointment_duration = appointment.get('appointment_duration', '')
            
            # Format fees
            fees = appointment.get('fees', '')
            if fees:
                fees = f"PKR {fees}"
            
            # Insert the appointment
            self.appointments_tree.insert(
                "",
                "end",
                values=(
                    appointment_time,
                    patient_name,
                    appointment.get('doctor_name', ''),
                    f"{appointment_duration} min",
                    fees,
                    appointment.get('reason_for_visit', '')
                ),
                tags=(appointment.get('patient_id', ''),)
            )