#!/usr/bin/env python3
"""
Test script for BC-98AC thermal printer
"""

import json
from escpos.printer import Usb

def test_printer():
    try:
        # Load settings
        with open('src/config/settings.json', 'r') as f:
            settings = json.load(f)
        
        # Get printer settings
        printer_settings = settings.get('printer_settings', {})
        vendor_id = int(printer_settings.get('vendor_id', '0x0483'), 16)
        product_id = int(printer_settings.get('product_id', '0x5740'), 16)
        
        # Try to connect to printer
        print(f"Attempting to connect to printer (Vendor ID: {vendor_id:04x}, Product ID: {product_id:04x})...")
        printer = Usb(vendor_id, product_id)
        
        # Print test page
        printer.set(align='center', font='a', width=2, height=2)
        printer.text("\nTest Page\n\n")
        printer.set(align='center', font='a', width=1, height=1)
        printer.text("If you can read this,\nthe printer is working!\n\n")
        printer.text("="*32 + "\n")
        printer.text("Printer Information:\n")
        printer.text(f"Vendor ID: {vendor_id:04x}\n")
        printer.text(f"Product ID: {product_id:04x}\n")
        printer.text("="*32 + "\n\n")
        printer.cut()
        
        print("Test page sent to printer successfully!")
        return True
        
    except ImportError:
        print("Error: python-escpos package not installed")
        print("Please install it using: pip install python-escpos")
        return False
    except Exception as e:
        print(f"Error connecting to printer: {str(e)}")
        print("\nTroubleshooting steps:")
        print("1. Make sure the printer is connected and powered on")
        print("2. Verify the vendor_id and product_id in settings.json")
        print("3. Check if you have permission to access the USB device")
        print("4. Try unplugging and reconnecting the printer")
        return False

if __name__ == "__main__":
    test_printer() 