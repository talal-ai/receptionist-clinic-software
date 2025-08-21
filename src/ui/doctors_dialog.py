#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Doctors Dialog for the Receptionist Application
Provides a dialog for managing doctors
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging

logger = logging.getLogger('receptionist.doctors_dialog')

class DoctorsDialog:
    """
    Doctors Dialog class for the Receptionist Application
    Provides a dialog for managing doctors
    """
    
    def __init__(self, parent, settings, callback=None):
        """
        Initialize the Doctors Dialog
        
        Args:
            parent: Parent widget
            settings: Application settings
            callback: Callback function when doctors are saved
        """
        self.parent = parent
        self.settings = settings
        self.callback = callback
        
        # Get current doctors
        self.doctors = settings.get("doctors", [])
        
        # Create the dialog
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Doctors List")
        self.dialog.geometry("500x400")
        self.dialog.minsize(400, 300)
        self.dialog.resizable(True, True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Make dialog modal
        self.dialog.focus_set()
        
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
        # Create main frame with padding
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configure grid
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=0)  # Header
        main_frame.rowconfigure(1, weight=1)  # Doctors list
        main_frame.rowconfigure(2, weight=0)  # Input area
        main_frame.rowconfigure(3, weight=0)  # Buttons
        
        # Header label
        header_label = ttk.Label(main_frame, text="Manage Doctors", font=("TkDefaultFont", 12, "bold"))
        header_label.grid(row=0, column=0, sticky='w', padx=5, pady=(0, 10))
        
        # Create frame for the listbox and scrollbar
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        # Listbox for doctors
        self.doctors_listbox = tk.Listbox(list_frame, selectmode=tk.SINGLE)
        self.doctors_listbox.grid(row=0, column=0, sticky='nsew')
        
        # Populate doctors
        for doctor in self.doctors:
            self.doctors_listbox.insert(tk.END, doctor)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient='vertical', command=self.doctors_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.doctors_listbox['yscrollcommand'] = scrollbar.set
        
        # Bind selection event
        self.doctors_listbox.bind('<<ListboxSelect>>', self._on_doctor_selected)
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=5)
        input_frame.columnconfigure(1, weight=1)
        
        # Doctor name
        ttk.Label(input_frame, text="Doctor Name:").grid(row=0, column=0, sticky='w', padx=(0, 5))
        self.doctor_name_var = tk.StringVar()
        self.doctor_name_entry = ttk.Entry(input_frame, textvariable=self.doctor_name_var, width=40)
        self.doctor_name_entry.grid(row=0, column=1, sticky='ew', padx=5)
        
        # Buttons area
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky='ew', padx=5, pady=(10, 0))
        
        # Action buttons
        self.add_button = ttk.Button(button_frame, text="Add", command=self._on_add)
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.update_button = ttk.Button(button_frame, text="Update", command=self._on_update, state=tk.DISABLED)
        self.update_button.pack(side=tk.LEFT, padx=5)
        
        self.remove_button = ttk.Button(button_frame, text="Remove", command=self._on_remove, state=tk.DISABLED)
        self.remove_button.pack(side=tk.LEFT, padx=5)
        
        # Save and cancel buttons
        self.cancel_button = ttk.Button(button_frame, text="Cancel", command=self.dialog.destroy)
        self.cancel_button.pack(side=tk.RIGHT, padx=5)
        
        self.save_button = ttk.Button(button_frame, text="Save", command=self._on_save)
        self.save_button.pack(side=tk.RIGHT, padx=5)
    
    def _on_doctor_selected(self, event):
        """Handle doctor selection"""
        try:
            # Get selected index
            selection = self.doctors_listbox.curselection()
            if selection:
                index = selection[0]
                doctor = self.doctors_listbox.get(index)
                
                # Set selected doctor name in the entry field
                self.doctor_name_var.set(doctor)
                
                # Enable update and remove buttons
                self.update_button.config(state=tk.NORMAL)
                self.remove_button.config(state=tk.NORMAL)
            else:
                # Disable update and remove buttons if no selection
                self.update_button.config(state=tk.DISABLED)
                self.remove_button.config(state=tk.DISABLED)
                
        except Exception as e:
            logger.error(f"Error handling doctor selection: {e}")
    
    def _on_add(self):
        """Add a new doctor"""
        doctor_name = self.doctor_name_var.get().strip()
        if not doctor_name:
            messagebox.showerror("Error", "Doctor name cannot be empty")
            return
        
        # Check if doctor already exists
        if doctor_name in self.doctors:
            messagebox.showwarning("Warning", f"Doctor '{doctor_name}' already exists")
            return
        
        # Add to the list
        self.doctors.append(doctor_name)
        self.doctors_listbox.insert(tk.END, doctor_name)
        
        # Clear entry
        self.doctor_name_var.set("")
    
    def _on_update(self):
        """Update selected doctor"""
        selection = self.doctors_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No doctor selected")
            return
        
        doctor_name = self.doctor_name_var.get().strip()
        if not doctor_name:
            messagebox.showerror("Error", "Doctor name cannot be empty")
            return
        
        # Get selected index
        index = selection[0]
        old_doctor = self.doctors_listbox.get(index)
        
        # Check if new name already exists and is not the same as the current one
        if doctor_name != old_doctor and doctor_name in self.doctors:
            messagebox.showwarning("Warning", f"Doctor '{doctor_name}' already exists")
            return
        
        # Update the list
        self.doctors[self.doctors.index(old_doctor)] = doctor_name
        self.doctors_listbox.delete(index)
        self.doctors_listbox.insert(index, doctor_name)
        self.doctors_listbox.selection_set(index)
        
        # Clear entry
        self.doctor_name_var.set("")
        
        # Disable update and remove buttons
        self.update_button.config(state=tk.DISABLED)
        self.remove_button.config(state=tk.DISABLED)
    
    def _on_remove(self):
        """Remove selected doctor"""
        selection = self.doctors_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "No doctor selected")
            return
        
        # Get selected index and doctor name
        index = selection[0]
        doctor = self.doctors_listbox.get(index)
        
        # Confirm removal
        confirm = messagebox.askyesno("Confirm Removal", f"Are you sure you want to remove doctor '{doctor}'?")
        if not confirm:
            return
        
        # Remove from the list
        self.doctors.remove(doctor)
        self.doctors_listbox.delete(index)
        
        # Clear entry
        self.doctor_name_var.set("")
        
        # Disable update and remove buttons
        self.update_button.config(state=tk.DISABLED)
        self.remove_button.config(state=tk.DISABLED)
    
    def _on_save(self):
        """Save doctors list"""
        try:
            # Update settings
            self.settings.set("doctors", self.doctors)
            
            # Call callback if provided
            if self.callback:
                self.callback()
            
            # Close dialog
            self.dialog.destroy()
            
            # Show success message
            messagebox.showinfo("Doctors Saved", "Doctors list has been saved successfully.")
            
        except Exception as e:
            logger.error(f"Error saving doctors: {e}")
            messagebox.showerror("Error", f"An error occurred while saving doctors: {e}") 