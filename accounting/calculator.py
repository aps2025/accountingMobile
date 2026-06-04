"""
calculator.py - Bill Calculations & Analytics

Handles all financial calculations and analytics for bills.
This module is responsible for:
- Calculating monthly expenses
- Calculating yearly expenses
- Converting between different frequencies
- Providing expense summaries
"""

from typing import List, Dict
from models import BillRepository


class BillCalculator:
    """Performs financial calculations on bills."""
    
    # Conversion factors for different frequencies to monthly
    FREQUENCY_TO_MONTHLY = {
        'weekly': 4.33,           # Average weeks per month
        'bi-weekly': 2.17,        # Average bi-weeks per month
        'monthly': 1.0,
        'quarterly': 1/3,         # 4 quarters per year / 12 months
        'yearly': 1/12
    }
    
    # Conversion factors for different frequencies to yearly
    FREQUENCY_TO_YEARLY = {
        'weekly': 52,
        'bi-weekly': 26,
        'monthly': 12,
        'quarterly': 4,
        'yearly': 1
    }
    
    def __init__(self, repository: BillRepository = None):
        """
        Initialize calculator with bill repository.
        
        Args:
            repository: BillRepository instance (creates new if None)
        """
        self.repository = repository or BillRepository()
    
    def calculate_monthly_total(self) -> float:
        """
        Calculate total monthly expenses from active bills.
        
        Returns:
            Total monthly expenses rounded to 2 decimal places
        """
        bills = self.repository.get_active()
        total = 0.0
        
        for bill in bills:
            amount = bill['amount']
            frequency = bill['frequency'].lower()
            
            multiplier = self.FREQUENCY_TO_MONTHLY.get(frequency, 1.0)
            total += amount * multiplier
        
        return round(total, 2)
    
    def calculate_yearly_total(self) -> float:
        """
        Calculate total yearly expenses from active bills.
        
        Returns:
            Total yearly expenses rounded to 2 decimal places
        """
        bills = self.repository.get_active()
        total = 0.0
        
        for bill in bills:
            amount = bill['amount']
            frequency = bill['frequency'].lower()
            
            multiplier = self.FREQUENCY_TO_YEARLY.get(frequency, 1.0)
            total += amount * multiplier
        
        return round(total, 2)
    
    def calculate_category_monthly(self, category: str) -> float:
        """
        Calculate monthly expenses for a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Total monthly expenses for category
        """
        bills = self.repository.get_by_category(category)
        total = 0.0
        
        for bill in bills:
            if bill['status'] == 'active':
                amount = bill['amount']
                frequency = bill['frequency'].lower()
                multiplier = self.FREQUENCY_TO_MONTHLY.get(frequency, 1.0)
                total += amount * multiplier
        
        return round(total, 2)
    
    def calculate_category_yearly(self, category: str) -> float:
        """
        Calculate yearly expenses for a specific category.
        
        Args:
            category: Category name
            
        Returns:
            Total yearly expenses for category
        """
        bills = self.repository.get_by_category(category)
        total = 0.0
        
        for bill in bills:
            if bill['status'] == 'active':
                amount = bill['amount']
                frequency = bill['frequency'].lower()
                multiplier = self.FREQUENCY_TO_YEARLY.get(frequency, 1.0)
                total += amount * multiplier
        
        return round(total, 2)
    
    def get_expense_summary(self) -> Dict:
        """
        Get a comprehensive expense summary.
        
        Returns:
            Dictionary with monthly total, yearly total, and category breakdown
        """
        categories = self.repository.get_categories()
        
        return {
            'monthly_total': self.calculate_monthly_total(),
            'yearly_total': self.calculate_yearly_total(),
            'categories': {
                cat: {
                    'monthly': self.calculate_category_monthly(cat),
                    'yearly': self.calculate_category_yearly(cat)
                }
                for cat in categories
            }
        }
    
    def convert_frequency(self, amount: float, from_frequency: str, to_frequency: str) -> float:
        """
        Convert an amount from one frequency to another.
        
        Args:
            amount: Amount to convert
            from_frequency: Source frequency
            to_frequency: Target frequency
            
        Returns:
            Converted amount
        """
        # Convert to yearly first
        yearly_multiplier = self.FREQUENCY_TO_YEARLY.get(from_frequency.lower(), 1.0)
        yearly_amount = amount * yearly_multiplier
        
        # Convert from yearly to target frequency
        to_multiplier = self.FREQUENCY_TO_YEARLY.get(to_frequency.lower(), 1.0)
        converted_amount = yearly_amount / to_multiplier
        
        return round(converted_amount, 2)
