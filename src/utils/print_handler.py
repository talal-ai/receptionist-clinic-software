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
from tkinter import messagebox

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
        
        # Add custom filter for date formatting
        self.jinja_env.filters['format_date'] = self.format_date
        
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
    <title>Reception Slip</title>
    <style>
        @page {
            size: A5;
            margin: 5mm;
        }
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            font-size: 10pt;
            color: #000;
            line-height: 1.2;
        }
        .header {
            text-align: center;
            margin-bottom: 8px;
            border-bottom: 1px solid #000;
            padding-bottom: 5px;
        }
        .header h1 {
            font-size: 14pt;
            color: #000;
            margin: 0 0 3px 0;
            font-weight: bold;
        }
        .qualifications {
            font-size: 9pt;
            color: #000;
            margin: 2px 0;
            font-weight: normal;
        }
        .contact-info {
            font-size: 8pt;
            color: #000;
            margin: 2px 0;
        }
        .phone-numbers {
            font-size: 8pt;
            margin: 1px 0;
        }
        .patient-info {
            margin: 5px 0;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        table td {
            padding: 2px 3px;
            font-size: 9pt;
            border-bottom: 1px solid #eee;
        }
        .label {
            font-weight: bold;
            width: 35%;
            color: #000;
        }
        .value {
            color: #000;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Dr. Muhammad Sajid Sohail</h1>
        <div class="qualifications">
            Consultant Physician<br>
            MBBS (K.E), FCPS (Medicine)
        </div>
        <div class="contact-info">
            <div class="phone-numbers">
                Cell: 0300-5809938<br>
                Cell: 0347-9809938
            </div>
        </div>
    </div>
    
    <div class="patient-info">
        <table>
            <tr>
                <td class="label">Token Number:</td>
                <td class="value">{{ token_number }}</td>
            </tr>
            <tr>
                <td class="label">Date:</td>
                <td class="value">{{ appointment_date }}</td>
            </tr>
            <tr>
                <td class="label">Patient Name:</td>
                <td class="value">{{ patient_name }}</td>
            </tr>
            <tr>
                <td class="label">Status:</td>
                <td class="value">{{ status }}</td>
            </tr>
            <tr>
                <td class="label">Time Arrival:</td>
                <td class="value">{{ arrival_time }}</td>
            </tr>
            <tr>
                <td class="label">Checkup Time:</td>
                <td class="value">{{ appointment_time }}</td>
            </tr>
            <tr>
                <td class="label">Fees:</td>
                <td class="value">{% if fees %}PKR {{ fees }}{% else %}Not specified{% endif %}</td>
            </tr>
            {% if remarks and remarks.strip() %}
            <tr>
                <td class="label">Remarks:</td>
                <td class="value">{{ remarks }}</td>
            </tr>
            {% endif %}
        </table>
    </div>
</body>
</html>''')
            logger.info(f"Created default template at {default_template_path}")
    
    def format_date(self, date_str):
        """
        Format a date string to DD-MM-YYYY format
        
        Args:
            date_str (str): Date string in any format
            
        Returns:
            str: Formatted date string in DD-MM-YYYY format
        """
        try:
            # Try to parse the date string
            # First try ISO format (YYYY-MM-DD)
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d')
            except ValueError:
                # Then try other common formats
                try:
                    date_obj = datetime.strptime(date_str, '%d/%m/%Y')
                except ValueError:
                    try:
                        date_obj = datetime.strptime(date_str, '%m/%d/%Y')
                    except ValueError:
                        # If all parsing attempts fail, return the original string
                        return date_str
            
            # Format to DD-MM-YYYY
            return date_obj.strftime('%d-%m-%Y')
        except Exception:
            # Return the original string if any error occurs
            return date_str
    
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
        
        # Convert 24-hour times to AM/PM format
        appointment_time = patient_data.get('appointment_time', '')
        arrival_time = patient_data.get('arrival_time', '')
        
        # Convert appointment time (checkup time) to AM/PM format if in 24-hour format
        if appointment_time and ':' in appointment_time and len(appointment_time) <= 5:
            try:
                hour, minute = map(int, appointment_time.split(':'))
                if hour == 0:
                    appointment_time = f"12:{minute:02d} AM"
                elif hour < 12:
                    appointment_time = f"{hour}:{minute:02d} AM"
                elif hour == 12:
                    appointment_time = f"12:{minute:02d} PM"
                else:
                    appointment_time = f"{hour-12}:{minute:02d} PM"
            except:
                pass  # Keep original if conversion fails
        
        # Convert arrival time to AM/PM format if in 24-hour format
        if arrival_time and ':' in arrival_time and len(arrival_time) <= 5:
            try:
                hour, minute = map(int, arrival_time.split(':'))
                if hour == 0:
                    arrival_time = f"12:{minute:02d} AM"
                elif hour < 12:
                    arrival_time = f"{hour}:{minute:02d} AM"
                elif hour == 12:
                    arrival_time = f"12:{minute:02d} PM"
                else:
                    arrival_time = f"{hour-12}:{minute:02d} PM"
            except:
                pass  # Keep original if conversion fails
        
        # Format the appointment date to DD-MM-YY
        appointment_date = patient_data.get('appointment_date', '')
        appointment_date = self.format_date(appointment_date)
        
        # Prepare the data for the template
        template_data = {
            'clinic_name': 'Dr. Muhammad Sajid Sohail',
            'token_number': patient_data.get('token_number', ''),
            'patient_name': f"{patient_data.get('first_name', '')} {patient_data.get('last_name', '')}".strip(),
            'status': patient_data.get('status', 'New'),
            'appointment_date': appointment_date,
            'arrival_time': arrival_time,  # Time arrival in AM/PM format
            'appointment_time': appointment_time,  # Checkup time in AM/PM format
            'fees': patient_data.get('fees', ''),
            'remarks': patient_data.get('remarks', patient_data.get('notes', '')),  # Get remarks or fall back to notes
            'generated_date': self.format_date(datetime.now().strftime('%Y-%m-%d')),
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
                    'margin-top': '5mm',
                    'margin-right': '5mm',
                    'margin-bottom': '5mm',
                    'margin-left': '5mm',
                    'encoding': 'UTF-8',
                    'quiet': '',
                    'disable-smart-shrinking': '',
                    'print-media-type': ''
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
        Print a PDF reception slip directly to printer without opening browser
        
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
            
            # Direct printing to Windows printer without opening browser
            try:
                import win32api
                import win32print
                import win32con
                
                # Get default printer if none specified
                if not printer_name:
                    printer_name = win32print.GetDefaultPrinter()
                
                # Method 1: Direct PDF printing using ShellExecute with SW_HIDE
                try:
                    result = win32api.ShellExecute(
                        0, 
                        "print", 
                        pdf_path,
                        f'/d:"{printer_name}"' if printer_name else None,
                        ".", 
                        win32con.SW_HIDE  # Hide the window completely
                    )
                    
                    if result > 32:  # Success
                        logger.info(f"PDF sent directly to printer: {printer_name or 'Default'}")
                        return True
                    else:
                        logger.warning(f"ShellExecute failed with code: {result}")
                        
                except Exception as shell_error:
                    logger.warning(f"ShellExecute method failed: {shell_error}")
                
                # Method 2: Alternative direct printing using win32print
                try:
                    # Open the PDF file
                    with open(pdf_path, 'rb') as pdf_file:
                        pdf_data = pdf_file.read()
                    
                    # Get printer handle
                    printer_handle = win32print.OpenPrinter(printer_name)
                    
                    # Start print job
                    job_info = win32print.StartDocPrinter(printer_handle, 1, ("Reception Slip", None, "RAW"))
                    win32print.StartPagePrinter(printer_handle)
                    
                    # Write PDF data to printer
                    win32print.WritePrinter(printer_handle, pdf_data)
                    
                    # End print job
                    win32print.EndPagePrinter(printer_handle)
                    win32print.EndDocPrinter(printer_handle)
                    win32print.ClosePrinter(printer_handle)
                    
                    logger.info(f"PDF sent directly to printer using win32print: {printer_name}")
                    return True
                    
                except Exception as win32_error:
                    logger.warning(f"win32print method failed: {win32_error}")
                    
                    # Method 3: Fallback to default application printing (hidden)
                    win32api.ShellExecute(
                        0, 
                        "print", 
                        pdf_path,
                        None,
                        ".", 
                        win32con.SW_HIDE
                    )
                    logger.info(f"PDF sent to default application for printing: {pdf_path}")
                    return True
                    
            except ImportError:
                logger.warning("pywin32 not installed. Please install with: pip install pywin32")
                messagebox.showwarning(
                    "Printer Setup Required",
                    "Please install pywin32 package for direct printing:\n\npip install pywin32"
                )
                return False
            except Exception as e:
                logger.error(f"Error sending to printer: {e}")
                return False
                
        except Exception as e:
            logger.error(f"Error printing PDF: {e}")
            return False
    
    def print_reception_slip(self, patient_data):
        """
        Generate and print a reception slip for a patient.
        This function will decide whether to use the thermal printer
        or the standard PDF/HTML printing method based on settings.
        """
        # Check if thermal printer is enabled (check both locations for compatibility)
        use_thermal = (self.settings.get('use_thermal_printer', False) or 
                      self.settings.get('printer_settings', {}).get('use_thermal_printer', False))
        
        if use_thermal:
            logger.info("Thermal printer is enabled in settings, attempting thermal print...")
            try:
                return self._print_thermal_receipt(patient_data)
            except Exception as e:
                logger.error(f"Failed to print thermal receipt: {e}")
                logger.info("Falling back to direct PDF printing...")
                
                # Fallback to direct PDF printing when thermal fails
                try:
                    return self._print_direct_pdf(patient_data)
                except Exception as pdf_error:
                    logger.error(f"Direct PDF printing also failed: {pdf_error}")
                    messagebox.showerror("Printing Error", 
                                       f"Both thermal and PDF printing failed.\n\n"
                                       f"Thermal error: {e}\nPDF error: {pdf_error}")
                    return False
        
        # Otherwise, use direct PDF printing for professional experience
        try:
            logger.info("Using direct PDF printing for professional experience...")
            return self._print_direct_pdf(patient_data)
        except Exception as e:
            logger.error(f"Error in direct PDF printing: {e}")
            messagebox.showerror("Printing Error", f"An error occurred during direct PDF printing: {e}")
            return False

    def _print_direct_pdf(self, patient_data):
        """
        Print reception slip directly to printer without opening browser or showing dialogs.
        This is the professional method for production environments.
        
        Args:
            patient_data (dict): Patient data
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            logger.info("Starting direct PDF printing process...")
            
            # Generate PDF first
            output_path = self.generate_pdf(patient_data)
            if not output_path:
                logger.error("Failed to generate PDF for direct printing")
                return False
            
            # Try multiple direct printing methods
            success = False
            
            # Method 1: Direct PDF printing with win32api (hidden)
            try:
                import win32api
                import win32print
                import win32con
                
                printer_name = self.settings.get('printer_name', '')
                if not printer_name:
                    printer_name = win32print.GetDefaultPrinter()
                
                # Use ShellExecute with SW_HIDE for completely silent printing
                result = win32api.ShellExecute(
                    0, 
                    "print", 
                    output_path,
                    f'/d:"{printer_name}"' if printer_name else None,
                    ".", 
                    win32con.SW_HIDE
                )
                
                if result > 32:
                    logger.info("Direct PDF printing successful using ShellExecute")
                    success = True
                else:
                    logger.warning(f"ShellExecute direct printing failed with code: {result}")
                    
            except Exception as e:
                logger.warning(f"Direct printing method 1 failed: {e}")
            
            # Method 2: Alternative direct printing using subprocess
            if not success:
                try:
                    import subprocess
                    import sys
                    
                    printer_name = self.settings.get('printer_name', '')
                    
                    if sys.platform == "win32":
                        # Windows: Use PowerShell for silent printing
                        if printer_name:
                            cmd = f'powershell -Command "Get-Content \'{output_path}\' | Out-Printer -Name \'{printer_name}\'"'
                        else:
                            cmd = f'powershell -Command "Get-Content \'{output_path}\' | Out-Printer"'
                        
                        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
                        if result.returncode == 0:
                            logger.info("Direct PDF printing successful using PowerShell")
                            success = True
                        else:
                            logger.warning(f"PowerShell direct printing failed: {result.stderr}")
                    else:
                        # Linux/Mac: Use lp command
                        if printer_name:
                            cmd = ['lp', '-d', printer_name, output_path]
                        else:
                            cmd = ['lp', output_path]
                        
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        if result.returncode == 0:
                            logger.info("Direct PDF printing successful using lp command")
                            success = True
                        else:
                            logger.warning(f"lp command direct printing failed: {result.stderr}")
                            
                except Exception as e:
                    logger.warning(f"Direct printing method 2 failed: {e}")
            
            # Method 3: Fallback to regular direct printing
            if not success:
                logger.info("Falling back to regular direct printing...")
                success = self.print_pdf(output_path)
            
            # Clean up temporary file
            try:
                if os.path.exists(output_path):
                    os.unlink(output_path)
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up temporary file: {cleanup_error}")
            
            if success:
                logger.info("Direct PDF printing completed successfully!")
            else:
                logger.error("All direct printing methods failed")
                
            return success
            
        except Exception as e:
            logger.error(f"Error in direct PDF printing: {e}")
            return False

    def _print_thermal_receipt(self, patient_data):
        """
        Prints a formatted receipt directly to a thermal printer using python-escpos.
        """
        try:
            from escpos.printer import Usb
        except ImportError:
            logger.warning("python-escpos is not installed. Please run: pip install python-escpos")
            messagebox.showwarning(
                "Dependency Missing",
                "The 'python-escpos' library is required for thermal printing. Please install it."
            )
            return False

        # Get printer configuration from settings
        printer_settings = self.settings.get('printer_settings', {})
        vendor_id = int(printer_settings.get('vendor_id', '0x0483'), 16)
        product_id = int(printer_settings.get('product_id', '0x5740'), 16)

        try:
            # Initialize the printer
            printer = Usb(vendor_id, product_id)
        except Exception as e:
            logger.error(f"Could not initialize thermal printer: {e}")
            messagebox.showerror(
                "Printer Connection Error",
                f"Failed to connect to the thermal printer. Please check if it's connected and powered on.\n\nError: {e}"
            )
            return False

        # Generate the data for printing
        _, template_data = self.generate_html(patient_data)

        # --- Start Printing ---
        # Header with doctor information from settings
        doctor_name = self.settings.get('default_doctor', 'Dr. Muhammad Sajid Sohail')
        doctor_qualifications = self.settings.get('doctor_qualifications', 'Consultant Physician\nMBBS (K.E), FCPS (Medicine)')
        doctor_phones = self.settings.get('doctor_phones', ['0300-5809938', '0347-9809938'])
        
        printer.set(align='center', font='a', bold=True, width=1, height=1)
        printer.text(f"{doctor_name}\n")

        printer.set(align='center', font='b', bold=False, width=1, height=1)
        # Print each qualification line
        for line in doctor_qualifications.split('\n'):
            printer.text(f"{line}\n")
        
        # Print phone numbers
        printer.set(align='center', font='b', bold=False, width=1, height=1)
        for phone in doctor_phones:
            printer.text(f"Cell: {phone}\n")
        
        printer.text("-" * 42 + "\n")

        # Patient and Token Details
        printer.set(align='left', font='a', bold=True)
        printer.text(f"Token Number: {template_data.get('token_number', 'N/A')}\n")
        
        printer.set(align='left', font='a', bold=False)
        printer.text(f"Date: {template_data.get('appointment_date', 'N/A')}\n")
        printer.text(f"Patient Name: {template_data.get('patient_name', 'N/A')}\n")
        printer.text(f"Status: {template_data.get('status', 'N/A')}\n")
        printer.text(f"Time Arrival: {template_data.get('arrival_time', 'N/A')}\n")
        printer.text(f"Checkup Time: {template_data.get('appointment_time', 'N/A')}\n")
        printer.text(f"Fees: PKR {template_data.get('fees', 'N/A')}\n")
        
        # Add remarks if present
        if template_data.get('remarks') and template_data.get('remarks').strip():
            printer.text(f"Remarks: {template_data.get('remarks')}\n")

        printer.text("\n")

        # Footer
        printer.set(align='center', font='b')
        printer.text(f"Generated on {template_data.get('generated_date')} at {template_data.get('generated_time')}\n")
        printer.text("Thank you for trusting Dr. Sajid Sohail\n")

        # Cut the paper
        printer.cut()
        
        logger.info("Successfully printed receipt to thermal printer.")
        return True

    def preview_thermal_receipt(self, patient_data):
        """
        Generates a text preview of what would be printed on a thermal receipt
        and saves it to a file without opening browser.
        """
        _, template_data = self.generate_html(patient_data)

        # --- Build Receipt String ---
        # The width is set to 42 characters for a standard 80mm receipt paper.
        width = 42
        lines = []

        # Header with doctor information from settings
        doctor_name = self.settings.get('default_doctor', 'Dr. Muhammad Sajid Sohail')
        doctor_qualifications = self.settings.get('doctor_qualifications', 'Consultant Physician\nMBBS (K.E), FCPS (Medicine)')
        doctor_phones = self.settings.get('doctor_phones', ['0300-5809938', '0347-9809938'])
        
        lines.append(doctor_name.center(width))
        lines.append("")
        
        # Add qualifications
        for line in doctor_qualifications.split('\n'):
            lines.append(line.center(width))
        lines.append("")
        
        # Add phone numbers
        for phone in doctor_phones:
            lines.append(f"Cell: {phone}".center(width))
        
        # Add a separator
        lines.append("-" * width)

        # Patient and Token Details (left-aligned)
        lines.append(f"Token Number: {template_data.get('token_number', 'N/A')}")
        lines.append(f"Date: {template_data.get('appointment_date', 'N/A')}")
        lines.append(f"Patient Name: {template_data.get('patient_name', 'N/A')}")
        lines.append(f"Status: {template_data.get('status', 'N/A')}")
        lines.append(f"Time Arrival: {template_data.get('arrival_time', 'N/A')}")
        lines.append(f"Checkup Time: {template_data.get('appointment_time', 'N/A')}")
        lines.append(f"Fees: PKR {template_data.get('fees', 'N/A')}")
        
        # Add remarks if present
        if template_data.get('remarks') and template_data.get('remarks').strip():
            lines.append(f"Remarks: {template_data.get('remarks')}")
        lines.append("")

        # Footer (centered)
        generated_line = f"Generated on {template_data.get('generated_date')} at {template_data.get('generated_time')}"
        lines.append(generated_line.center(width))
        thank_you_line = f"Thank you for trusting {template_data.get('clinic_name')}"
        lines.append(thank_you_line.center(width))

        receipt_content = "\n".join(lines)

        try:
            # Save to a temporary file
            with tempfile.NamedTemporaryFile('w', delete=False, suffix='.txt', encoding='utf-8') as f:
                f.write(receipt_content)
                temp_path = f.name
            
            # Log the preview location instead of opening browser
            logger.info(f"Generated thermal receipt preview at: {temp_path}")
            logger.info("Thermal printer preview saved to file (no browser opened)")
            return True
        except Exception as e:
            logger.error(f"Failed to generate thermal preview: {e}")
            messagebox.showerror("Preview Error", f"Could not generate the preview file.\n\nError: {e}")
            return False