#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stats Handler for the Receptionist Application
Handles statistics calculations for patients and revenue
"""

import logging
import pandas as pd
from datetime import datetime, timedelta

logger = logging.getLogger('receptionist.stats_handler')

class StatsHandler:
    """
    Stats Handler class for the Receptionist Application
    Handles statistics calculations for patients and revenue
    """
    
    def __init__(self, excel_handler):
        """
        Initialize the Stats Handler
        
        Args:
            excel_handler: ExcelHandler instance
        """
        self.excel_handler = excel_handler
    
    def get_daily_stats(self, date=None):
        """
        Get daily statistics for patient visits and revenue
        
        Args:
            date (str, optional): Date in YYYY-MM-DD format. Defaults to today.
            
        Returns:
            dict: Dictionary with visit_count and revenue
        """
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
            
        try:
            # Get appointments for the date
            df = self.excel_handler.get_appointments_for_date(date)
            
            # Count visits
            visit_count = len(df)
            
            # Calculate revenue
            revenue = df['fees'].sum() if not df.empty else 0
            
            return {
                'date': date,
                'visit_count': visit_count,
                'revenue': revenue
            }
        except Exception as e:
            logger.error(f"Error getting daily stats: {e}")
            return {
                'date': date,
                'visit_count': 0,
                'revenue': 0
            }
    
    def get_weekly_stats(self, end_date=None):
        """
        Get weekly statistics for patient visits and revenue
        
        Args:
            end_date (str, optional): End date in YYYY-MM-DD format. Defaults to today.
            
        Returns:
            dict: Dictionary with visit_count and revenue
        """
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
            
        # Calculate start date (7 days before end date)
        start_date = end_date - timedelta(days=6)
        
        try:
            # Initialize counters
            visit_count = 0
            revenue = 0
            
            # Get stats for each day in the week
            current_date = start_date
            while current_date <= end_date:
                date_str = current_date.strftime('%Y-%m-%d')
                daily_stats = self.get_daily_stats(date_str)
                
                visit_count += daily_stats['visit_count']
                revenue += daily_stats['revenue']
                
                current_date += timedelta(days=1)
            
            return {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'visit_count': visit_count,
                'revenue': revenue
            }
        except Exception as e:
            logger.error(f"Error getting weekly stats: {e}")
            return {
                'start_date': start_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'visit_count': 0,
                'revenue': 0
            }
    
    def get_monthly_stats(self, year=None, month=None):
        """
        Get monthly statistics for patient visits and revenue
        
        Args:
            year (int, optional): Year. Defaults to current year.
            month (int, optional): Month (1-12). Defaults to current month.
            
        Returns:
            dict: Dictionary with visit_count and revenue
        """
        if year is None or month is None:
            now = datetime.now()
            year = now.year
            month = now.month
            
        try:
            # Get all patients
            df = self.excel_handler.get_all_patients()
            
            # Filter by month and year
            df['appointment_date'] = pd.to_datetime(df['appointment_date'])
            monthly_df = df[
                (df['appointment_date'].dt.year == year) & 
                (df['appointment_date'].dt.month == month)
            ]
            
            # Count visits
            visit_count = len(monthly_df)
            
            # Calculate revenue
            revenue = monthly_df['fees'].sum() if not monthly_df.empty else 0
            
            return {
                'year': year,
                'month': month,
                'visit_count': visit_count,
                'revenue': revenue
            }
        except Exception as e:
            logger.error(f"Error getting monthly stats: {e}")
            return {
                'year': year,
                'month': month,
                'visit_count': 0,
                'revenue': 0
            } 