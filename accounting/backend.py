import sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class BillManager:
    """Backend for managing recurring bills with SQLite storage."""
    
    def __init__(self, db_path: str = "bills.db"):
        """Initialize the database connection and create tables if needed."""
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the bills table if it doesn't exist."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bills (
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
        ''')
        
        conn.commit()
        conn.close()
    
    def add_bill(self, name: str, amount: float, frequency: str, due_date: int,
                 category: str = "", notes: str = "", payment_method: str = "") -> int:
        """
        Add a new bill to the database.
        
        Args:
            name: Bill name/description
            amount: Bill amount
            frequency: Frequency (monthly, yearly, weekly, quarterly, bi-weekly)
            due_date: Day of month (1-31)
            category: Bill category
            notes: Additional notes
            payment_method: Payment method
            
        Returns:
            Bill ID
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO bills (name, amount, frequency, due_date, category, notes, 
                             start_date, payment_method, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, amount, frequency, due_date, category, notes, now, payment_method, now, now))
        
        conn.commit()
        bill_id = cursor.lastrowid
        conn.close()
        
        return bill_id
    
    def get_all_bills(self) -> List[Dict]:
        """Retrieve all bills from the database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills ORDER BY due_date ASC')
        bills = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return bills
    
    def get_bill_by_id(self, bill_id: int) -> Optional[Dict]:
        """Retrieve a specific bill by ID."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills WHERE id = ?', (bill_id,))
        row = cursor.fetchone()
        
        conn.close()
        return dict(row) if row else None
    
    def update_bill(self, bill_id: int, name: str = None, amount: float = None,
                   frequency: str = None, due_date: int = None, category: str = None,
                   notes: str = None, status: str = None, payment_method: str = None) -> bool:
        """Update an existing bill."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Get current bill data
        current = self.get_bill_by_id(bill_id)
        if not current:
            conn.close()
            return False
        
        # Use provided values or keep existing ones
        name = name if name is not None else current['name']
        amount = amount if amount is not None else current['amount']
        frequency = frequency if frequency is not None else current['frequency']
        due_date = due_date if due_date is not None else current['due_date']
        category = category if category is not None else current['category']
        notes = notes if notes is not None else current['notes']
        status = status if status is not None else current['status']
        payment_method = payment_method if payment_method is not None else current['payment_method']
        
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            UPDATE bills 
            SET name = ?, amount = ?, frequency = ?, due_date = ?, category = ?,
                notes = ?, status = ?, payment_method = ?, updated_at = ?
            WHERE id = ?
        ''', (name, amount, frequency, due_date, category, notes, status, payment_method, now, bill_id))
        
        conn.commit()
        conn.close()
        
        return True
    
    def delete_bill(self, bill_id: int) -> bool:
        """Delete a bill from the database."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM bills WHERE id = ?', (bill_id,))
        conn.commit()
        success = cursor.rowcount > 0
        conn.close()
        
        return success
    
    def get_bills_by_category(self, category: str) -> List[Dict]:
        """Get all bills in a specific category."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills WHERE category = ? ORDER BY due_date ASC', (category,))
        bills = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return bills
    
    def get_active_bills(self) -> List[Dict]:
        """Get all active bills."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills WHERE status = "active" ORDER BY due_date ASC')
        bills = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return bills
    
    def calculate_monthly_total(self) -> float:
        """Calculate total monthly expenses from active bills."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills WHERE status = "active"')
        bills = cursor.fetchall()
        conn.close()
        
        total = 0
        for bill in bills:
            amount = bill[2]  # amount column
            frequency = bill[3]  # frequency column
            
            if frequency.lower() == 'monthly':
                total += amount
            elif frequency.lower() == 'weekly':
                total += amount * 4.33  # Average weeks per month
            elif frequency.lower() == 'bi-weekly':
                total += amount * 2.17  # Average bi-weeks per month
            elif frequency.lower() == 'yearly':
                total += amount / 12
            elif frequency.lower() == 'quarterly':
                total += amount / 3
        
        return round(total, 2)
    
    def calculate_yearly_total(self) -> float:
        """Calculate total yearly expenses from active bills."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM bills WHERE status = "active"')
        bills = cursor.fetchall()
        conn.close()
        
        total = 0
        for bill in bills:
            amount = bill[2]  # amount column
            frequency = bill[3]  # frequency column
            
            if frequency.lower() == 'monthly':
                total += amount * 12
            elif frequency.lower() == 'weekly':
                total += amount * 52
            elif frequency.lower() == 'bi-weekly':
                total += amount * 26
            elif frequency.lower() == 'yearly':
                total += amount
            elif frequency.lower() == 'quarterly':
                total += amount * 4
        
        return round(total, 2)
    
    def get_categories(self) -> List[str]:
        """Get all unique categories."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT category FROM bills WHERE category IS NOT NULL AND category != "" ORDER BY category')
        categories = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return categories
