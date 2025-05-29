# 🏥 Clinic Receptionist Software

A modern desktop application for efficiently managing patient appointments and printing reception slips in a doctor's clinic. Designed to streamline front-desk operations and improve patient experience.

## ✨ Features

- 📝 Patient registration and management
- 🗓️ Intuitive appointment scheduling interface
- 🔍 Quick patient search by name
- 📅 Daily, weekly, and monthly appointment views
- 🖨️ One-click reception slip printing
- 💾 Automatic data backup and recovery
- 📊 Excel-based data storage for easy management
- 🔒 Simple yet effective data security

## 🛠️ Technical Requirements

- Python 3.7 or higher
- Tkinter (included with most Python installations)
- pandas (data manipulation)
- openpyxl (Excel file handling)
- tkcalendar (calendar widget)
- pdfkit (PDF generation)
- Jinja2 (HTML templating)
- wkhtmltopdf (optional, for enhanced PDF generation)

## 📋 Installation

1. Clone this repository or download the source code:
   ```
   git clone https://github.com/yourusername/receptionist.git
   cd receptionist
   ```

2. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```

3. For PDF generation (optional):
   Install wkhtmltopdf:
   - **Windows**: Download and install from [wkhtmltopdf.org](https://wkhtmltopdf.org/downloads.html)
   - **macOS**: `brew install wkhtmltopdf`
   - **Linux**: `sudo apt-get install wkhtmltopdf`
   
   Note: If wkhtmltopdf is not installed, the application will fall back to generating HTML reception slips that can be viewed and printed from a web browser.

## 🚀 Usage

1. Launch the application:
   ```
   python main.py
   ```
   
   Alternatively, on Windows, you can use the included batch file:
   ```
   start.bat
   ```

2. The application will start and show the main window with:
   - Search panel (top left)
   - Appointments calendar view (bottom left)
   - Patient information form (right)

3. Basic operations:
   - ➕ Add a new patient: Click "File" > "New Patient" or use the Clear button in the patient form
   - 🔍 Search for patients: Enter a name in the search box and click "Search"
   - 📅 View appointments: Select a date in the Appointments section
   - 🖨️ Print reception slip: Select a patient and click "Print Reception Slip"
   - 💾 Data is automatically saved and backed up

## 💽 Data Storage

All patient and appointment data is stored in an Excel file located in the `data` directory. The application automatically creates daily backups to prevent data loss. This approach allows:

- Easy data import/export with other systems
- Simple manual editing if needed (though not recommended during active application use)
- Straightforward backup and restore processes

## ⚙️ Configuration

You can modify the `settings.json` file (created after first run) to customize:

- 🏢 Clinic name, logo, and contact information
- ⏱️ Default appointment duration
- 👨‍⚕️ Doctor list and specialties
- 🖨️ PDF template for reception slips
- 🌈 UI theme and colors
- And more...

## 📁 Directory Structure

- `main.py`: Main entry point
- `src/`: Source code
  - `config/`: Configuration files and settings management
  - `models/`: Data models for patients and appointments
  - `ui/`: User interface components and screens
  - `utils/`: Utility functions and helper modules
  - `resources/`: Resources like templates, images, and assets
- `data/`: Data storage and backup files
- `logs/`: Application logs for troubleshooting

## 🎨 Customization

To customize the reception slip template, edit the HTML template file in `src/resources/templates/default_template.html`. The template uses Jinja2 syntax and supports:

- Custom clinic branding
- Different layout options
- QR codes for appointment verification
- Barcode integration for patient identification

## 📜 License

This software is open source and available under the MIT License.

## Support

For any questions, issues, or feature requests:
- Create an issue in the GitHub repository
## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📸 Screenshots

![WhatsApp Image 2025-05-28 at 23 47 21_31463af6](https://github.com/user-attachments/assets/6ce3b733-9dc7-46b5-a59e-d45d2d4af3bf)

![WhatsApp Image 2025-05-28 at 23 47 20_fed1bef0](https://github.com/user-attachments/assets/e65837c1-da90-476f-8129-0444c5c419e2)

![WhatsApp Image 2025-05-28 at 04 00 32_04ef743a](https://github.com/user-attachments/assets/0da404f1-730c-4c1f-a7a7-57feeebf7136)
