"""
Service Routes
Handles service requests and usage tracking
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any, List
from datetime import datetime
import logging

from app.models.schemas import (
    ServiceResponse, ServiceUsageCreate, ServiceUsageResponse, ResponseModel
)
from app.database.connection import DatabaseOperations
from app.database.queries import ServiceQueries, ServiceUsageQueries, BookingQueries, LogQueries
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/services", tags=["Services"])


@router.get("", response_model=List[ServiceResponse])
async def get_all_services(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get all available services
    
    Available to: All authenticated users
    """
    try:
        services = DatabaseOperations.execute_query(
            ServiceQueries.GET_ALL_SERVICES,
            fetch_all=True
        )
        
        return services
        
    except Exception as e:
        logger.error(f"Failed to get services: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve services"
        )


@router.get("/{service_id}", response_model=ServiceResponse)
async def get_service(
    service_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get service by ID
    
    Available to: All authenticated users
    """
    try:
        service = DatabaseOperations.execute_query(
            ServiceQueries.GET_SERVICE_BY_ID,
            (service_id,),
            fetch_one=True
        )
        
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        
        return service
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get service: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve service"
        )


@router.post("/usage", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager", "Reception", "Staff"))])
async def create_service_usage(
    usage_data: ServiceUsageCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Record service usage for a booking
    
    Available to: Admin, Manager, Reception, Staff
    """
    try:
        # Verify booking exists
        booking = DatabaseOperations.execute_query(
            BookingQueries.GET_BOOKING_BY_ID,
            (usage_data.bookingID,),
            fetch_one=True
        )
        
        if not booking:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )
        
        if booking['bookingStatus'] not in ['CheckedIn', 'Booked']:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Can only add services to active bookings"
            )
        
        # Get service details
        service = DatabaseOperations.execute_query(
            ServiceQueries.GET_SERVICE_BY_ID,
            (usage_data.serviceID,),
            fetch_one=True
        )
        
        if not service:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service not found"
            )
        
        # Generate unique usage ID (using timestamp + booking ID)
        usage_id = int(datetime.now().timestamp() * 1000)
        
        # Create service usage record
        DatabaseOperations.execute_insert(
            ServiceUsageQueries.CREATE_SERVICE_USAGE,
            (
                usage_id,
                usage_data.bookingID,
                usage_data.serviceID,
                service['ratePerUnit'],
                usage_data.quantity,
                datetime.now()
            )
        )
        
        # Log the action
        DatabaseOperations.execute_insert(
            LogQueries.CREATE_LOG,
            (
                booking['branchID'],
                current_user['userID'],
                usage_data.bookingID,
                'Other',
                f"Service '{service['serviceType']}' added to booking"
            )
        )
        
        logger.info(f"Service usage recorded: {usage_id}")
        
        return {
            "success": True,
            "message": "Service usage recorded successfully",
            "data": {"usageID": usage_id}
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to record service usage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to record service usage"
        )


@router.get("/usage/booking/{booking_id}", response_model=List[ServiceUsageResponse])
async def get_services_by_booking(
    booking_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all services used for a specific booking
    
    Available to: All authenticated users
    """
    try:
        services = DatabaseOperations.execute_query(
            ServiceUsageQueries.GET_SERVICES_BY_BOOKING,
            (booking_id,),
            fetch_all=True
        )
        
        return services
        
    except Exception as e:
        logger.error(f"Failed to get service usage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve service usage"
        )


@router.get("/usage/{usage_id}", response_model=ServiceUsageResponse)
async def get_service_usage(
    usage_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get service usage by ID
    
    Available to: All authenticated users
    """
    try:
        usage = DatabaseOperations.execute_query(
            ServiceUsageQueries.GET_SERVICE_USAGE_BY_ID,
            (usage_id,),
            fetch_one=True
        )
        
        if not usage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Service usage not found"
            )
        
        return usage
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get service usage: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve service usage"
        )