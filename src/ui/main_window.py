#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Window for the Receptionist Application
Provides the main UI for the application
"""

import os
import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from PIL import Image, ImageTk  # Add PIL import for image handling

from ui.patient_form import PatientForm
from ui.appointment_view import AppointmentView
from ui.search_panel import SearchPanel
from ui.settings_dialog import SettingsDialog
from ui.doctors_dialog import DoctorsDialog
from models.patient_model import PatientModel

logger = logging.getLogger('receptionist.main_window')

class MainWindow:
    """
    Main Window class for the Receptionist Application
    Provides the main UI for the application
    """
    
    def __init__(self, settings):
        """
        Initialize the Main Window
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.root = tk.Tk()
        self.root.title(settings.get('app_name', 'Clinic Receptionist'))
        self.root.geometry('1024x768')
        self.root.minsize(800, 600)
        
        # Set application icon
        try:
            # Check if logo file exists in resources directory
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'logo.png')
            if not os.path.exists(logo_path):
                # Create resources directory if it doesn't exist
                resources_dir = os.path.dirname(logo_path)
                if not os.path.exists(resources_dir):
                    os.makedirs(resources_dir)
                logger.warning(f"Logo file not found at {logo_path}. Please add a logo.png file.")
            else:
                # Process and set the window icon using PIL for better resizing
                try:
                    # Open the image with PIL
                    original_img = Image.open(logo_path)
                    
                    # Create appropriate icon sizes
                    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
                    icons = []
                    
                    for size in icon_sizes:
                        # Resize with high-quality resampling
                        resized_img = original_img.resize(size, Image.Resampling.LANCZOS)
                        # Convert to PhotoImage
                        photo_img = ImageTk.PhotoImage(resized_img)
                        icons.append(photo_img)
                    
                    # Set multiple icons for the window (tkinter will choose the best one)
                    self.root.iconphoto(True, *icons)
                    
                    # Keep a reference to prevent garbage collection
                    self._icons = icons
                    
                    logger.info("Application logo set successfully with multiple sizes")
                except ImportError:
                    # Fallback if PIL is not available
                    logo_img = tk.PhotoImage(file=logo_path)
                    self.root.iconphoto(True, logo_img)
                    logger.info("Application logo set with basic tkinter (PIL not available)")
        except Exception as e:
            logger.error(f"Failed to set application logo: {str(e)}")
        
        # Create the patient model
        self.patient_model = PatientModel(settings)
        
        # Create the UI
        self._create_ui()
        
        # Initialize data
        self._initialize_data()
        
        # Set up cleanup on window close
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
    
    def _create_ui(self):
        """Create the user interface"""
        # Configure the grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)  # Menu bar
        self.root.rowconfigure(1, weight=0)  # Toolbar
        self.root.rowconfigure(2, weight=0)  # Stats bar
        self.root.rowconfigure(3, weight=1)  # Main content
        self.root.rowconfigure(4, weight=0)  # Status bar
        
        # Create the menu bar
        self._create_menu_bar()
        
        # Create the toolbar
        self._create_toolbar()
        
        # Create the stats bar
        self._create_stats_bar()
        
        # Create the main content frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=3, column=0, sticky='nsew', padx=10, pady=10)
        
        # Configure the main frame grid
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.rowconfigure(0, weight=1)
        
        # Create the left panel (Search and Appointments)
        self.left_panel = ttk.Frame(self.main_frame)
        self.left_panel.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configure the left panel grid
        self.left_panel.columnconfigure(0, weight=1)
        self.left_panel.rowconfigure(0, weight=0)  # Search panel
        self.left_panel.rowconfigure(1, weight=1)  # Appointment view
        
        # Create the search panel
        self.search_panel = SearchPanel(self.left_panel, self.patient_model, self._on_patient_selected)
        self.search_panel.frame.grid(row=0, column=0, sticky='new', padx=5, pady=5)
        
        # Create the appointment view
        self.appointment_view = AppointmentView(self.left_panel, self.patient_model, self._on_patient_selected)
        self.appointment_view.frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create the right panel (Patient Form)
        self.patient_form = PatientForm(self.main_frame, self.settings, self.patient_model, 
                                       self._on_patient_saved, self._on_patient_printed)
        self.patient_form.frame.grid(row=0, column=1, sticky='nsew', padx=5, pady=5)
        
        # Create the status bar
        self._create_status_bar()
    
    def _create_menu_bar(self):
        """Create the menu bar"""
        self.menu_bar = tk.Menu(self.root)
        
        # File menu
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="New Patient", command=self._on_new_patient)
        file_menu.add_command(label="Print Current", command=self._on_print_current)
        file_menu.add_separator()
        file_menu.add_command(label="Backup Database", command=self._on_backup_database)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)
        
        # View menu
        view_menu = tk.Menu(self.menu_bar, tearoff=0)
        view_menu.add_command(label="Refresh", command=self._on_refresh, accelerator="F5")
        view_menu.add_command(label="Refresh Stats", command=self._on_refresh_stats)
        view_menu.add_separator()
        view_menu.add_command(label="Today's Appointments", command=self._on_view_today)
        view_menu.add_command(label="Tomorrow's Appointments", command=self._on_view_tomorrow)
        view_menu.add_command(label="All Patients", command=self._on_view_all_patients)
        view_menu.add_separator()
        view_menu.add_command(label="View Statistics", command=self._on_view_statistics, accelerator="Ctrl+S")
        self.menu_bar.add_cascade(label="View", menu=view_menu)
        
        # Tools menu
        tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        tools_menu.add_command(label="Settings", command=self._on_settings)
        tools_menu.add_command(label="Doctor List", command=self._on_doctor_list)
        self.menu_bar.add_cascade(label="Tools", menu=tools_menu)
        
        # Help menu
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self._on_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)
        
        self.root.config(menu=self.menu_bar)
        
        # Bind F5 key to refresh
        self.root.bind('<F5>', lambda event: self._on_refresh())
        
        # Bind Ctrl+S to view statistics
        self.root.bind('<Control-s>', lambda event: self._on_view_statistics())
    
    def _create_toolbar(self):
        """Create a toolbar with common actions"""
        toolbar_frame = ttk.Frame(self.root)
        toolbar_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=2)
        
        # New Patient button
        new_patient_btn = ttk.Button(toolbar_frame, text="New Patient", command=self._on_new_patient)
        new_patient_btn.pack(side=tk.LEFT, padx=2)
        
        # Refresh button
        refresh_btn = ttk.Button(toolbar_frame, text="Refresh", command=self._on_refresh)
        refresh_btn.pack(side=tk.LEFT, padx=2)
        
        # Refresh Stats button
        refresh_stats_btn = ttk.Button(toolbar_frame, text="Refresh Stats", command=self._on_refresh_stats)
        refresh_stats_btn.pack(side=tk.LEFT, padx=2)
        
        # Today's Appointments button
        today_btn = ttk.Button(toolbar_frame, text="Today", command=self._on_view_today)
        today_btn.pack(side=tk.LEFT, padx=2)
        
        # View Statistics button
        stats_btn = ttk.Button(toolbar_frame, text="Statistics", command=self._on_view_statistics)
        stats_btn.pack(side=tk.LEFT, padx=2)
        
        # Print button
        print_btn = ttk.Button(toolbar_frame, text="Print Current", command=self._on_print_current)
        print_btn.pack(side=tk.LEFT, padx=2)
        
        # Preview Thermal button
        preview_thermal_btn = ttk.Button(toolbar_frame, text="Preview Thermal", command=self._on_preview_thermal)
        preview_thermal_btn.pack(side=tk.LEFT, padx=2)
    
    def _create_stats_bar(self):
        """Create a compact stats bar showing daily, weekly, and monthly statistics"""
        # Create a frame for the stats bar with a border
        stats_frame = ttk.Frame(self.root, relief=tk.RIDGE, borderwidth=1)
        stats_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
        
        # Style for labels
        title_style = {'font': ('Arial', 9, 'bold')}
        value_style = {'font': ('Arial', 9)}
        
        # Create the daily stats section
        daily_frame = ttk.Frame(stats_frame)
        daily_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(daily_frame, text="TODAY:", **title_style).pack(side=tk.LEFT)
        self.daily_visits_label = ttk.Label(daily_frame, text="0 visits", **value_style)
        self.daily_visits_label.pack(side=tk.LEFT, padx=5)
        self.daily_revenue_label = ttk.Label(daily_frame, text="PKR 0", **value_style)
        self.daily_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Add separator
        ttk.Separator(stats_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Create the weekly stats section
        weekly_frame = ttk.Frame(stats_frame)
        weekly_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(weekly_frame, text="WEEK:", **title_style).pack(side=tk.LEFT)
        self.weekly_visits_label = ttk.Label(weekly_frame, text="0 visits", **value_style)
        self.weekly_visits_label.pack(side=tk.LEFT, padx=5)
        self.weekly_revenue_label = ttk.Label(weekly_frame, text="PKR 0", **value_style)
        self.weekly_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Add separator
        ttk.Separator(stats_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Create the monthly stats section
        monthly_frame = ttk.Frame(stats_frame)
        monthly_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(monthly_frame, text="MONTH:", **title_style).pack(side=tk.LEFT)
        self.monthly_visits_label = ttk.Label(monthly_frame, text="0 visits", **value_style)
        self.monthly_visits_label.pack(side=tk.LEFT, padx=5)
        self.monthly_revenue_label = ttk.Label(monthly_frame, text="PKR 0", **value_style)
        self.monthly_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        refresh_btn = ttk.Button(stats_frame, text="↻", width=2, command=self._on_refresh_stats)
        refresh_btn.pack(side=tk.RIGHT, padx=5, pady=2)
        
        # Update the stats initially
        self._update_stats_bar()
    
    def _update_stats_bar(self):
        """Update the statistics in the stats bar"""
        try:
            # Get current date
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            
            # Update daily stats
            daily_stats = self.patient_model.stats_handler.get_daily_stats(today)
            self.daily_visits_label.config(text=f"{daily_stats['visit_count']} visits")
            self.daily_revenue_label.config(text=f"PKR {daily_stats['revenue']:.2f}")
            
            # Update weekly stats
            weekly_stats = self.patient_model.stats_handler.get_weekly_stats()
            self.weekly_visits_label.config(text=f"{weekly_stats['visit_count']} visits")
            self.weekly_revenue_label.config(text=f"PKR {weekly_stats['revenue']:.2f}")
            
            # Update monthly stats
            monthly_stats = self.patient_model.stats_handler.get_monthly_stats()
            self.monthly_visits_label.config(text=f"{monthly_stats['visit_count']} visits")
            self.monthly_revenue_label.config(text=f"PKR {monthly_stats['revenue']:.2f}")
            
            logger.info("Updated stats bar")
            
        except Exception as e:
            logger.error(f"Error updating stats bar: {e}")
    
    def _create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Frame(self.root, relief=tk.SUNKEN)
        self.status_bar.grid(row=4, column=0, sticky='ew')
        
        # Status message label
        self.status_message = ttk.Label(self.status_bar, text="Ready", anchor=tk.W)
        self.status_message.pack(side=tk.LEFT, padx=5)
        
        # Database path label
        db_path = self.settings.get_excel_path()
        self.db_path_label = ttk.Label(self.status_bar, text=f"Database: {db_path}", anchor=tk.E)
        self.db_path_label.pack(side=tk.RIGHT, padx=5)
    
    def _initialize_data(self):
        """Initialize data and load today's appointments"""
        self._on_view_today()
    
    def _on_patient_selected(self, patient_data):
        """
        Handle patient selection
        
        Args:
            patient_data (dict): Selected patient data
        """
        # Load the patient data into the form
        self.patient_form.load_patient(patient_data)
        
        # Update status
        self.status_message.config(text=f"Loaded patient: {patient_data.get('first_name', '')} {patient_data.get('last_name', '')}")
    
    def _on_patient_saved(self, patient_data):
        """
        Handle patient save
        
        Args:
            patient_data (dict): Saved patient data
        """
        # Refresh appointment view if necessary
        self.appointment_view.refresh()
        
        # Update status
        self.status_message.config(text=f"Saved patient: {patient_data.get('first_name', '')} {patient_data.get('last_name', '')}")
    
    def _on_patient_printed(self, patient_data):
        """
        Handle patient reception slip printing
        
        Args:
            patient_data (dict): Patient data
        """
        # Update status
        self.status_message.config(text=f"Printed reception slip for: {patient_data.get('first_name', '')} {patient_data.get('last_name', '')}")
    
    def _on_new_patient(self):
        """Handle new patient command"""
        # Clear the form
        self.patient_form.clear()
        
        # Set default appointment date and time
        now = datetime.now()
        self.patient_form.set_default_appointment(now)
        
        # Update status
        self.status_message.config(text="New patient")
    
    def _on_print_current(self):
        """Handle print current command"""
        self.patient_form.print_reception_slip()
    
    def _on_backup_database(self):
        """Handle backup database command"""
        try:
            # Use the Excel handler to create a backup
            self.patient_model.excel_handler._create_backup()
            messagebox.showinfo("Backup Created", "Database backup created successfully.")
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            messagebox.showerror("Backup Error", f"Error creating backup: {e}")
    
    def _on_view_today(self):
        """Handle view today's appointments command"""
        today = datetime.now().strftime('%Y-%m-%d')
        self.appointment_view.show_appointments_for_date(today)
        self.status_message.config(text=f"Viewing appointments for today ({today})")
    
    def _on_view_tomorrow(self):
        """Handle view tomorrow's appointments command"""
        tomorrow = (datetime.now() + timedelta(days=1)).strftime('%Y-%m-%d')
        self.appointment_view.show_appointments_for_date(tomorrow)
        self.status_message.config(text=f"Viewing appointments for tomorrow ({tomorrow})")
    
    def _on_view_all_patients(self):
        """Handle view all patients command"""
        self.search_panel.show_all_patients()
        self.status_message.config(text="Viewing all patients")
    
    def _on_settings(self):
        """Handle settings command"""
        # Open the settings dialog
        SettingsDialog(self.root, self.settings, self._on_settings_saved)
    
    def _on_settings_saved(self):
        """Handle settings saved event"""
        # Update window title
        self.root.title(self.settings.get('app_name', 'Clinic Receptionist'))
        
        # Update database path label
        db_path = self.settings.get_excel_path()
        self.db_path_label.config(text=f"Database: {db_path}")
        
        # Refresh patient form if it exists
        if hasattr(self, 'patient_form'):
            # Update doctor list in the patient form
            doctors = self.settings.get("doctors", [])
            self.patient_form.doctor_name_combo['values'] = doctors
            
            # Update default appointment duration
            self.patient_form.appointment_duration_var.set(
                str(self.settings.get("appointment_duration_mins", 30))
            )
        
        # Refresh data
        self._on_refresh()
        
        # Update status
        self.status_message.config(text="Settings updated")
    
    def _on_doctor_list(self):
        """Handle doctor list command"""
        # Open the doctors dialog
        DoctorsDialog(self.root, self.settings, self._on_doctors_saved)
    
    def _on_doctors_saved(self):
        """Handle doctors saved event"""
        # Update doctor list in the patient form if it exists
        if hasattr(self, 'patient_form'):
            doctors = self.settings.get("doctors", [])
            self.patient_form.doctor_name_combo['values'] = doctors
        
        # Update status
        self.status_message.config(text="Doctors list updated")
    
    def _on_about(self):
        """Handle about command"""
        messagebox.showinfo(
            "About Clinic Receptionist",
            f"{self.settings.get('app_name', 'Clinic Receptionist')}\n\n"
            f"Version: 1.0.0\n\n"
            f"A receptionist application for doctor clinics.\n\n"
            f"© {datetime.now().year} {self.settings.get('company_name', 'My Doctor Clinic')}"
        )
    
    def _on_refresh(self):
        """Handle refresh command"""
        # Refresh appointment view
        self.appointment_view.refresh()
        
        # Refresh search results if showing all patients
        self.search_panel.show_all_patients()
        
        # Refresh stats bar
        self._update_stats_bar()
        
        # Update status
        self.status_message.config(text="Data refreshed")
    
    def _on_refresh_stats(self):
        """Handle refresh stats command"""
        # Update the stats bar
        self._update_stats_bar()
        
        # Update status
        self.status_message.config(text="Statistics refreshed")
        
        # If statistics window is open, refresh it
        for window in self.root.winfo_children():
            if isinstance(window, tk.Toplevel) and window.title() == "Clinic Statistics":
                # Find the StatsView in the window
                for child in window.winfo_children():
                    if hasattr(child, 'update_stats'):
                        child.update_stats()
                        break
    
    def _on_view_statistics(self):
        """Open the statistics view window"""
        # Create a new top level window
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Clinic Statistics")
        stats_window.geometry("800x600")
        stats_window.minsize(700, 500)
        
        # Create the statistics view
        from ui.stats_view import StatsView
        stats_view = StatsView(stats_window, self.patient_model)
        
        # Set the window position
        stats_window.update_idletasks()
        width = stats_window.winfo_width()
        height = stats_window.winfo_height()
        x = (stats_window.winfo_screenwidth() // 2) - (width // 2)
        y = (stats_window.winfo_screenheight() // 2) - (height // 2)
        stats_window.geometry(f'{width}x{height}+{x}+{y}')
        
        # Make the window modal
        stats_window.transient(self.root)
        stats_window.grab_set()
        
        # Update status
        self.status_message.config(text="Viewing statistics")
    
    def _on_close(self):
        """Handle window close event"""
        # Clean up resources
        if hasattr(self, 'patient_form'):
            self.patient_form.cleanup()
        
        # Close the window
        self.root.destroy()
    
    def _on_preview_thermal(self):
        """Handle preview thermal receipt command"""
        # Get the current patient data from the form
        patient_data = self.patient_form.get_patient_data()
        if not patient_data.get('first_name'):
            messagebox.showwarning("No Patient Loaded", "Please load or enter patient details before previewing.")
            return
        
        # Use the print handler to generate and show the preview
        from utils.print_handler import PrintHandler
        print_handler = PrintHandler(self.settings)
        print_handler.preview_thermal_receipt(patient_data)
    
    def run(self):
        """Run the application"""
        # Center the window on the screen
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Run the application
        self.root.mainloop()