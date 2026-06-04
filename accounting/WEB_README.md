# Bill Manager - Web Version

A responsive, mobile-friendly web application for managing recurring bills. Built with Flask and pure HTML/CSS/JavaScript.

## Features

### ✅ Full Bill Management
- Add, edit, delete bills
- View all active bills
- Filter by category
- Pause bills (inactive status)

### ✅ Financial Analytics
- Real-time monthly total calculation
- Real-time yearly total calculation
- Category-based expense breakdown
- Frequency conversion (weekly → monthly → yearly)

### ✅ Mobile-Friendly
- Responsive design works on phones, tablets, laptops
- Touch-friendly buttons and inputs
- Optimized for all screen sizes

### ✅ No Installation Required
- Pure Python backend (Flask)
- No database setup needed
- SQLite database auto-created
- Reuses all backend logic from desktop version

## Installation

### Prerequisites
- Python 3.6+
- pip (Python package manager)

### Setup

1. **Navigate to the accounting folder:**
```bash
cd c:\Users\al12918\source\mine\0527\accouting
```

2. **Install Flask (one-time setup):**
```bash
pip install -r requirements.txt
```

Or manually:
```bash
pip install Flask==2.3.3
```

## Running the Web Application

### Option 1: Using the launcher script (Recommended)
```bash
python run_web.py
```

### Option 2: Direct Flask run
```bash
python app.py
```

### Access the Application

**On your computer:**
- Open browser and go to: `http://localhost:5000`

**From another device (phone, tablet, etc.) on the same network:**
1. Find your computer's IP address:
   - Windows: Open Command Prompt and type `ipconfig`, look for "IPv4 Address"
   - Example: `192.168.1.100`

2. On your mobile device, open browser and go to:
   - `http://192.168.1.100:5000`

## File Structure

```
accouting/
├── app.py                 # Flask web application
├── run_web.py            # Web app launcher
├── requirements.txt      # Python dependencies
├── database.py           # Database layer
├── models.py             # Bill model & CRUD
├── calculator.py         # Financial calculations
├── validators.py         # Input validation
├── templates/
│   └── index.html        # Web UI (HTML/CSS/JS)
├── main.py               # Desktop app launcher
├── ui.py                 # Desktop GUI (Tkinter)
├── README.md             # Desktop version docs
└── bills.db              # SQLite database (auto-created)
```

## API Endpoints

The web app provides REST API endpoints for programmatic access:

### Bills Management
- `GET /api/bills` - Get all active bills
- `GET /api/bills/all` - Get all bills (including inactive)
- `GET /api/bills/<id>` - Get specific bill
- `POST /api/bills` - Create new bill
- `PUT /api/bills/<id>` - Update bill
- `DELETE /api/bills/<id>` - Delete bill

### Statistics & Analytics
- `GET /api/statistics` - Get monthly/yearly totals
- `GET /api/summary` - Get comprehensive expense summary
- `GET /api/categories` - Get all categories
- `GET /api/bills/category/<name>` - Get bills by category

### Example API Usage

**Create a bill:**
```bash
curl -X POST http://localhost:5000/api/bills \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Electricity",
    "amount": 150.50,
    "frequency": "monthly",
    "due_date": 15,
    "category": "Utilities",
    "status": "active"
  }'
```

**Get statistics:**
```bash
curl http://localhost:5000/api/statistics
```

## User Interface

### Left Panel - Add/Edit Bill
- Form to enter bill details
- All fields validated before submission
- Clear button to reset form
- Edit mode when selecting a bill

### Right Panel - Bills List
- Displays all active bills
- Shows amount, frequency, due date, category, status
- Edit button to load bill into form
- Delete button to remove bill
- Real-time updates

### Statistics Bar
- Monthly total expenses
- Yearly total expenses
- Updates automatically when bills change

## Data Persistence

All data is stored in `bills.db` (SQLite database):
- Automatically created on first run
- Persists between sessions
- No external database needed
- Can be backed up like any file

## Troubleshooting

### Port Already in Use
If port 5000 is already in use:
```bash
python app.py --port 8000
```

### Flask Not Found
Install Flask:
```bash
pip install Flask
```

### Database Issues
Delete `bills.db` and restart the app (creates fresh database):
```bash
del bills.db
python run_web.py
```

### Can't Access from Mobile
1. Ensure both devices are on the same network
2. Check Windows Firewall - allow Python through firewall
3. Use your computer's actual IP address (not localhost)

## Shared Backend

Both desktop and web versions use the same backend modules:
- `database.py` - Database operations
- `models.py` - Bill data model
- `calculator.py` - Financial calculations
- `validators.py` - Input validation

This means:
- Data is shared between desktop and web versions
- Same validation rules
- Same calculations
- Easy to maintain

## Performance

- Lightweight Flask server
- No external dependencies (except Flask)
- SQLite database is fast for small datasets
- Responsive UI with instant feedback

## Security Notes

- Default Flask server is for development/local use
- For production deployment, use a production WSGI server (Gunicorn, uWSGI)
- Data is stored locally in SQLite
- No data sent to external servers

## Browser Compatibility

Works on:
- Chrome/Chromium
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Chrome Mobile, etc.)

## Future Enhancements

- Export to CSV/PDF
- Bill payment reminders
- Budget tracking
- Multi-user support
- Dark mode
- Advanced filtering and sorting
- Bill templates
- Payment history tracking

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review the main README.md for backend details
3. Check browser console (F12) for JavaScript errors

## License

Free to use and modify.
