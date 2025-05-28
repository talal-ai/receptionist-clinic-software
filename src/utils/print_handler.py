#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Print Handler for the Receptionist Application
Handles generating and printing reception slips
"""

import os
import logging
import tempfile
from datetime import datetime
from pathlib import Path
import webbrowser
import jinja2
import pdfkit

logger = logging.getLogger('receptionist.print_handler')

class PrintHandler:
    """
    Print Handler class for the Receptionist Application
    Handles generating and printing reception slips
    """
    
    def __init__(self, settings):
        """
        Initialize the Print Handler
        
        Args:
            settings: Application settings
        """
        self.settings = settings
        self.template_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'templates')
        
        # Ensure template directory exists
        os.makedirs(self.template_dir, exist_ok=True)
        
        # Create default template if it doesn't exist
        self._ensure_default_template()
        
        # Set up the Jinja2 environment
        self.jinja_env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(self.template_dir),
            autoescape=True
        )
        
        # Check if wkhtmltopdf is available
        try:
            pdfkit.configuration()
            self.pdf_available = True
        except Exception:
            self.pdf_available = False
            logger.warning("wkhtmltopdf not found. Falling back to HTML output.")
    
    def _ensure_default_template(self):
        """Ensure the default template exists"""
        default_template_path = os.path.join(self.template_dir, 'default_template.html')
        
        if not os.path.exists(default_template_path):
            # Create the default template
            with open(default_template_path, 'w', encoding='utf-8') as f:
                f.write('''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>{{ clinic_name }} - Reception Slip</title>
    <style>
        @page {
            size: A5;
            margin: 10mm;
        }
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            font-size: 12pt;
        }
        .header {
            text-align: center;
            margin-bottom: 15px;
            border-bottom: 1px solid #333;
            padding-bottom: 10px;
        }
        .header h1 {
            font-size: 18pt;
            color: #0066cc;
            margin: 5px 0;
        }
        .header .logo {
            max-width: 150px;
            max-height: 60px;
        }
        .header p {
            margin: 5px 0;
            font-size: 10pt;
        }
        .content {
            margin: 15px 0;
        }
        .content h2 {
            font-size: 14pt;
            color: #0066cc;
            margin: 10px 0;
        }
        .patient-info, .appointment-info {
            margin-bottom: 15px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table td {
            padding: 5px;
        }
        .label {
            font-weight: bold;
            width: 40%;
        }
        .footer {
            margin-top: 20px;
            text-align: center;
            font-size: 10pt;
            color: #666;
            border-top: 1px solid #ddd;
            padding-top: 10px;
        }
        .barcode {
            text-align: center;
            margin: 15px 0;
        }
        .instructions {
            font-size: 10pt;
            margin-top: 15px;
            padding: 10px;
            border: 1px solid #ddd;
            background-color: #f9f9f9;
        }
    </style>
</head>
<body>
    <div class="header">
        {% if logo_path %}
        <img src="{{ logo_path }}" alt="{{ clinic_name }} Logo" class="logo">
        {% endif %}
        <h1>{{ clinic_name }}</h1>
        <p>{{ clinic_address }}</p>
        <p>Tel: {{ clinic_phone }}</p>
    </div>
    
    <div class="content">
        <h2>Reception Slip</h2>
        
        <div class="patient-info">
            <table>
                <tr>
                    <td class="label">Patient ID:</td>
                    <td>{{ patient_id }}</td>
                </tr>
                <tr>
                    <td class="label">Name:</td>
                    <td>{{ patient_name }}</td>
                </tr>
                <tr>
                    <td class="label">Phone:</td>
                    <td>{{ phone_number }}</td>
                </tr>
            </table>
        </div>
        
        <div class="appointment-info">
            <table>
                <tr>
                    <td class="label">Doctor:</td>
                    <td>{{ doctor_name }}</td>
                </tr>
                <tr>
                    <td class="label">Date:</td>
                    <td>{{ appointment_date }}</td>
                </tr>
                <tr>
                    <td class="label">Time:</td>
                    <td>{{ appointment_time }}</td>
                </tr>
                <tr>
                    <td class="label">Duration:</td>
                    <td>{{ appointment_duration }} minutes</td>
                </tr>
                <tr>
                    <td class="label">Fees:</td>
                    <td>{% if fees %}PKR {{ fees }}{% else %}Not specified{% endif %}</td>
                </tr>
                <tr>
                    <td class="label">Reason for Visit:</td>
                    <td>{{ reason_for_visit }}</td>
                </tr>
            </table>
        </div>
        
        {% if barcode %}
        <div class="barcode">
            <img src="{{ barcode }}" alt="Patient Barcode">
        </div>
        {% endif %}
        
        <div class="instructions">
            <p><strong>Please Note:</strong></p>
            <ul>
                <li>Please arrive 10 minutes before your appointment time.</li>
                <li>Bring any relevant medical records or test results.</li>
                <li>If you need to cancel or reschedule, please call at least 24 hours in advance.</li>
            </ul>
        </div>
    </div>
    
    <div class="footer">
        <p>This slip was generated on {{ generated_date }} at {{ generated_time }}</p>
        <p>Thank you for choosing {{ clinic_name }}</p>
    </div>
</body>
</html>''')
            logger.info(f"Created default template at {default_template_path}")
    
    def generate_html(self, patient_data):
        """
        Generate HTML content for a reception slip
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            tuple: (html_content, template_data)
        """
        # Get the template
        template_name = self.settings.get('receipt_template', 'default_template.html')
        template = self.jinja_env.get_template(template_name)
        
        # Prepare the data for the template
        template_data = {
            'clinic_name': self.settings.get('company_name', 'Doctor Clinic'),
            'clinic_address': self.settings.get('clinic_address', '123 Medical St, Health City'),
            'clinic_phone': self.settings.get('clinic_phone', '123-456-7890'),
            'logo_path': self.settings.get('logo_path', ''),
            'patient_id': patient_data.get('patient_id', ''),
            'patient_name': f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}",
            'phone_number': patient_data.get('phone_number', ''),
            'doctor_name': patient_data.get('doctor_name', ''),
            'appointment_date': patient_data.get('appointment_date', ''),
            'appointment_time': patient_data.get('appointment_time', ''),
            'appointment_duration': patient_data.get('appointment_duration', 
                                                  self.settings.get('appointment_duration_mins', 30)),
            'fees': patient_data.get('fees', ''),
            'reason_for_visit': patient_data.get('reason_for_visit', ''),
            'barcode': '',  # Can be implemented later if needed
            'generated_date': datetime.now().strftime(self.settings.get('date_format', '%Y-%m-%d')),
            'generated_time': datetime.now().strftime(self.settings.get('time_format', '%H:%M'))
        }
        
        # Render the template
        html_content = template.render(**template_data)
        return html_content, template_data
    
    def generate_pdf(self, patient_data, output_path=None):
        """
        Generate a PDF reception slip for a patient
        
        Args:
            patient_data (dict): Patient data
            output_path (str, optional): Path to save the PDF. Defaults to a temp file.
            
        Returns:
            str: Path to the generated PDF or HTML
        """
        try:
            # Generate HTML content
            html_content, _ = self.generate_html(patient_data)
            
            # Determine the output path
            if output_path is None:
                # Create a temporary file
                fd, output_path = tempfile.mkstemp(suffix='.pdf')
                os.close(fd)
            
            # If PDF generation is available, use it
            if self.pdf_available:
                # Convert HTML to PDF
                options = {
                    'page-size': 'A5',
                    'margin-top': '10mm',
                    'margin-right': '10mm',
                    'margin-bottom': '10mm',
                    'margin-left': '10mm',
                    'encoding': 'UTF-8',
                    'quiet': ''
                }
                
                pdfkit.from_string(html_content, output_path, options=options)
                logger.info(f"Generated PDF at {output_path}")
            else:
                # Fallback to HTML
                output_path = output_path.replace('.pdf', '.html')
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Generated HTML at {output_path} (PDF fallback)")
            
            return output_path
        except Exception as e:
            logger.error(f"Error generating PDF: {e}")
            
            # If an error occurs during PDF generation, try falling back to HTML
            try:
                html_content, _ = self.generate_html(patient_data)
                html_path = tempfile.mkstemp(suffix='.html')[1]
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                logger.info(f"Fallback: Generated HTML at {html_path}")
                return html_path
            except Exception as html_error:
                logger.error(f"Error in HTML fallback: {html_error}")
                raise e
    
    def print_pdf(self, pdf_path, printer_name=None):
        """
        Print a PDF reception slip
        
        Args:
            pdf_path (str): Path to the PDF file
            printer_name (str, optional): Name of the printer. Defaults to system default.
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Use the printer name from settings if not provided
            if printer_name is None:
                printer_name = self.settings.get('printer_name', '')
            
            # Print the PDF - this is platform dependent
            # On Windows, you might use a command like:
            # os.system(f'SumatraPDF.exe -print-to "{printer_name}" "{pdf_path}"')
            
            # For now, just open the PDF in the default viewer
            # The user can print from there
            webbrowser.open(pdf_path)
            logger.info(f"Opened file for printing: {pdf_path}")
            
            return True
        except Exception as e:
            logger.error(f"Error printing PDF: {e}")
            return False
    
    def print_reception_slip(self, patient_data):
        """
        Generate and print a reception slip for a patient
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Generate the PDF or HTML
            output_path = self.generate_pdf(patient_data)
            
            # Print the file
            success = self.print_pdf(output_path)
            
            return success
        except Exception as e:
            logger.error(f"Error printing reception slip: {e}")
            
            # One final fallback attempt - generate HTML directly and open in browser
            try:
                html_content, _ = self.generate_html(patient_data)
                
                # Save to a temporary file
                with tempfile.NamedTemporaryFile('w', delete=False, suffix='.html', encoding='utf-8') as f:
                    f.write(html_content)
                    temp_path = f.name
                
                # Open in browser
                webbrowser.open(f'file://{temp_path}')
                logger.info(f"Emergency fallback: Opened HTML at {temp_path}")
                return True
            except Exception as html_error:
                logger.error(f"Error in emergency HTML fallback: {html_error}")
                return False 