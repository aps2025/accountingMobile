"""
validators.py - Input Validation & Error Handling

Handles validation of bill data and user inputs.
This module is responsible for:
- Validating bill names
- Validating amounts
- Validating frequencies
- Validating due dates
- Providing clear error messages
"""

from typing import Tuple, Optional


class BillValidator:
    """Validates bill data and inputs."""
    
    VALID_FREQUENCIES = ['weekly', 'bi-weekly', 'monthly', 'quarterly', 'yearly']
    VALID_STATUSES = ['active', 'inactive']
    
    @staticmethod
    def validate_name(name: str) -> Tuple[bool, Optional[str]]:
        """
        Validate bill name.
        
        Args:
            name: Bill name to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if not name or not name.strip():
            return False, "Bill name is required!"
        
        if len(name.strip()) < 2:
            return False, "Bill name must be at least 2 characters!"
        
        if len(name.strip()) > 100:
            return False, "Bill name must be less than 100 characters!"
        
        return True, None
    
    @staticmethod
    def validate_amount(amount: str) -> Tuple[bool, Optional[str]]:
        """
        Validate bill amount.
        
        Args:
            amount: Amount string to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            amount_float = float(amount)
        except ValueError:
            return False, "Amount must be a valid number!"
        
        if amount_float <= 0:
            return False, "Amount must be greater than 0!"
        
        if amount_float > 999999.99:
            return False, "Amount is too large!"
        
        return True, None
    
    @staticmethod
    def validate_frequency(frequency: str) -> Tuple[bool, Optional[str]]:
        """
        Validate bill frequency.
        
        Args:
            frequency: Frequency to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if frequency.lower() not in BillValidator.VALID_FREQUENCIES:
            valid_freqs = ', '.join(BillValidator.VALID_FREQUENCIES)
            return False, f"Frequency must be one of: {valid_freqs}"
        
        return True, None
    
    @staticmethod
    def validate_due_date(due_date: str) -> Tuple[bool, Optional[str]]:
        """
        Validate due date (day of month).
        
        Args:
            due_date: Due date to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            due_date_int = int(due_date)
        except ValueError:
            return False, "Due date must be a valid number!"
        
        if due_date_int < 1 or due_date_int > 31:
            return False, "Due date must be between 1 and 31!"
        
        return True, None
    
    @staticmethod
    def validate_status(status: str) -> Tuple[bool, Optional[str]]:
        """
        Validate bill status.
        
        Args:
            status: Status to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if status.lower() not in BillValidator.VALID_STATUSES:
            return False, f"Status must be one of: {', '.join(BillValidator.VALID_STATUSES)}"
        
        return True, None
    
    @staticmethod
    def validate_bill_data(name: str, amount: str, frequency: str, due_date: str, 
                          status: str = "active") -> Tuple[bool, Optional[str]]:
        """
        Validate all bill data at once.
        
        Args:
            name: Bill name
            amount: Bill amount
            frequency: Bill frequency
            due_date: Bill due date
            status: Bill status
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Validate name
        is_valid, error = BillValidator.validate_name(name)
        if not is_valid:
            return False, error
        
        # Validate amount
        is_valid, error = BillValidator.validate_amount(amount)
        if not is_valid:
            return False, error
        
        # Validate frequency
        is_valid, error = BillValidator.validate_frequency(frequency)
        if not is_valid:
            return False, error
        
        # Validate due date
        is_valid, error = BillValidator.validate_due_date(due_date)
        if not is_valid:
            return False, error
        
        # Validate status
        is_valid, error = BillValidator.validate_status(status)
        if not is_valid:
            return False, error
        
        return True, None
