# Printer Setup Guide 🖨️

## Prerequisites

1. **Python Requirements**
   ```bash
   pip install -r requirements.txt
   ```

2. **wkhtmltopdf Installation**
   - Download from: https://wkhtmltopdf.org/downloads.html
   - Install according to your operating system
   - Add to system PATH during installation

3. **Thermal Printer Setup (BC-98AC)**
   
   ### Windows
   1. Connect the BC-98AC printer via USB
   2. Windows should automatically install basic drivers
   3. Install printer manufacturer drivers if provided


## Configuration

The printer settings are in `src/config/settings.json`:

```json
"printer_settings": {
    "use_thermal_printer": true,
    "printer_name": "BC-98AC",
    "vendor_id": "0x0483",
    "product_id": "0x5740",
    "interface": 0
}
```

If the printer doesn't work with these default IDs:

1. **Windows**: Find correct IDs in Device Manager
   - Open Device Manager
   - Find the printer under "Ports" or "USB controllers"
   - Properties → Details → Hardware Ids
   - Look for VID_ and PID_ values



## Testing the Printer

1. Open the application
2. Add a test patient
3. Click "Print Reception Slip"
4. The application will:
   - Try to print directly to thermal printer
   - If that fails, open PDF in browser
   - If PDF fails, open HTML in browser

## Troubleshooting

1. **Printer Not Found**
   - Check USB connection
   - Verify printer is powered on
   - Confirm vendor_id and product_id in settings.json
   - Try unplugging and reconnecting the printer

2. **Permission Issues**
   - Windows: Run as Administrator
   - Linux: Check udev rules and user groups

3. **Print Quality Issues**
   - Check paper is properly loaded
   - Verify paper type matches printer specifications
   - Clean printer head if necessary

4. **Fallback Options**
   If thermal printing fails, the system will:
   1. Try to generate and print PDF
   2. If PDF fails, generate and show HTML
   3. Both PDF and HTML can be printed from browser

## Default Template

The default receipt template is in `src/resources/templates/default_template.html`
- Can be customized for clinic branding
- Supports logo, clinic details, and custom styling
- Changes apply to both thermal and PDF/HTML printing

## Support

For technical support:
1. Check application logs in the `logs` directory
2. Contact system administrator
3. Refer to printer manual for hardware-specific issues 