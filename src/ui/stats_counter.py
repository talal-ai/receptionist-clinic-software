#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stats Counter for the Receptionist Application
Displays statistics in the top bar
"""

import logging
import tkinter as tk
from tkinter import ttk
from datetime import datetime

logger = logging.getLogger('receptionist.stats_counter')

class StatsCounter:
    """
    Stats Counter class for the Receptionist Application
    Displays patient visit and revenue statistics in the top bar
    """
    
    def __init__(self, parent, patient_model):
        """
        Initialize the Stats Counter
        
        Args:
            parent: Parent widget
            patient_model: PatientModel instance
        """
        self.parent = parent
        self.patient_model = patient_model
        self.frame = ttk.Frame(parent)
        
        # Use the stats handler from the patient model
        self.stats_handler = patient_model.stats_handler
        
        # Create the UI
        self._create_ui()
        
        # Initial update
        self.update_stats()
    
    def _create_ui(self):
        """Create the user interface"""
        # Style for labels
        title_style = {'font': ('Arial', 9, 'bold')}
        value_style = {'font': ('Arial', 9)}
        
        # Create the stats frame with a border
        self.stats_frame = ttk.Frame(self.frame, relief=tk.RIDGE, borderwidth=1)
        self.stats_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        
        # Create the daily stats frame
        daily_frame = ttk.Frame(self.stats_frame)
        daily_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(daily_frame, text="TODAY:", **title_style).pack(side=tk.LEFT)
        self.daily_visits_label = ttk.Label(daily_frame, text="0 visits", **value_style)
        self.daily_visits_label.pack(side=tk.LEFT, padx=5)
        self.daily_revenue_label = ttk.Label(daily_frame, text="PKR 0", **value_style)
        self.daily_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.stats_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Create the weekly stats frame
        weekly_frame = ttk.Frame(self.stats_frame)
        weekly_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(weekly_frame, text="WEEK:", **title_style).pack(side=tk.LEFT)
        self.weekly_visits_label = ttk.Label(weekly_frame, text="0 visits", **value_style)
        self.weekly_visits_label.pack(side=tk.LEFT, padx=5)
        self.weekly_revenue_label = ttk.Label(weekly_frame, text="PKR 0", **value_style)
        self.weekly_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Separator
        ttk.Separator(self.stats_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        # Create the monthly stats frame
        monthly_frame = ttk.Frame(self.stats_frame)
        monthly_frame.pack(side=tk.LEFT, padx=10, pady=2)
        
        ttk.Label(monthly_frame, text="MONTH:", **title_style).pack(side=tk.LEFT)
        self.monthly_visits_label = ttk.Label(monthly_frame, text="0 visits", **value_style)
        self.monthly_visits_label.pack(side=tk.LEFT, padx=5)
        self.monthly_revenue_label = ttk.Label(monthly_frame, text="PKR 0", **value_style)
        self.monthly_revenue_label.pack(side=tk.LEFT, padx=5)
        
        # Refresh button
        self.refresh_btn = ttk.Button(self.stats_frame, text="↻", width=2, command=self.update_stats)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5, pady=2)
    
    def update_stats(self):
        """Update the statistics"""
        try:
            # Get current date
            now = datetime.now()
            today = now.strftime('%Y-%m-%d')
            
            # Get daily stats
            daily_stats = self.stats_handler.get_daily_stats(today)
            self.daily_visits_label.config(text=f"{daily_stats['visit_count']} visits")
            self.daily_revenue_label.config(text=f"PKR {daily_stats['revenue']:.2f}")
            
            # Get weekly stats
            weekly_stats = self.stats_handler.get_weekly_stats()
            self.weekly_visits_label.config(text=f"{weekly_stats['visit_count']} visits")
            self.weekly_revenue_label.config(text=f"PKR {weekly_stats['revenue']:.2f}")
            
            # Get monthly stats
            monthly_stats = self.stats_handler.get_monthly_stats()
            self.monthly_visits_label.config(text=f"{monthly_stats['visit_count']} visits")
            self.monthly_revenue_label.config(text=f"PKR {monthly_stats['revenue']:.2f}")
            
            logger.info(f"Updated stats: Daily={daily_stats['visit_count']} visits/PKR{daily_stats['revenue']:.2f}, " +
                       f"Weekly={weekly_stats['visit_count']} visits/PKR{weekly_stats['revenue']:.2f}, " +
                       f"Monthly={monthly_stats['visit_count']} visits/PKR{monthly_stats['revenue']:.2f}")
            
        except Exception as e:
            logger.error(f"Error updating stats: {e}") 