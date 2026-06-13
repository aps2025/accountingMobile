"""
data_manager.py - Data Export & Import Module

Handles exporting bills to CSV/JSON and importing bills from files.
This module provides data backup and restore capabilities for the bill manager.
"""

import csv
import json
from typing import List, Dict
from datetime import datetime
from pathlib import Path


class DataExporter:
    """Export bills to various file formats."""
    
    @staticmethod
    def export_to_csv(bills: List[Dict], filename: str = None) -> str:
        """
        Export bills to CSV format.
        
        Args:
            bills: List of bill dictionaries
            filename: Output filename (default: bills_YYYYMMDD_HHMMSS.csv)
            
        Returns:
            Path to created CSV file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bills_export_{timestamp}.csv"
        
        if not bills:
            raise ValueError("No bills to export")
        
        # Get all field names from the first bill
        fieldnames = bills[0].keys()
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(bills)
        
        return filename
    
    @staticmethod
    def export_to_json(bills: List[Dict], filename: str = None) -> str:
        """
        Export bills to JSON format.
        
        Args:
            bills: List of bill dictionaries
            filename: Output filename (default: bills_YYYYMMDD_HHMMSS.json)
            
        Returns:
            Path to created JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"bills_export_{timestamp}.json"
        
        if not bills:
            raise ValueError("No bills to export")
        
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(bills, jsonfile, indent=2, ensure_ascii=False)
        
        return filename


class DataImporter:
    """Import bills from various file formats."""
    
    @staticmethod
    def import_from_csv(filename: str) -> List[Dict]:
        """
        Import bills from CSV file.
        
        Args:
            filename: Path to CSV file
            
        Returns:
            List of bill dictionaries
        """
        bills = []
        
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                for row in reader:
                    # Convert numeric fields
                    if 'id' in row and row['id']:
                        row['id'] = int(row['id'])
                    if 'amount' in row:
                        row['amount'] = float(row['amount'])
                    if 'due_date' in row:
                        row['due_date'] = int(row['due_date'])
                    
                    bills.append(row)
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")
        except Exception as e:
            raise ValueError(f"Error reading CSV file: {str(e)}")
        
        return bills
    
    @staticmethod
    def import_from_json(filename: str) -> List[Dict]:
        """
        Import bills from JSON file.
        
        Args:
            filename: Path to JSON file
            
        Returns:
            List of bill dictionaries
        """
        try:
            with open(filename, 'r', encoding='utf-8') as jsonfile:
                bills = json.load(jsonfile)
            
            if not isinstance(bills, list):
                raise ValueError("JSON must contain a list of bills")
            
            # Convert numeric fields
            for bill in bills:
                if 'id' in bill and bill['id']:
                    bill['id'] = int(bill['id'])
                if 'amount' in bill:
                    bill['amount'] = float(bill['amount'])
                if 'due_date' in bill:
                    bill['due_date'] = int(bill['due_date'])
            
            return bills
        
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filename}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON file: {str(e)}")
        except Exception as e:
            raise ValueError(f"Error reading JSON file: {str(e)}")
    
    @staticmethod
    def import_from_file(filename: str) -> List[Dict]:
        """
        Auto-detect file format and import bills.
        
        Args:
            filename: Path to import file (.csv or .json)
            
        Returns:
            List of bill dictionaries
        """
        file_path = Path(filename)
        
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {filename}")
        
        suffix = file_path.suffix.lower()
        
        if suffix == '.csv':
            return DataImporter.import_from_csv(filename)
        elif suffix == '.json':
            return DataImporter.import_from_json(filename)
        else:
            raise ValueError(f"Unsupported file format: {suffix}. Use .csv or .json")
