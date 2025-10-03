"""
Billing Routes
Handles invoice generation and payment processing
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List
from decimal import Decimal
import logging

from app.models.schemas import (
    InvoiceResponse, PaymentCreate, PaymentResponse, ResponseModel
)
from app.services.billing_service import BillingService
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/billing", tags=["Billing"])


@router.post("/invoice/generate/{booking_id}", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def generate_invoice(
    booking_id: int,
    payment_plan: str = "Full",
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Generate invoice for a booking
    
    Available to: Admin, Manager, Reception
    """
    try:
        if payment_plan not in ['Full', 'Installment']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Payment plan must be 'Full' or 'Installment'"
            )
        
        invoice_id = BillingService.generate_invoice(
            booking_id,
            current_user['userID'],
            payment_plan
        )
        
        return {
            "success": True,
            "message": "Invoice generated successfully",
            "data": {"invoiceID": invoice_id}
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to generate invoice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate invoice"
        )


@router.get("/invoice/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(
    invoice_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get invoice by ID
    
    Available to: All authenticated users
    """
    try:
        invoice = BillingService.get_invoice_by_id(invoice_id)
        
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found"
            )
        
        return invoice
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get invoice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve invoice"
        )


@router.get("/invoice/booking/{booking_id}", response_model=InvoiceResponse)
async def get_invoice_by_booking(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get invoice for a booking
    
    Available to: All authenticated users
    """
    try:
        invoice = BillingService.get_invoice_by_booking(booking_id)
        
        if not invoice:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Invoice not found for this booking"
            )
        
        return invoice
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get invoice: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve invoice"
        )


@router.post("/payment", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def process_payment(
    payment_data: PaymentCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Process a payment for an invoice
    
    Available to: Admin, Manager, Reception
    """
    try:
        transaction_id = BillingService.process_payment(
            payment_data.invoiceID,
            payment_data.paymentMethod.value,
            payment_data.amount,
            current_user['userID']
        )
        
        return {
            "success": True,
            "message": "Payment processed successfully",
            "data": {"transactionID": transaction_id}
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to process payment: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process payment"
        )


@router.get("/payment/invoice/{invoice_id}", response_model=List[PaymentResponse])
async def get_payments(
    invoice_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all payments for an invoice
    
    Available to: All authenticated users
    """
    try:
        payments = BillingService.get_payments_by_invoice(invoice_id)
        return payments
        
    except Exception as e:
        logger.error(f"Failed to get payments: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve payments"
        )


@router.get("/pending/{branch_id}", response_model=List[InvoiceResponse])
async def get_pending_invoices(
    branch_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all pending invoices for a branch
    
    Available to: All authenticated users
    """
    try:
        # If user is not Admin/Manager, ensure they can only see their branch
        if current_user['userRole'] not in ['Admin', 'Manager']:
            if current_user.get('branchID') != branch_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied to this branch"
                )
        
        invoices = BillingService.get_pending_invoices(branch_id)
        return invoices
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get pending invoices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve pending invoices"
        )