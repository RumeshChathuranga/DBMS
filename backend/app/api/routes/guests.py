"""
Guest Routes
Handles guest information management
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Dict, Any, List
import logging

from app.models.schemas import GuestCreate, GuestUpdate, GuestResponse, ResponseModel
from app.database.connection import DatabaseOperations
from app.database.queries import GuestQueries
from app.api.dependencies import get_current_user, require_role
from app.utils.validators import Validators

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/guests", tags=["Guests"])


@router.post("", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def create_guest(
    guest_data: GuestCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Create a new guest
    
    Available to: Admin, Manager, Reception
    """
    try:
        # Validate phone and email
        if not Validators.validate_phone(guest_data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone format. Use +94xxxxxxxxx"
            )
        
        if guest_data.email and not Validators.validate_email(guest_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Check if guest with same ID number already exists
        existing = DatabaseOperations.execute_query(
            GuestQueries.GET_GUEST_BY_ID_NUMBER,
            (guest_data.idNumber,),
            fetch_one=True
        )
        
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Guest with this ID number already exists"
            )
        
        # Create guest
        guest_id = DatabaseOperations.execute_insert(
            GuestQueries.CREATE_GUEST,
            (
                guest_data.firstName,
                guest_data.lastName,
                guest_data.phone,
                guest_data.email,
                guest_data.idNumber
            )
        )
        
        return {
            "success": True,
            "message": "Guest created successfully",
            "data": {"guestID": guest_id}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create guest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create guest"
        )


@router.get("/search", response_model=List[GuestResponse])
async def search_guests(
    query: str = Query(..., min_length=2),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Search guests by name or phone
    
    Available to: All authenticated users
    """
    try:
        search_pattern = f"%{query}%"
        offset = (page - 1) * page_size
        
        guests = DatabaseOperations.execute_query(
            GuestQueries.SEARCH_GUESTS,
            (search_pattern, search_pattern, search_pattern, page_size, offset),
            fetch_all=True
        )
        
        return guests
        
    except Exception as e:
        logger.error(f"Failed to search guests: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to search guests"
        )


@router.get("/{guest_id}", response_model=GuestResponse)
async def get_guest(
    guest_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get guest by ID
    
    Available to: All authenticated users
    """
    try:
        guest = DatabaseOperations.execute_query(
            GuestQueries.GET_GUEST_BY_ID,
            (guest_id,),
            fetch_one=True
        )
        
        if not guest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Guest not found"
            )
        
        return guest
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get guest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve guest"
        )


@router.put("/{guest_id}", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception"))])
async def update_guest(
    guest_id: int,
    guest_data: GuestUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Update guest information
    
    Available to: Admin, Manager, Reception
    """
    try:
        # Check if guest exists
        guest = DatabaseOperations.execute_query(
            GuestQueries.GET_GUEST_BY_ID,
            (guest_id,),
            fetch_one=True
        )
        
        if not guest:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Guest not found"
            )
        
        # Validate phone if provided
        if guest_data.phone and not Validators.validate_phone(guest_data.phone):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid phone format"
            )
        
        # Validate email if provided
        if guest_data.email and not Validators.validate_email(guest_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid email format"
            )
        
        # Update guest
        affected_rows = DatabaseOperations.execute_update(
            GuestQueries.UPDATE_GUEST,
            (
                guest_data.firstName or guest['firstName'],
                guest_data.lastName or guest['lastName'],
                guest_data.phone or guest['phone'],
                guest_data.email or guest['email'],
                guest_id
            )
        )
        
        return {
            "success": True,
            "message": "Guest updated successfully",
            "data": {"affected_rows": affected_rows}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update guest: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update guest"
        )