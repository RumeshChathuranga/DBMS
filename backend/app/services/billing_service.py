"""
Billing Service
Handles invoice generation and payment processing
"""
from typing import Optional, Dict, Any, List
from datetime import date, datetime
from decimal import Decimal
import logging

from app.database.connection import DatabaseOperations, Database
from app.database.queries import (
    InvoiceQueries, PaymentQueries, ServiceUsageQueries,
    BookingQueries, TaxPolicyQueries, LogQueries
)
from app.utils.helpers import DateTimeHelper, MoneyHelper
from app.utils.validators import Validators

logger = logging.getLogger(__name__)


class BillingService:
    """Billing and payment service"""
    
    @staticmethod
    def calculate_invoice_amounts(
        booking_id: int
    ) -> Dict[str, Decimal]:
        """
        Calculate all invoice amounts for a booking
        
        Args:
            booking_id: Booking ID
            
        Returns:
            Dict with all calculated amounts
        """
        try:
            # Get booking details
            booking = DatabaseOperations.execute_query(
                BookingQueries.GET_BOOKING_BY_ID,
                (booking_id,),
                fetch_one=True
            )
            
            if not booking:
                raise ValueError("Booking not found")
            
            # Calculate room charges
            nights = DateTimeHelper.calculate_nights(
                booking['checkInDate'],
                booking['checkOutDate']
            )
            room_charges = MoneyHelper.calculate_room_charges(
                Decimal(str(booking['rate'])),
                nights
            )
            
            # Calculate service charges
            services = DatabaseOperations.execute_query(
                ServiceUsageQueries.GET_SERVICES_BY_BOOKING,
                (booking_id,),
                fetch_all=True
            )
            
            service_charges = Decimal('0.00')
            for service in services:
                service_charges += Decimal(str(service['rate'])) * service['quantity']
            
            # Get tax policy (assuming there's a general tax policy)
            tax_policy = DatabaseOperations.execute_query(
                TaxPolicyQueries.GET_TAX_POLICY_BY_TYPE,
                ('Room',),
                fetch_one=True
            )
            
            tax_rate = Decimal(str(tax_policy['rate'])) if tax_policy else Decimal('0.00')
            
            # Calculate tax
            subtotal = room_charges + service_charges
            tax_amount = MoneyHelper.calculate_tax(subtotal, tax_rate)
            
            # For now, no discount
            discount_amount = Decimal('0.00')
            
            # Calculate final amount
            final_amount = MoneyHelper.calculate_final_amount(
                room_charges,
                service_charges,
                tax_amount,
                discount_amount
            )
            
            return {
                'roomCharges': room_charges,
                'serviceCharges': service_charges,
                'taxAmount': tax_amount,
                'discountAmount': discount_amount,
                'totalAmount': final_amount,
                'nights': nights,
                'policyID': tax_policy['policyID'] if tax_policy else None
            }
            
        except Exception as e:
            logger.error(f"Failed to calculate invoice amounts: {e}")
            raise
    
    @staticmethod
    def generate_invoice(
        booking_id: int,
        user_id: int,
        payment_plan: str = 'Full'
    ) -> Optional[int]:
        """
        Generate invoice for a booking
        
        Args:
            booking_id: Booking ID
            user_id: User generating the invoice
            payment_plan: Payment plan (Full/Installment)
            
        Returns:
            Invoice ID or None
        """
        try:
            # Check if invoice already exists
            existing_invoice = DatabaseOperations.execute_query(
                InvoiceQueries.GET_INVOICE_BY_BOOKING,
                (booking_id,),
                fetch_one=True
            )
            
            if existing_invoice:
                logger.info(f"Invoice already exists for booking {booking_id}")
                return existing_invoice['invoiceID']
            
            # Calculate amounts
            amounts = BillingService.calculate_invoice_amounts(booking_id)
            
            # Create invoice
            invoice_id = DatabaseOperations.execute_insert(
                InvoiceQueries.CREATE_INVOICE,
                (
                    booking_id,
                    amounts.get('policyID'),
                    None,  # discountCode
                    payment_plan,
                    amounts['roomCharges'],
                    amounts['serviceCharges'],
                    amounts['taxAmount'],
                    amounts['discountAmount'],
                    Decimal('0.00'),  # settledAmount
                    'Pending'
                )
            )
            
            # Get booking for logging
            booking = DatabaseOperations.execute_query(
                BookingQueries.GET_BOOKING_BY_ID,
                (booking_id,),
                fetch_one=True
            )
            
            # Log the action
            DatabaseOperations.execute_insert(
                LogQueries.CREATE_LOG,
                (
                    booking['branchID'],
                    user_id,
                    booking_id,
                    'Other',
                    f"Invoice generated (ID: {invoice_id})"
                )
            )
            
            logger.info(f"Invoice generated successfully: ID {invoice_id}")
            return invoice_id
            
        except Exception as e:
            logger.error(f"Failed to generate invoice: {e}")
            raise
    
    @staticmethod
    def get_invoice_by_id(invoice_id: int) -> Optional[Dict[str, Any]]:
        """
        Get invoice by ID
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            Invoice details or None
        """
        try:
            return DatabaseOperations.execute_query(
                InvoiceQueries.GET_INVOICE_BY_ID,
                (invoice_id,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Failed to get invoice: {e}")
            return None
    
    @staticmethod
    def get_invoice_by_booking(booking_id: int) -> Optional[Dict[str, Any]]:
        """
        Get invoice by booking ID
        
        Args:
            booking_id: Booking ID
            
        Returns:
            Invoice details or None
        """
        try:
            return DatabaseOperations.execute_query(
                InvoiceQueries.GET_INVOICE_BY_BOOKING,
                (booking_id,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Failed to get invoice: {e}")
            return None
    
    @staticmethod
    def process_payment(
        invoice_id: int,
        payment_method: str,
        amount: Decimal,
        user_id: int
    ) -> Optional[int]:
        """
        Process a payment for an invoice
        
        Args:
            invoice_id: Invoice ID
            payment_method: Payment method
            amount: Payment amount
            user_id: User processing payment
            
        Returns:
            Transaction ID or None
        """
        try:
            # Validate amount
            is_valid, error_msg = Validators.validate_amount(float(amount))
            if not is_valid:
                raise ValueError(error_msg)
            
            # Get invoice
            invoice = BillingService.get_invoice_by_id(invoice_id)
            if not invoice:
                raise ValueError("Invoice not found")
            
            if invoice['invoiceStatus'] == 'Paid':
                raise ValueError("Invoice is already fully paid")
            
            if invoice['invoiceStatus'] == 'Cancelled':
                raise ValueError("Cannot process payment for cancelled invoice")
            
            # Calculate balance due
            balance_due = invoice['totalAmount'] - invoice['settledAmount']
            
            if amount > balance_due:
                raise ValueError(f"Payment amount exceeds balance due ({balance_due})")
            
            with Database.get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Create payment record
                cursor.execute(
                    PaymentQueries.CREATE_PAYMENT,
                    (invoice_id, date.today(), payment_method, amount)
                )
                transaction_id = cursor.lastrowid
                
                # Update invoice settled amount
                new_settled = invoice['settledAmount'] + amount
                
                # Determine new status
                if new_settled >= invoice['totalAmount']:
                    new_status = 'Paid'
                elif new_settled > 0:
                    new_status = 'Partially Paid'
                else:
                    new_status = 'Pending'
                
                cursor.execute(
                    InvoiceQueries.UPDATE_INVOICE_SETTLED_AMOUNT,
                    (new_settled, new_status, invoice_id)
                )
                
                # Log the payment
                cursor.execute(
                    LogQueries.CREATE_LOG,
                    (
                        None,  # branchID - get from booking if needed
                        user_id,
                        invoice['bookingID'],
                        'Payment',
                        f"Payment of {amount} via {payment_method}"
                    )
                )
                
                conn.commit()
                cursor.close()
                
                logger.info(f"Payment processed: {amount} for invoice {invoice_id}")
                return transaction_id
                
        except Exception as e:
            logger.error(f"Failed to process payment: {e}")
            raise
    
    @staticmethod
    def get_payments_by_invoice(invoice_id: int) -> List[Dict[str, Any]]:
        """
        Get all payments for an invoice
        
        Args:
            invoice_id: Invoice ID
            
        Returns:
            List of payments
        """
        try:
            return DatabaseOperations.execute_query(
                PaymentQueries.GET_PAYMENTS_BY_INVOICE,
                (invoice_id,),
                fetch_all=True
            )
        except Exception as e:
            logger.error(f"Failed to get payments: {e}")
            raise
    
    @staticmethod
    def get_pending_invoices(branch_id: int) -> List[Dict[str, Any]]:
        """
        Get all pending invoices for a branch
        
        Args:
            branch_id: Branch ID
            
        Returns:
            List of pending invoices
        """
        try:
            return DatabaseOperations.execute_query(
                InvoiceQueries.GET_PENDING_INVOICES,
                (branch_id,),
                fetch_all=True
            )
        except Exception as e:
            logger.error(f"Failed to get pending invoices: {e}")
            raise