#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Search Panel for the Receptionist Application
Provides search functionality for patients
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox

logger = logging.getLogger('receptionist.search_panel')

class SearchPanel:
    """
    Search Panel class for the Receptionist Application
    Provides search functionality for patients
    """
    
    def __init__(self, parent, patient_model, on_patient_selected=None):
        """
        Initialize the Search Panel
        
        Args:
            parent: Parent widget
            patient_model: Patient model
            on_patient_selected: Callback function when a patient is selected
        """
        self.parent = parent
        self.patient_model = patient_model
        self.on_patient_selected = on_patient_selected
        
        # Create the UI
        self._create_ui()
        
        # Show all patients by default
        self.show_all_patients()
    
    def _create_ui(self):
        """Create the user interface"""
        # Create the main frame
        self.frame = ttk.LabelFrame(self.parent, text="Search Patients")
        
        # Configure the frame grid
        self.frame.columnconfigure(0, weight=0)  # Label
        self.frame.columnconfigure(1, weight=1)  # Search entry
        self.frame.columnconfigure(2, weight=0)  # Search button
        self.frame.columnconfigure(3, weight=0)  # Clear button
        
        # Search Row
        ttk.Label(self.frame, text="Search:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(self.frame, textvariable=self.search_var)
        self.search_entry.grid(row=0, column=1, sticky='ew', padx=5, pady=5)
        
        self.search_button = ttk.Button(self.frame, text="Search", command=self._on_search)
        self.search_button.grid(row=0, column=2, sticky='e', padx=5, pady=5)
        
        self.clear_button = ttk.Button(self.frame, text="Show All", command=self.show_all_patients)
        self.clear_button.grid(row=0, column=3, sticky='e', padx=5, pady=5)
        
        # Bind Enter key to search
        self.search_entry.bind("<Return>", lambda event: self._on_search())
        
        # Search Results
        self.results_frame = ttk.Frame(self.frame)
        self.results_frame.grid(row=1, column=0, columnspan=4, sticky='nsew', padx=5, pady=5)
        
        # Configure the results frame grid
        self.results_frame.columnconfigure(0, weight=1)
        self.results_frame.rowconfigure(0, weight=1)
        
        # Create the treeview for search results
        self.results_tree = ttk.Treeview(
            self.results_frame,
            columns=("ID", "Token", "Name", "Status", "Doctor", "Date", "Arrival", "Fees"),
            show="headings",
            height=5
        )
        
        # Define the columns
        self.results_tree.heading("ID", text="ID")
        self.results_tree.heading("Token", text="Token")
        self.results_tree.heading("Name", text="Name")
        self.results_tree.heading("Status", text="Status")
        self.results_tree.heading("Doctor", text="Doctor")
        self.results_tree.heading("Date", text="Date")
        self.results_tree.heading("Arrival", text="Arrival")
        self.results_tree.heading("Fees", text="Fees")
        
        # Configure column widths
        self.results_tree.column("ID", width=50)
        self.results_tree.column("Token", width=50)
        self.results_tree.column("Name", width=150)
        self.results_tree.column("Status", width=60)
        self.results_tree.column("Doctor", width=120)
        self.results_tree.column("Date", width=80)
        self.results_tree.column("Arrival", width=60)
        self.results_tree.column("Fees", width=60)
        
        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self.results_frame, orient="vertical", command=self.results_tree.yview)
        self.results_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        self.results_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Add the delete button
        self.delete_button = ttk.Button(self.frame, text="Delete Selected Patient", command=self._on_delete_selected)
        self.delete_button.grid(row=2, column=0, columnspan=4, sticky='e', padx=5, pady=5)
        
        # Bind selection event
        self.results_tree.bind("<<TreeviewSelect>>", self._on_result_selected)
    
    def _on_search(self):
        """Handle search button click"""
        search_text = self.search_var.get().strip()
        
        # Search for patients by name
        results = self.patient_model.search_patients_by_name(search_text)
        
        # Display the results
        self._display_results(results)
        
        # Update the results label
        if search_text:
            if len(results) == 0:
                messagebox.showinfo("Search Results", "No patients found matching your search.")
    
    def _on_result_selected(self, event):
        """
        Handle selection of a search result
        
        Args:
            event: Treeview selection event
        """
        # Get the selected item
        selection = self.results_tree.selection()
        
        if not selection:
            return
        
        # Get the patient ID from the selected item
        item = self.results_tree.item(selection[0])
        patient_id = item['values'][0]
        
        # Get the patient data
        patient_data = self.patient_model.get_patient_by_id(patient_id)
        
        # Call the callback if provided
        if self.on_patient_selected and patient_data:
            self.on_patient_selected(patient_data)
    
    def _on_delete_selected(self):
        """Handle delete button click"""
        selection = self.results_tree.selection()
        
        if not selection:
            messagebox.showinfo("Selection Required", "Please select a patient to delete.")
            return
        
        # Get the patient info from the selected item
        item = self.results_tree.item(selection[0])
        patient_id = item['values'][0]
        patient_name = item['values'][2]
        
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
                # Refresh the list
                self.show_all_patients()
            else:
                messagebox.showerror("Error", f"Failed to delete patient {patient_name}.")
    
    def _display_results(self, results):
        """
        Display search results in the treeview
        
        Args:
            results (pandas.DataFrame): Search results
        """
        # Clear the treeview
        for item in self.results_tree.get_children():
            self.results_tree.delete(item)
        
        # Add the results to the treeview
        for _, row in results.iterrows():
            # Get patient name
            name = f"{row.get('first_name', '')} {row.get('last_name', '')}"
            
            # Format fees
            fees = row.get('fees', '')
            if fees:
                fees = f"PKR {fees}"
            
            self.results_tree.insert(
                "",
                "end",
                values=(
                    row.get('patient_id', ''),
                    row.get('token_number', ''),
                    name,
                    row.get('status', ''),
                    row.get('doctor_name', ''),
                    row.get('appointment_date', ''),
                    row.get('arrival_time', ''),
                    fees
                )
            )
    
    def show_all_patients(self):
        """Show all patients in the search results"""
        # Clear the search field
        self.search_var.set("")
        
        # Get all patients
        results = self.patient_model.get_all_patients()
        
        # Display the results
        self._display_results(results)