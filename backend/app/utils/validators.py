"""
Validation Utilities
Common validation functions for data integrity
"""
import re
from datetime import datetime, date
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom validation error"""
    pass


class Validators:
    """Collection of validation methods"""
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """
        Validate email format
        
        Args:
            email: Email address to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not email:
            return False
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def validate_phone(phone: str) -> bool:
        """
        Validate Sri Lankan phone format (+94xxxxxxxxx)
        
        Args:
            phone: Phone number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not phone:
            return False
        
        # Sri Lankan phone format: +94xxxxxxxxx
        phone_pattern = r'^\+94[0-9]{9}$'
        return bool(re.match(phone_pattern, phone))
    
    @staticmethod
    def validate_nic(nic: str) -> bool:
        """
        Validate Sri Lankan NIC format
        Supports both old (9 digits + V/X) and new (12 digits) formats
        
        Args:
            nic: NIC number to validate
            
        Returns:
            True if valid, False otherwise
        """
        if not nic:
            return False
        
        # Old format: 9 digits + V or X
        old_pattern = r'^[0-9]{9}[VvXx]$'
        # New format: 12 digits
        new_pattern = r'^[0-9]{12}$'
        
        return bool(re.match(old_pattern, nic) or re.match(new_pattern, nic))
    
    @staticmethod
    def validate_password_strength(password: str) -> tuple[bool, str]:
        """
        Validate password strength
        Requirements:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character
        
        Args:
            password: Password to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if len(password) < 8:
            return False, "Password must be at least 8 characters long"
        
        if not re.search(r'[A-Z]', password):
            return False, "Password must contain at least one uppercase letter"
        
        if not re.search(r'[a-z]', password):
            return False, "Password must contain at least one lowercase letter"
        
        if not re.search(r'[0-9]', password):
            return False, "Password must contain at least one digit"
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            return False, "Password must contain at least one special character"
        
        return True, "Password is strong"
    
    @staticmethod
    def validate_date_range(
        check_in: datetime, 
        check_out: datetime
    ) -> tuple[bool, str]:
        """
        Validate booking date range
        
        Args:
            check_in: Check-in datetime
            check_out: Check-out datetime
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if check_in is before check_out
        if check_in >= check_out:
            return False, "Check-out date must be after check-in date"
        
        # Check if check_in is not in the past
        now = datetime.now()
        if check_in < now:
            return False, "Check-in date cannot be in the past"
        
        # Check if booking is not too far in the future (e.g., max 1 year)
        max_future = now.replace(year=now.year + 1)
        if check_in > max_future:
            return False, "Check-in date cannot be more than 1 year in advance"
        
        return True, "Date range is valid"
    
    @staticmethod
    def validate_guest_count(count: int, room_capacity: int) -> tuple[bool, str]:
        """
        Validate number of guests against room capacity
        
        Args:
            count: Number of guests
            room_capacity: Room capacity
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if count <= 0:
            return False, "Number of guests must be at least 1"
        
        if count > room_capacity:
            return False, f"Number of guests ({count}) exceeds room capacity ({room_capacity})"
        
        return True, "Guest count is valid"
    
    @staticmethod
    def validate_amount(amount: float, min_amount: float = 0) -> tuple[bool, str]:
        """
        Validate monetary amount
        
        Args:
            amount: Amount to validate
            min_amount: Minimum allowed amount
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if amount < min_amount:
            return False, f"Amount must be at least {min_amount}"
        
        # Check for reasonable decimal places (max 2)
        if round(amount, 2) != amount:
            return False, "Amount can have at most 2 decimal places"
        
        return True, "Amount is valid"
    
    @staticmethod
    def sanitize_input(input_string: str, max_length: Optional[int] = None) -> str:
        """
        Sanitize user input by removing potentially harmful characters
        
        Args:
            input_string: String to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized string
        """
        if not input_string:
            return ""
        
        # Remove leading/trailing whitespace
        sanitized = input_string.strip()
        
        # Remove any null bytes
        sanitized = sanitized.replace('\x00', '')
        
        # Truncate if necessary
        if max_length and len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized
    
    @staticmethod
    def validate_enum_value(value: str, allowed_values: list) -> tuple[bool, str]:
        """
        Validate if value is in allowed enum values
        
        Args:
            value: Value to check
            allowed_values: List of allowed values
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        if value not in allowed_values:
            return False, f"Value must be one of: {', '.join(allowed_values)}"
        
        return True, "Value is valid"


# Convenience functions
def validate_email(email: str) -> bool:
    """Validate email format"""
    return Validators.validate_email(email)


def validate_phone(phone: str) -> bool:
    """Validate phone format"""
    return Validators.validate_phone(phone)


def validate_nic(nic: str) -> bool:
    """Validate NIC format"""
    return Validators.validate_nic(nic)


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    return Validators.validate_password_strength(password)


# Test function
if __name__ == "__main__":
    print("=== Testing Validators ===")
    
    # Test email validation
    print("\n--- Email Validation ---")
    emails = ["test@example.com", "invalid.email", "user@domain.co.uk"]
    for email in emails:
        print(f"{email}: {validate_email(email)}")
    
    # Test phone validation
    print("\n--- Phone Validation ---")
    phones = ["+94771234567", "+94123456789", "0771234567"]
    for phone in phones:
        print(f"{phone}: {validate_phone(phone)}")
    
    # Test NIC validation
    print("\n--- NIC Validation ---")
    nics = ["123456789V", "123456789012", "12345678X", "invalid"]
    for nic in nics:
        print(f"{nic}: {validate_nic(nic)}")
    
    # Test password validation
    print("\n--- Password Validation ---")
    passwords = ["weak", "StrongPass123!", "NoSpecialChar123", "nouppsercase123!"]
    for pwd in passwords:
        valid, msg = validate_password(pwd)
        print(f"{pwd}: {valid} - {msg}")