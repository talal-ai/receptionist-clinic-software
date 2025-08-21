# Printer Configuration Guide 🖨️

## Step 1: Find Your Printer's USB Details

1. Connect your BC-98AC printer to your computer
2. Open Device Manager:
   - Press `Windows Key + X`
   - Click "Device Manager"

3. Look for your printer under:
   - "Ports (COM & LPT)" or
   - "Universal Serial Bus controllers"

4. Right-click the printer and select "Properties"
5. Go to "Details" tab
6. In the dropdown, select "Hardware Ids"
7. You'll see something like:
   ```
   USB\VID_0483&PID_5740
   ```
   - The number after VID_ is your Vendor ID
   - The number after PID_ is your Product ID

## Step 2: Update Settings File

1. Go to your application folder
2. Open: `src/config/settings.json`
3. Find the printer_settings section:
   ```json
   "printer_settings": {
       "use_thermal_printer": true,
       "printer_name": "BC-98AC",
       "vendor_id": "0x0483",    👈 Update this
       "product_id": "0x5740",   👈 Update this
       "interface": 0
   }
   ```
4. Update the vendor_id and product_id with your values
   - Add "0x" before the numbers you found
   - Example: If you found VID_0483, enter "0x0483"

## Step 3: Test the Printer

1. Open Command Prompt/PowerShell in your application folder
2. Run the test script:
   ```
   python test_printer.py
   ```
3. The printer should print a test page

## Common Issues

### If Test Print Fails:
1. Check printer is powered on
2. Check USB connection
3. Double-check the IDs in settings.json
4. Try unplugging and reconnecting the printer

### If Numbers Don't Match:
Sometimes the printer might have different IDs. Common values are:
- vendor_id: "0x0483", "0x0416", "0x0425", "0x04b8"
- product_id: "0x5740", "0x5011", "0x0006"

Try these combinations if the default doesn't work.

## Need Help?

If you're having trouble:
1. Take a photo of your Device Manager showing the printer properties
2. Note down any error messages
3. Contact technical support with this information

## Important Notes

- Don't change other settings unless instructed
- Keep a backup of the original settings.json file
- The printer must be connected before starting the application
- If you change printers, you'll need to update these settings again 