"""
database.py - Database Connection & Initialization

Handles SQLite database setup, connection management, and schema creation.
This module is responsible for:
- Creating and managing the SQLite database connection
- Creating the bills table with proper schema
- Providing a connection interface for other modules
"""

import sqlite3
from pathlib import Path


class Database:
    """Manages SQLite database connection and initialization."""
    
    def __init__(self, db_path: str = "bills.db"):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file (default: bills.db)
        """
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create the bills table if it doesn't exist."""
        conn = self.get_connection()
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
    
    def get_connection(self):
        """
        Get a new database connection.
        
        Returns:
            sqlite3.Connection object
        """
        return sqlite3.connect(self.db_path)
    
    def execute_query(self, query: str, params: tuple = ()):
        """
        Execute a query and return results.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            List of results
        """
        conn = self.get_connection()
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        results = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        return results
    
    def execute_update(self, query: str, params: tuple = ()):
        """
        Execute an insert/update/delete query.
        
        Args:
            query: SQL query string
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute(query, params)
        conn.commit()
        
        affected_rows = cursor.rowcount
        last_id = cursor.lastrowid
        
        conn.close()
        
        return affected_rows, last_id
