# Clinic Receptionist Software

A desktop application for managing patient appointments and printing reception slips in a doctor's clinic.

## Features

- Patient registration and management
- Appointment scheduling
- Search patients by name
- View appointments by date
- Print reception slips
- Automatic data backup
- Excel-based data storage

## Requirements

- Python 3.7+
- Tkinter (included with most Python installations)
- pandas
- openpyxl
- tkcalendar
- pdfkit
- Jinja2
- wkhtmltopdf (optional, for PDF generation)

## Installation

1. Clone this repository or download the source code

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

## Usage

1. Run the application:
   ```
   python main.py
   ```
   
   Alternatively, on Windows, you can use the batch file:
   ```
   start.bat
   ```

2. The application will start and show the main window with:
   - Search panel (top left)
   - Appointments view (bottom left)
   - Patient form (right)

3. Basic operations:
   - Add a new patient: Click "File" > "New Patient" or use the Clear button in the patient form
   - Search for patients: Enter a name in the search box and click "Search"
   - View appointments: Select a date in the Appointments section
   - Print reception slip: Select a patient and click "Print Reception Slip"

## Data Storage

All data is stored in an Excel file located in the `data` directory. The application automatically creates backups when changes are made.

## Configuration

You can modify the `settings.json` file (created after first run) to customize:

- Company name and logo
- Default appointment duration
- Doctor list
- PDF template for reception slips
- And more...

## Directory Structure

- `main.py`: Main entry point
- `src/`: Source code
  - `config/`: Configuration files
  - `models/`: Data models
  - `ui/`: User interface components
  - `utils/`: Utility functions
  - `resources/`: Resources like templates and images
- `data/`: Data storage
- `logs/`: Log files

## Customization

To customize the reception slip template, edit the HTML template file in `src/resources/templates/default_template.html`.

## License

This software is open source and available under the MIT License.

## Contact

For any questions or issues, please create an issue in the repository or contact the developer.