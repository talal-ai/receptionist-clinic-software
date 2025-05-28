#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Statistics View for the Receptionist Application
Provides a standalone page for viewing statistics
"""

import logging
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

logger = logging.getLogger('receptionist.stats_view')

class StatsView:
    """
    Statistics View class for the Receptionist Application
    Provides a standalone page for viewing statistics
    """
    
    def __init__(self, parent, patient_model):
        """
        Initialize the Statistics View
        
        Args:
            parent: Parent widget (typically a Toplevel window)
            patient_model: PatientModel instance
        """
        self.parent = parent
        self.patient_model = patient_model
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Use the stats handler from the patient model
        self.stats_handler = patient_model.stats_handler
        
        # Set default window properties
        if isinstance(parent, tk.Toplevel):
            parent.title("Clinic Statistics Dashboard")
            parent.minsize(800, 600)
            
            # Set window icon if available
            try:
                parent.iconbitmap("icon.ico")
            except:
                pass
        
        # Create the UI
        self._create_ui()
        
        # Initial update with loading indicator
        self.parent.after(100, self.update_stats)  # Short delay before loading data
    
    def _create_ui(self):
        """Create the user interface"""
        # Configure the frame
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=0)  # Title
        self.frame.rowconfigure(1, weight=0)  # Controls
        self.frame.rowconfigure(2, weight=1)  # Tables
        
        # Title section with professional styling
        title_frame = ttk.Frame(self.frame)
        title_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        title_frame.columnconfigure(0, weight=1)
        
        # Add a horizontal separator above the title
        ttk.Separator(title_frame, orient='horizontal').grid(row=0, column=0, sticky='ew', pady=5)
        
        # Title with better styling
        header_frame = ttk.Frame(title_frame)
        header_frame.grid(row=1, column=0, sticky='ew')
        
        title_label = ttk.Label(
            header_frame, 
            text="Clinic Statistics Dashboard", 
            font=('Arial', 18, 'bold'),
            foreground='#0066cc'
        )
        title_label.pack(side=tk.LEFT, padx=5)
        
        # Subtitle with current date
        current_date = datetime.now().strftime('%B %d, %Y')
        subtitle_label = ttk.Label(
            header_frame,
            text=f"Data as of {current_date}",
            font=('Arial', 10, 'italic'),
            foreground='#666666'
        )
        subtitle_label.pack(side=tk.LEFT, padx=(10, 5))
        
        # Refresh button with icon text
        refresh_btn = ttk.Button(header_frame, text="↻ Refresh Data", command=self.update_stats)
        refresh_btn.pack(side=tk.RIGHT, padx=5)
        
        # Add a horizontal separator below the title
        ttk.Separator(title_frame, orient='horizontal').grid(row=2, column=0, sticky='ew', pady=5)
        
        # Create controls section
        self._create_controls_section()
        
        # Create tables section
        self._create_tables_section()
    
    def _create_controls_section(self):
        """Create the controls section with date selectors"""
        controls_frame = ttk.LabelFrame(self.frame, text="Date Selection")
        controls_frame.grid(row=1, column=0, sticky='ew', padx=5, pady=5)
        
        # Configure the grid
        controls_frame.columnconfigure(0, weight=1)  # Daily controls
        controls_frame.columnconfigure(1, weight=1)  # Weekly controls
        controls_frame.columnconfigure(2, weight=1)  # Monthly controls
        
        # Style for section headers
        section_header_style = {'font': ('Arial', 10, 'bold'), 'foreground': '#0066cc'}
        
        # Daily controls
        daily_frame = ttk.Frame(controls_frame, padding=10)
        daily_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=5)
        
        ttk.Label(daily_frame, text="Daily Statistics", **section_header_style).pack(anchor='w', pady=(0, 5))
        
        # Add a separator after the header
        ttk.Separator(daily_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(daily_frame, text="Select Date:").pack(anchor='w', pady=(5, 0))
        
        date_frame = ttk.Frame(daily_frame)
        date_frame.pack(fill='x', pady=5)
        
        # Use separate spinboxes for year, month, day
        year = datetime.now().year
        month = datetime.now().month
        day = datetime.now().day
        
        self.daily_year_var = tk.StringVar(value=str(year))
        self.daily_month_var = tk.StringVar(value=str(month))
        self.daily_day_var = tk.StringVar(value=str(day))
        
        year_spinner = ttk.Spinbox(date_frame, from_=2000, to=2100, width=5, textvariable=self.daily_year_var)
        month_spinner = ttk.Spinbox(date_frame, from_=1, to=12, width=3, textvariable=self.daily_month_var)
        day_spinner = ttk.Spinbox(date_frame, from_=1, to=31, width=3, textvariable=self.daily_day_var)
        
        year_spinner.pack(side=tk.LEFT, padx=2)
        ttk.Label(date_frame, text="-").pack(side=tk.LEFT)
        month_spinner.pack(side=tk.LEFT, padx=2)
        ttk.Label(date_frame, text="-").pack(side=tk.LEFT)
        day_spinner.pack(side=tk.LEFT, padx=2)
        
        # Go button with better styling
        ttk.Button(date_frame, text="Apply", width=8, command=self._on_daily_date_change).pack(side=tk.LEFT, padx=(10, 0))
        
        # Weekly controls
        weekly_frame = ttk.Frame(controls_frame, padding=10)
        weekly_frame.grid(row=0, column=1, sticky='nsew', padx=10, pady=5)
        
        ttk.Label(weekly_frame, text="Weekly Statistics", **section_header_style).pack(anchor='w', pady=(0, 5))
        
        # Add a separator after the header
        ttk.Separator(weekly_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(weekly_frame, text="Select End Date:").pack(anchor='w', pady=(5, 0))
        
        date_frame = ttk.Frame(weekly_frame)
        date_frame.pack(fill='x', pady=5)
        
        self.weekly_year_var = tk.StringVar(value=str(year))
        self.weekly_month_var = tk.StringVar(value=str(month))
        self.weekly_day_var = tk.StringVar(value=str(day))
        
        year_spinner = ttk.Spinbox(date_frame, from_=2000, to=2100, width=5, textvariable=self.weekly_year_var)
        month_spinner = ttk.Spinbox(date_frame, from_=1, to=12, width=3, textvariable=self.weekly_month_var)
        day_spinner = ttk.Spinbox(date_frame, from_=1, to=31, width=3, textvariable=self.weekly_day_var)
        
        year_spinner.pack(side=tk.LEFT, padx=2)
        ttk.Label(date_frame, text="-").pack(side=tk.LEFT)
        month_spinner.pack(side=tk.LEFT, padx=2)
        ttk.Label(date_frame, text="-").pack(side=tk.LEFT)
        day_spinner.pack(side=tk.LEFT, padx=2)
        
        # Go button
        ttk.Button(date_frame, text="Apply", width=8, command=self._on_weekly_date_change).pack(side=tk.LEFT, padx=(10, 0))
        
        # Monthly controls
        monthly_frame = ttk.Frame(controls_frame, padding=10)
        monthly_frame.grid(row=0, column=2, sticky='nsew', padx=10, pady=5)
        
        ttk.Label(monthly_frame, text="Monthly Statistics", **section_header_style).pack(anchor='w', pady=(0, 5))
        
        # Add a separator after the header
        ttk.Separator(monthly_frame, orient='horizontal').pack(fill='x', pady=5)
        
        ttk.Label(monthly_frame, text="Select Month:").pack(anchor='w', pady=(5, 0))
        
        date_frame = ttk.Frame(monthly_frame)
        date_frame.pack(fill='x', pady=5)
        
        self.monthly_year_var = tk.StringVar(value=str(year))
        self.monthly_month_var = tk.StringVar(value=str(month))
        
        year_spinner = ttk.Spinbox(date_frame, from_=2000, to=2100, width=5, textvariable=self.monthly_year_var)
        month_spinner = ttk.Spinbox(date_frame, from_=1, to=12, width=3, textvariable=self.monthly_month_var)
        
        year_spinner.pack(side=tk.LEFT, padx=2)
        ttk.Label(date_frame, text="-").pack(side=tk.LEFT)
        month_spinner.pack(side=tk.LEFT, padx=2)
        
        # Go button
        ttk.Button(date_frame, text="Apply", width=8, command=self._on_monthly_date_change).pack(side=tk.LEFT, padx=(10, 0))
    
    def _create_tables_section(self):
        """Create the tables section with statistics tables"""
        tables_frame = ttk.Frame(self.frame, padding=5)
        tables_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
        
        # Configure the grid
        tables_frame.columnconfigure(0, weight=1)
        tables_frame.rowconfigure(0, weight=1)
        
        # Create notebook with tabs
        self.notebook = ttk.Notebook(tables_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Daily stats tab
        daily_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(daily_tab, text="Daily Statistics")
        daily_tab.columnconfigure(0, weight=1)
        daily_tab.rowconfigure(0, weight=0)  # Info
        daily_tab.rowconfigure(1, weight=1)  # Table
        
        # Daily info frame with better styling
        daily_info_frame = ttk.Frame(daily_tab, padding=5)
        daily_info_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Add a border around the info frame
        daily_info_border = ttk.LabelFrame(daily_info_frame, text="Date Information")
        daily_info_border.pack(fill='x', expand=True)
        
        info_content = ttk.Frame(daily_info_border, padding=10)
        info_content.pack(fill='x')
        
        ttk.Label(info_content, text="Selected Date:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.daily_date_label = ttk.Label(info_content, text="", font=('Arial', 10), foreground='#0066cc')
        self.daily_date_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Daily table with improved styling
        daily_table_frame = ttk.Frame(daily_tab)
        daily_table_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create a border around the table
        daily_table_border = ttk.LabelFrame(daily_table_frame, text="Daily Metrics")
        daily_table_border.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create table container
        daily_table_container = ttk.Frame(daily_table_border, padding=10)
        daily_table_container.pack(fill='both', expand=True)
        
        # Create Treeview with better styling
        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 10))
        style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))
        
        self.daily_tree = ttk.Treeview(
            daily_table_container, 
            columns=("metric", "value"), 
            show="headings",
            style="Treeview"
        )
        self.daily_tree.heading("metric", text="Metric")
        self.daily_tree.heading("value", text="Value")
        self.daily_tree.column("metric", width=250, anchor='w')
        self.daily_tree.column("value", width=200, anchor='e')
        
        # Add scrollbar
        daily_scrollbar = ttk.Scrollbar(daily_table_container, orient="vertical", command=self.daily_tree.yview)
        self.daily_tree.configure(yscrollcommand=daily_scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.daily_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        daily_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Weekly stats tab
        weekly_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(weekly_tab, text="Weekly Statistics")
        weekly_tab.columnconfigure(0, weight=1)
        weekly_tab.rowconfigure(0, weight=0)  # Info
        weekly_tab.rowconfigure(1, weight=1)  # Table
        
        # Weekly info frame
        weekly_info_frame = ttk.Frame(weekly_tab, padding=5)
        weekly_info_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Add a border around the info frame
        weekly_info_border = ttk.LabelFrame(weekly_info_frame, text="Date Range")
        weekly_info_border.pack(fill='x', expand=True)
        
        info_content = ttk.Frame(weekly_info_border, padding=10)
        info_content.pack(fill='x')
        
        ttk.Label(info_content, text="Selected Period:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.weekly_range_label = ttk.Label(info_content, text="", font=('Arial', 10), foreground='#0066cc')
        self.weekly_range_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Weekly table with improved styling
        weekly_table_frame = ttk.Frame(weekly_tab)
        weekly_table_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create a border around the table
        weekly_table_border = ttk.LabelFrame(weekly_table_frame, text="Weekly Metrics")
        weekly_table_border.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create table container
        weekly_table_container = ttk.Frame(weekly_table_border, padding=10)
        weekly_table_container.pack(fill='both', expand=True)
        
        # Create Treeview
        self.weekly_tree = ttk.Treeview(
            weekly_table_container, 
            columns=("metric", "value"), 
            show="headings",
            style="Treeview"
        )
        self.weekly_tree.heading("metric", text="Metric")
        self.weekly_tree.heading("value", text="Value")
        self.weekly_tree.column("metric", width=250, anchor='w')
        self.weekly_tree.column("value", width=200, anchor='e')
        
        # Add scrollbar
        weekly_scrollbar = ttk.Scrollbar(weekly_table_container, orient="vertical", command=self.weekly_tree.yview)
        self.weekly_tree.configure(yscrollcommand=weekly_scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.weekly_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        weekly_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Monthly stats tab
        monthly_tab = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(monthly_tab, text="Monthly Statistics")
        monthly_tab.columnconfigure(0, weight=1)
        monthly_tab.rowconfigure(0, weight=0)  # Info
        monthly_tab.rowconfigure(1, weight=1)  # Table
        
        # Monthly info frame
        monthly_info_frame = ttk.Frame(monthly_tab, padding=5)
        monthly_info_frame.grid(row=0, column=0, sticky='ew', padx=5, pady=5)
        
        # Add a border around the info frame
        monthly_info_border = ttk.LabelFrame(monthly_info_frame, text="Month Information")
        monthly_info_border.pack(fill='x', expand=True)
        
        info_content = ttk.Frame(monthly_info_border, padding=10)
        info_content.pack(fill='x')
        
        ttk.Label(info_content, text="Selected Month:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT)
        self.month_name_label = ttk.Label(info_content, text="", font=('Arial', 10), foreground='#0066cc')
        self.month_name_label.pack(side=tk.LEFT, padx=(5, 0))
        
        # Monthly table with improved styling
        monthly_table_frame = ttk.Frame(monthly_tab)
        monthly_table_frame.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Create a border around the table
        monthly_table_border = ttk.LabelFrame(monthly_table_frame, text="Monthly Metrics")
        monthly_table_border.pack(fill='both', expand=True, padx=2, pady=2)
        
        # Create table container
        monthly_table_container = ttk.Frame(monthly_table_border, padding=10)
        monthly_table_container.pack(fill='both', expand=True)
        
        # Create Treeview
        self.monthly_tree = ttk.Treeview(
            monthly_table_container, 
            columns=("metric", "value"), 
            show="headings",
            style="Treeview"
        )
        self.monthly_tree.heading("metric", text="Metric")
        self.monthly_tree.heading("value", text="Value")
        self.monthly_tree.column("metric", width=250, anchor='w')
        self.monthly_tree.column("value", width=200, anchor='e')
        
        # Add scrollbar
        monthly_scrollbar = ttk.Scrollbar(monthly_table_container, orient="vertical", command=self.monthly_tree.yview)
        self.monthly_tree.configure(yscrollcommand=monthly_scrollbar.set)
        
        # Pack the Treeview and scrollbar
        self.monthly_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        monthly_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def _on_daily_date_change(self):
        """Handle daily date change"""
        try:
            year = int(self.daily_year_var.get())
            month = int(self.daily_month_var.get())
            day = int(self.daily_day_var.get())
            
            # Validate date
            try:
                date = datetime(year, month, day)
                date_str = date.strftime('%Y-%m-%d')
                
                # Update stats for this date
                self._update_daily_stats(date_str)
                
                # Switch to daily tab
                self.notebook.select(0)
                
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please enter a valid date.")
                
        except ValueError as e:
            logger.error(f"Invalid date: {e}")
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for year, month, and day.")
    
    def _on_weekly_date_change(self):
        """Handle weekly date change"""
        try:
            year = int(self.weekly_year_var.get())
            month = int(self.weekly_month_var.get())
            day = int(self.weekly_day_var.get())
            
            # Validate date
            try:
                end_date = datetime(year, month, day)
                date_str = end_date.strftime('%Y-%m-%d')
                
                # Update stats for this week
                self._update_weekly_stats(date_str)
                
                # Switch to weekly tab
                self.notebook.select(1)
                
            except ValueError:
                messagebox.showwarning("Invalid Date", "Please enter a valid date.")
                
        except ValueError as e:
            logger.error(f"Invalid date: {e}")
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for year, month, and day.")
    
    def _on_monthly_date_change(self):
        """Handle monthly date change"""
        try:
            year = int(self.monthly_year_var.get())
            month = int(self.monthly_month_var.get())
            
            # Validate month
            if month < 1 or month > 12:
                messagebox.showwarning("Invalid Month", "Month must be between 1 and 12.")
                return
                
            # Update stats for this month
            self._update_monthly_stats(year, month)
            
            # Switch to monthly tab
            self.notebook.select(2)
            
        except ValueError as e:
            logger.error(f"Invalid date: {e}")
            messagebox.showwarning("Invalid Input", "Please enter valid numbers for year and month.")
    
    def _update_daily_stats(self, date):
        """Update daily statistics"""
        daily_stats = self.stats_handler.get_daily_stats(date)
        
        # Update date label
        formatted_date = datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d, %Y')
        self.daily_date_label.config(text=formatted_date)
        
        # Clear previous data
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)
        
        # Configure treeview tags for alternating row colors
        self.daily_tree.tag_configure('odd', background='#f5f5f5')
        self.daily_tree.tag_configure('even', background='#ffffff')
        self.daily_tree.tag_configure('highlight', background='#e6f2ff')
        
        # Add metrics to table
        metrics = [
            ("Date", date),
            ("Total Patient Visits", daily_stats['visit_count']),
            ("Total Revenue", f"PKR {daily_stats['revenue']:.2f}"),
            ("Average Revenue per Visit", f"PKR {daily_stats['revenue'] / daily_stats['visit_count']:.2f}" if daily_stats['visit_count'] > 0 else "PKR 0.00")
        ]
        
        # Insert with alternating colors
        for i, (metric, value) in enumerate(metrics):
            tag = 'even' if i % 2 == 0 else 'odd'
            # Highlight the revenue row
            if "Revenue" in metric:
                tag = 'highlight'
            self.daily_tree.insert("", "end", values=(metric, value), tags=(tag,))
    
    def _update_weekly_stats(self, end_date):
        """Update weekly statistics"""
        weekly_stats = self.stats_handler.get_weekly_stats(end_date)
        
        # Update range label
        self.weekly_range_label.config(text=f"{weekly_stats['start_date']} to {weekly_stats['end_date']}")
        
        # Clear previous data
        for item in self.weekly_tree.get_children():
            self.weekly_tree.delete(item)
        
        # Configure treeview tags for alternating row colors
        self.weekly_tree.tag_configure('odd', background='#f5f5f5')
        self.weekly_tree.tag_configure('even', background='#ffffff')
        self.weekly_tree.tag_configure('highlight', background='#e6f2ff')
        
        # Add metrics to table
        metrics = [
            ("Date Range", f"{weekly_stats['start_date']} to {weekly_stats['end_date']}"),
            ("Total Patient Visits", weekly_stats['visit_count']),
            ("Total Revenue", f"PKR {weekly_stats['revenue']:.2f}"),
            ("Average Revenue per Visit", f"PKR {weekly_stats['revenue'] / weekly_stats['visit_count']:.2f}" if weekly_stats['visit_count'] > 0 else "PKR 0.00"),
            ("Average Daily Visits", f"{weekly_stats['visit_count'] / 7:.1f}"),
            ("Average Daily Revenue", f"PKR {weekly_stats['revenue'] / 7:.2f}")
        ]
        
        # Insert with alternating colors
        for i, (metric, value) in enumerate(metrics):
            tag = 'even' if i % 2 == 0 else 'odd'
            # Highlight revenue rows
            if "Revenue" in metric:
                tag = 'highlight'
            self.weekly_tree.insert("", "end", values=(metric, value), tags=(tag,))
    
    def _update_monthly_stats(self, year, month):
        """Update monthly statistics"""
        monthly_stats = self.stats_handler.get_monthly_stats(year, month)
        
        # Get month name
        month_name = datetime(year, month, 1).strftime('%B %Y')
        
        # Update month label
        self.month_name_label.config(text=month_name)
        
        # Clear previous data
        for item in self.monthly_tree.get_children():
            self.monthly_tree.delete(item)
        
        # Configure treeview tags for alternating row colors
        self.monthly_tree.tag_configure('odd', background='#f5f5f5')
        self.monthly_tree.tag_configure('even', background='#ffffff')
        self.monthly_tree.tag_configure('highlight', background='#e6f2ff')
        self.monthly_tree.tag_configure('projection', background='#fff8e1')
        
        # Calculate days in month
        if month == 12:
            last_day = 31
        else:
            last_day = (datetime(year, month+1, 1) - datetime(year, month, 1)).days
        
        # Add metrics to table
        metrics = [
            ("Month", month_name),
            ("Total Patient Visits", monthly_stats['visit_count']),
            ("Total Revenue", f"PKR {monthly_stats['revenue']:.2f}"),
            ("Average Revenue per Visit", f"PKR {monthly_stats['revenue'] / monthly_stats['visit_count']:.2f}" if monthly_stats['visit_count'] > 0 else "PKR 0.00"),
            ("Average Daily Visits", f"{monthly_stats['visit_count'] / last_day:.1f}"),
            ("Average Daily Revenue", f"PKR {monthly_stats['revenue'] / last_day:.2f}"),
            ("Projected Monthly Visits", f"{monthly_stats['visit_count'] / datetime.now().day * last_day:.1f}" if month == datetime.now().month and year == datetime.now().year else "N/A"),
            ("Projected Monthly Revenue", f"PKR {monthly_stats['revenue'] / datetime.now().day * last_day:.2f}" if month == datetime.now().month and year == datetime.now().year else "N/A")
        ]
        
        # Insert with alternating colors
        for i, (metric, value) in enumerate(metrics):
            tag = 'even' if i % 2 == 0 else 'odd'
            # Highlight revenue rows
            if "Revenue" in metric and "Projected" not in metric:
                tag = 'highlight'
            # Use special highlighting for projections
            if "Projected" in metric:
                tag = 'projection'
            self.monthly_tree.insert("", "end", values=(metric, value), tags=(tag,))
    
    def update_stats(self):
        """Update all statistics"""
        try:
            # Show a message while updating
            self.notebook.pack_forget()
            updating_frame = ttk.Frame(self.frame)
            updating_frame.grid(row=2, column=0, sticky='nsew', padx=5, pady=5)
            updating_label = ttk.Label(updating_frame, text="Updating statistics...", font=('Arial', 12))
            updating_label.pack(expand=True, pady=50)
            self.frame.update()
            
            # Update daily stats with current date
            today = datetime.now().strftime('%Y-%m-%d')
            self._update_daily_stats(today)
            
            # Update weekly stats ending today
            self._update_weekly_stats(today)
            
            # Update monthly stats for current month
            now = datetime.now()
            self._update_monthly_stats(now.year, now.month)
            
            logger.info("Updated all statistics")
            
            # Restore the notebook
            updating_frame.destroy()
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            logger.error(f"Error updating stats: {e}")
            messagebox.showerror("Statistics Error", f"An error occurred while updating statistics: {e}") 