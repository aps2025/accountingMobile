"""
models.py - Bill Data Model & CRUD Operations

Handles all bill-related database operations (Create, Read, Update, Delete).
This module is responsible for:
- Bill creation and validation
- Retrieving bills with various filters
- Updating bill information
- Deleting bills
"""

from typing import List, Dict, Optional
from datetime import datetime
from database import Database


class Bill:
    """Represents a single bill with all its properties."""
    
    def __init__(self, name: str, amount: float, frequency: str, due_date: int,
                 category: str = "", notes: str = "", payment_method: str = "", 
                 status: str = "active", bill_id: int = None):
        """
        Initialize a Bill object.
        
        Args:
            name: Bill name/description
            amount: Bill amount
            frequency: Payment frequency (monthly, yearly, weekly, etc.)
            due_date: Day of month (1-31)
            category: Bill category
            notes: Additional notes
            payment_method: Payment method
            status: Bill status (active/inactive)
            bill_id: Database ID (None for new bills)
        """
        self.id = bill_id
        self.name = name
        self.amount = amount
        self.frequency = frequency
        self.due_date = due_date
        self.category = category
        self.notes = notes
        self.payment_method = payment_method
        self.status = status
    
    def to_dict(self) -> Dict:
        """Convert bill to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'amount': self.amount,
            'frequency': self.frequency,
            'due_date': self.due_date,
            'category': self.category,
            'notes': self.notes,
            'payment_method': self.payment_method,
            'status': self.status
        }


class BillRepository:
    """Handles all bill database operations."""
    
    def __init__(self, db: Database = None):
        """
        Initialize repository with database connection.
        
        Args:
            db: Database instance (creates new if None)
        """
        self.db = db or Database()
    
    def create(self, bill: Bill) -> int:
        """
        Create a new bill in the database.
        
        Args:
            bill: Bill object to create
            
        Returns:
            ID of created bill
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = '''
            INSERT INTO bills (name, amount, frequency, due_date, category, notes, 
                             start_date, payment_method, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        
        params = (bill.name, bill.amount, bill.frequency, bill.due_date, bill.category,
                 bill.notes, now, bill.payment_method, bill.status, now, now)
        
        _, bill_id = self.db.execute_update(query, params)
        return bill_id
    
    def get_by_id(self, bill_id: int) -> Optional[Dict]:
        """
        Retrieve a bill by ID.
        
        Args:
            bill_id: Bill ID
            
        Returns:
            Bill dictionary or None if not found
        """
        query = 'SELECT * FROM bills WHERE id = ?'
        results = self.db.execute_query(query, (bill_id,))
        return results[0] if results else None
    
    def get_all(self) -> List[Dict]:
        """
        Retrieve all bills sorted by due date.
        
        Returns:
            List of bill dictionaries
        """
        query = 'SELECT * FROM bills ORDER BY due_date ASC'
        return self.db.execute_query(query)
    
    def get_active(self) -> List[Dict]:
        """
        Retrieve all active bills.
        
        Returns:
            List of active bill dictionaries
        """
        query = 'SELECT * FROM bills WHERE status = "active" ORDER BY due_date ASC'
        return self.db.execute_query(query)
    
    def get_by_category(self, category: str) -> List[Dict]:
        """
        Retrieve bills by category.
        
        Args:
            category: Category name
            
        Returns:
            List of bill dictionaries
        """
        query = 'SELECT * FROM bills WHERE category = ? ORDER BY due_date ASC'
        return self.db.execute_query(query, (category,))
    
    def get_categories(self) -> List[str]:
        """
        Get all unique categories.
        
        Returns:
            List of category names
        """
        query = 'SELECT DISTINCT category FROM bills WHERE category IS NOT NULL AND category != "" ORDER BY category'
        results = self.db.execute_query(query)
        return [row['category'] for row in results]
    
    def update(self, bill_id: int, bill: Bill) -> bool:
        """
        Update an existing bill.
        
        Args:
            bill_id: Bill ID to update
            bill: Bill object with updated data
            
        Returns:
            True if successful, False otherwise
        """
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        query = '''
            UPDATE bills 
            SET name = ?, amount = ?, frequency = ?, due_date = ?, category = ?,
                notes = ?, status = ?, payment_method = ?, updated_at = ?
            WHERE id = ?
        '''
        
        params = (bill.name, bill.amount, bill.frequency, bill.due_date, bill.category,
                 bill.notes, bill.status, bill.payment_method, now, bill_id)
        
        affected_rows, _ = self.db.execute_update(query, params)
        return affected_rows > 0
    
    def delete(self, bill_id: int) -> bool:
        """
        Delete a bill.
        
        Args:
            bill_id: Bill ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        query = 'DELETE FROM bills WHERE id = ?'
        affected_rows, _ = self.db.execute_update(query, (bill_id,))
        return affected_rows > 0
