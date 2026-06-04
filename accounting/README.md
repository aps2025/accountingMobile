# Bill Manager Application

A lightweight, modular Python application for managing recurring bills with a Tkinter GUI and SQLite backend.

## Project Structure

The application is organized into separate, focused modules for better maintainability and testability:

### Backend Modules

#### **database.py** - Database Connection & Initialization
- Manages SQLite database connection and setup
- Creates the bills table with proper schema
- Provides methods for executing queries and updates
- **Key Classes:**
  - `Database`: Handles all database operations

#### **models.py** - Bill Data Model & CRUD Operations
- Defines the Bill data model
- Implements all Create, Read, Update, Delete operations
- Manages bill validation and persistence
- **Key Classes:**
  - `Bill`: Represents a single bill with all properties
  - `BillRepository`: Handles all database operations for bills

#### **calculator.py** - Bill Calculations & Analytics
- Performs financial calculations on bills
- Converts between different payment frequencies
- Calculates monthly and yearly expenses
- Provides expense summaries by category
- **Key Classes:**
  - `BillCalculator`: Performs all financial calculations

#### **validators.py** - Input Validation & Error Handling
- Validates all user inputs
- Provides clear error messages
- Ensures data integrity before storage
- **Key Classes:**
  - `BillValidator`: Validates bill data and user inputs

### Frontend Module

#### **ui.py** - Tkinter GUI
- Clean, user-friendly interface
- Two-panel layout (form + list)
- Real-time statistics display
- **Key Classes:**
  - `BillManagerUI`: Main GUI application

### Entry Point

#### **main.py**
- Application launcher
- Initializes and runs the GUI

## Features

### Bill Management
- ✅ **Add Bills** - Create new recurring bills with all details
- ✅ **Edit Bills** - Double-click any bill to modify it
- ✅ **Delete Bills** - Remove bills with confirmation
- ✅ **View Bills** - Display all active bills in a sortable list

### Financial Calculations
- ✅ **Monthly Total** - Calculate total monthly expenses
- ✅ **Yearly Total** - Calculate total yearly expenses
- ✅ **Category Breakdown** - View expenses by category
- ✅ **Frequency Conversion** - Convert amounts between different frequencies

### Bill Properties
Each bill stores the following information:
- **Name** - Bill description (e.g., "Electricity", "Internet")
- **Amount** - Bill amount in dollars
- **Frequency** - Payment frequency (weekly, bi-weekly, monthly, quarterly, yearly)
- **Due Date** - Day of month (1-31)
- **Category** - Bill category (utilities, subscriptions, insurance, etc.)
- **Status** - Active or inactive (pause bills without deleting)
- **Payment Method** - How the bill is paid (optional)
- **Notes** - Additional information (optional)

### Data Persistence
- SQLite database stores all bills
- Data automatically persists between sessions
- Database file: `bills.db` (created automatically)

## Installation & Usage

### Prerequisites
- Python 3.6+
- Tkinter (usually included with Python)
- No external dependencies required!

### Running the Application

```bash
cd c:\Users\al12918\source\mine\0527\accouting
python main.py
```

The application will:
1. Create a `bills.db` SQLite database (if it doesn't exist)
2. Open the GUI window
3. Load all existing bills

## Module Dependencies

```
main.py
  └── ui.py
       ├── models.py
       │    └── database.py
       ├── calculator.py
       │    └── models.py
       │         └── database.py
       └── validators.py
```

## Architecture Benefits

### Separation of Concerns
- **Database Layer** (`database.py`): Handles all database operations
- **Data Model** (`models.py`): Defines bill structure and CRUD operations
- **Business Logic** (`calculator.py`): Performs calculations and analytics
- **Validation** (`validators.py`): Ensures data integrity
- **Presentation** (`ui.py`): User interface

### Maintainability
- Each module has a single responsibility
- Easy to test individual components
- Easy to extend with new features
- Clear documentation for each module

### Reusability
- Backend modules can be used independently
- Easy to create alternative UIs (web, CLI, etc.)
- Calculator can be used for reporting/exports

## Frequency Conversion Factors

The calculator uses these conversion factors:

| Frequency | To Monthly | To Yearly |
|-----------|-----------|-----------|
| Weekly | 4.33 | 52 |
| Bi-weekly | 2.17 | 26 |
| Monthly | 1.0 | 12 |
| Quarterly | 0.33 | 4 |
| Yearly | 0.083 | 1 |

## Example Usage

### Adding a Bill
1. Fill in the form fields:
   - Name: "Electricity"
   - Amount: "150.50"
   - Frequency: "monthly"
   - Due Date: "15"
   - Category: "Utilities"
2. Click "Add Bill"
3. Bill appears in the list

### Editing a Bill
1. Double-click a bill in the list
2. Form fields populate with bill data
3. Modify the fields
4. Click "Update Bill"

### Deleting a Bill
1. Select a bill in the list
2. Click "Delete Selected"
3. Confirm the deletion

## Database Schema

```sql
CREATE TABLE bills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    amount REAL NOT NULL,
    frequency TEXT NOT NULL,
    due_date INTEGER NOT NULL,
    category TEXT,
    notes TEXT,
    start_date TEXT NOT NULL,
    status TEXT DEFAULT 'active',
    payment_method TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
)
```

## Future Enhancement Ideas

- Export bills to CSV/PDF
- Bill payment reminders
- Recurring bill templates
- Budget tracking and alerts
- Multi-user support
- Web-based UI
- Mobile app
- Integration with banking APIs

## License

This project is free to use and modify.
