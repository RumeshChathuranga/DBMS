"""
Helper Utilities
General purpose helper functions
"""
from datetime import datetime, date, timedelta
from typing import Optional, List, Dict, Any
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)


class DateTimeHelper:
    """Helper functions for date and time operations"""
    
    @staticmethod
    def calculate_nights(check_in: datetime, check_out: datetime) -> int:
        """
        Calculate number of nights between check-in and check-out
        
        Args:
            check_in: Check-in datetime
            check_out: Check-out datetime
            
        Returns:
            Number of nights
        """
        delta = check_out.date() - check_in.date()
        return max(delta.days, 1)  # Minimum 1 night
    
    @staticmethod
    def format_datetime(dt: datetime, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """
        Format datetime to string
        
        Args:
            dt: Datetime object
            format_str: Format string
            
        Returns:
            Formatted datetime string
        """
        if dt is None:
            return ""
        return dt.strftime(format_str)
    
    @staticmethod
    def format_date(d: date, format_str: str = "%Y-%m-%d") -> str:
        """
        Format date to string
        
        Args:
            d: Date object
            format_str: Format string
            
        Returns:
            Formatted date string
        """
        if d is None:
            return ""
        return d.strftime(format_str)
    
    @staticmethod
    def parse_datetime(date_str: str, format_str: str = "%Y-%m-%d %H:%M:%S") -> Optional[datetime]:
        """
        Parse string to datetime
        
        Args:
            date_str: Date string
            format_str: Format string
            
        Returns:
            Datetime object or None
        """
        try:
            return datetime.strptime(date_str, format_str)
        except ValueError:
            logger.error(f"Failed to parse datetime: {date_str}")
            return None
    
    @staticmethod
    def is_date_in_range(
        check_date: date, 
        start_date: date, 
        end_date: date
    ) -> bool:
        """
        Check if a date falls within a date range
        
        Args:
            check_date: Date to check
            start_date: Range start date
            end_date: Range end date
            
        Returns:
            True if date is in range
        """
        return start_date <= check_date <= end_date
    
    @staticmethod
    def get_current_timestamp() -> datetime:
        """Get current timestamp"""
        return datetime.now()


class MoneyHelper:
    """Helper functions for monetary calculations"""
    
    @staticmethod
    def calculate_room_charges(rate: Decimal, nights: int) -> Decimal:
        """
        Calculate total room charges
        
        Args:
            rate: Room rate per night
            nights: Number of nights
            
        Returns:
            Total room charges
        """
        return Decimal(str(rate)) * nights
    
    @staticmethod
    def calculate_service_charges(services: List[Dict[str, Any]]) -> Decimal:
        """
        Calculate total service charges
        
        Args:
            services: List of service usage dicts with 'rate' and 'quantity'
            
        Returns:
            Total service charges
        """
        total = Decimal('0.00')
        for service in services:
            rate = Decimal(str(service.get('rate', 0)))
            quantity = service.get('quantity', 1)
            total += rate * quantity
        return total
    
    @staticmethod
    def calculate_tax(amount: Decimal, tax_rate: Decimal) -> Decimal:
        """
        Calculate tax amount
        
        Args:
            amount: Base amount
            tax_rate: Tax rate (e.g., 0.15 for 15%)
            
        Returns:
            Tax amount
        """
        return Decimal(str(amount)) * Decimal(str(tax_rate))
    
    @staticmethod
    def calculate_discount(amount: Decimal, discount_rate: Decimal) -> Decimal:
        """
        Calculate discount amount
        
        Args:
            amount: Base amount
            discount_rate: Discount rate (e.g., 0.10 for 10%)
            
        Returns:
            Discount amount
        """
        return Decimal(str(amount)) * Decimal(str(discount_rate))
    
    @staticmethod
    def calculate_final_amount(
        room_charges: Decimal,
        service_charges: Decimal,
        tax_amount: Decimal,
        discount_amount: Decimal
    ) -> Decimal:
        """
        Calculate final invoice amount
        
        Args:
            room_charges: Total room charges
            service_charges: Total service charges
            tax_amount: Tax amount
            discount_amount: Discount amount
            
        Returns:
            Final amount to pay
        """
        subtotal = Decimal(str(room_charges)) + Decimal(str(service_charges))
        total = subtotal + Decimal(str(tax_amount)) - Decimal(str(discount_amount))
        return max(total, Decimal('0.00'))  # Ensure non-negative
    
    @staticmethod
    def format_currency(amount: Decimal, currency: str = "LKR") -> str:
        """
        Format amount as currency
        
        Args:
            amount: Amount to format
            currency: Currency code
            
        Returns:
            Formatted currency string
        """
        return f"{currency} {amount:,.2f}"
    
    @staticmethod
    def round_money(amount: Decimal) -> Decimal:
        """
        Round amount to 2 decimal places
        
        Args:
            amount: Amount to round
            
        Returns:
            Rounded amount
        """
        return Decimal(str(amount)).quantize(Decimal('0.01'))


class PaginationHelper:
    """Helper functions for pagination"""
    
    @staticmethod
    def calculate_offset(page: int, page_size: int) -> int:
        """
        Calculate SQL OFFSET value
        
        Args:
            page: Page number (1-based)
            page_size: Items per page
            
        Returns:
            OFFSET value
        """
        return (page - 1) * page_size
    
    @staticmethod
    def create_pagination_response(
        items: List[Any],
        total_items: int,
        page: int,
        page_size: int
    ) -> Dict[str, Any]:
        """
        Create pagination response
        
        Args:
            items: List of items for current page
            total_items: Total number of items
            page: Current page number
            page_size: Items per page
            
        Returns:
            Pagination response dict
        """
        total_pages = (total_items + page_size - 1) // page_size
        
        return {
            "items": items,
            "pagination": {
                "current_page": page,
                "page_size": page_size,
                "total_items": total_items,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_previous": page > 1
            }
        }


class ResponseHelper:
    """Helper functions for API responses"""
    
    @staticmethod
    def success_response(
        data: Any = None, 
        message: str = "Success"
    ) -> Dict[str, Any]:
        """
        Create success response
        
        Args:
            data: Response data
            message: Success message
            
        Returns:
            Success response dict
        """
        response = {
            "success": True,
            "message": message
        }
        if data is not None:
            response["data"] = data
        return response
    
    @staticmethod
    def error_response(
        message: str = "An error occurred",
        error_code: Optional[str] = None,
        details: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Create error response
        
        Args:
            message: Error message
            error_code: Error code
            details: Additional error details
            
        Returns:
            Error response dict
        """
        response = {
            "success": False,
            "message": message
        }
        if error_code:
            response["error_code"] = error_code
        if details:
            response["details"] = details
        return response


class StringHelper:
    """Helper functions for string operations"""
    
    @staticmethod
    def generate_booking_reference(booking_id: int, branch_id: int) -> str:
        """
        Generate booking reference number
        
        Args:
            booking_id: Booking ID
            branch_id: Branch ID
            
        Returns:
            Booking reference string
        """
        branch_codes = {1: "CMB", 2: "KDY", 3: "GAL"}
        branch_code = branch_codes.get(branch_id, "UNK")
        return f"SKY-{branch_code}-{booking_id:06d}"
    
    @staticmethod
    def format_full_name(first_name: str, last_name: str) -> str:
        """
        Format full name
        
        Args:
            first_name: First name
            last_name: Last name
            
        Returns:
            Full name
        """
        return f"{first_name} {last_name}".strip()
    
    @staticmethod
    def truncate_string(text: str, max_length: int, suffix: str = "...") -> str:
        """
        Truncate string to max length
        
        Args:
            text: Text to truncate
            max_length: Maximum length
            suffix: Suffix to add if truncated
            
        Returns:
            Truncated string
        """
        if len(text) <= max_length:
            return text
        return text[:max_length - len(suffix)] + suffix


# Convenience functions
def calculate_nights(check_in: datetime, check_out: datetime) -> int:
    """Calculate nights between dates"""
    return DateTimeHelper.calculate_nights(check_in, check_out)


def calculate_room_charges(rate: float, nights: int) -> Decimal:
    """Calculate room charges"""
    return MoneyHelper.calculate_room_charges(Decimal(str(rate)), nights)


def success_response(data: Any = None, message: str = "Success") -> Dict[str, Any]:
    """Create success response"""
    return ResponseHelper.success_response(data, message)


def error_response(message: str, error_code: str = None) -> Dict[str, Any]:
    """Create error response"""
    return ResponseHelper.error_response(message, error_code)


# Test function
if __name__ == "__main__":
    print("=== Testing Helper Functions ===")
    
    # Test date calculations
    check_in = datetime(2025, 1, 15, 14, 0)
    check_out = datetime(2025, 1, 18, 11, 0)
    nights = calculate_nights(check_in, check_out)
    print(f"\nNights between {check_in.date()} and {check_out.date()}: {nights}")
    
    # Test money calculations
    room_rate = Decimal('150.00')
    room_charges = calculate_room_charges(float(room_rate), nights)
    print(f"Room charges: {MoneyHelper.format_currency(room_charges)}")
    
    # Test response helpers
    print("\n--- Response Examples ---")
    print("Success:", success_response({"id": 1}, "Booking created"))
    print("Error:", error_response("Room not available", "ROOM_UNAVAILABLE"))