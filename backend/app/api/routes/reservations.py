"""
Reservation Routes
Handles booking creation, updates, check-in/check-out
"""
from fastapi import APIRouter, HTTPException, Depends, Query
from fastapi import status as http_status
from typing import Dict, Any, List
import logging

from app.models.schemas import (
    BookingCreate, BookingUpdate, BookingResponse, ResponseModel
)
from app.services.booking_service import BookingService
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def create_booking(
    booking_data: BookingCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new booking
    
    Available to: Admin, Manager, Reception
    """
    try:
        booking_id = BookingService.create_booking(
            booking_data.dict(),
            current_user['userID']
        )
        
        return {
            "success": True,
            "message": "Booking created successfully",
            "data": {"bookingID": booking_id}
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create booking: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create booking"
        )


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get booking by ID
    
    Available to: All authenticated users
    """
    try:
        booking = BookingService.get_booking_by_id(booking_id)
        
        if not booking:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        return booking
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get booking: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve booking"
        )


@router.get("", response_model=List[BookingResponse])
async def get_bookings(
    branch_id: int = Query(None),
    status: str = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get bookings with filters
    
    Available to: All authenticated users
    """
    try:
        # If user is not Admin/Manager, filter by their branch
        if current_user['userRole'] not in ['Admin', 'Manager']:
            branch_id = current_user.get('branchID')
        
        bookings = BookingService.get_bookings(
            branch_id=branch_id,
            status=status,
            page=page,
            page_size=page_size
        )
        
        return bookings
        
    except Exception as e:
        logger.error(f"Failed to get bookings: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve bookings"
        )


@router.put("/{booking_id}", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def update_booking(
    booking_id: int,
    booking_data: BookingUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update booking details
    
    Available to: Admin, Manager, Reception
    """
    try:
        success = BookingService.update_booking(
            booking_id,
            booking_data.dict(exclude_unset=True),
            current_user['userID']
        )
        
        if not success:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Booking not found or update failed"
            )
        
        return {
            "success": True,
            "message": "Booking updated successfully"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update booking: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update booking"
        )


@router.post("/{booking_id}/check-in", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def check_in(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Check in a guest
    
    Available to: Admin, Manager, Reception
    """
    try:
        success = BookingService.check_in(booking_id, current_user['userID'])
        
        return {
            "success": True,
            "message": "Guest checked in successfully"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Check-in failed: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Check-in failed"
        )


@router.post("/{booking_id}/check-out", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def check_out(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Check out a guest
    
    Available to: Admin, Manager, Reception
    """
    try:
        success = BookingService.check_out(booking_id, current_user['userID'])
        
        return {
            "success": True,
            "message": "Guest checked out successfully"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Check-out failed: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Check-out failed"
        )


@router.delete("/{booking_id}", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def cancel_booking(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Cancel a booking
    
    Available to: Admin, Manager, Reception
    """
    try:
        success = BookingService.cancel_booking(booking_id, current_user['userID'])
        
        return {
            "success": True,
            "message": "Booking cancelled successfully"
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to cancel booking: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to cancel booking"
        )


@router.get("/today/check-ins", response_model=List[BookingResponse])
async def get_todays_checkins(
    branch_id: int = Query(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get bookings scheduled for check-in today
    
    Available to: All authenticated users
    """
    try:
        bookings = BookingService.get_todays_checkins(branch_id)
        return bookings
        
    except Exception as e:
        logger.error(f"Failed to get today's check-ins: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve today's check-ins"
        )


@router.get("/today/check-outs", response_model=List[BookingResponse])
async def get_todays_checkouts(
    branch_id: int = Query(...),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get bookings scheduled for check-out today
    
    Available to: All authenticated users
    """
    try:
        bookings = BookingService.get_todays_checkouts(branch_id)
        return bookings
        
    except Exception as e:
        logger.error(f"Failed to get today's check-outs: {e}")
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve today's check-outs"
        )