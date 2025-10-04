"""
Room Routes
Handles room and room type management
"""
from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Dict, Any, List
import logging

from app.models.schemas import RoomResponse, RoomTypeResponse, ResponseModel
from app.database.connection import DatabaseOperations
from app.database.queries import RoomQueries, RoomTypeQueries
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.get("/types", response_model=List[RoomTypeResponse])
async def get_room_types(
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all room types

    Available to: All authenticated users
    """
    try:
        room_types = DatabaseOperations.execute_query(
            RoomTypeQueries.GET_ALL_ROOM_TYPES,
            fetch_all=True
        )

        return room_types

    except Exception as e:
        logger.error(f"Failed to fetch room types: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch room types"
        )


@router.get("/branch/{branch_id}", response_model=List[RoomResponse])
async def get_rooms_by_branch(
    branch_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get all rooms for a specific branch

    Available to: All authenticated users
    """
    try:
        rooms = DatabaseOperations.execute_query(
            RoomQueries.GET_ALL_ROOMS_BY_BRANCH,
            (branch_id,),
            fetch_all=True
        )

        return rooms

    except Exception as e:
        logger.error(f"Failed to fetch rooms for branch {branch_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch rooms"
        )


@router.get("/{room_id}", response_model=RoomResponse)
async def get_room(
    room_id: int,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Get room by ID

    Available to: All authenticated users
    """
    try:
        room = DatabaseOperations.execute_query(
            RoomQueries.GET_ROOM_BY_ID,
            (room_id,),
            fetch_one=True
        )

        if not room:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        return room

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get room: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve room"
        )


@router.post("/availability", response_model=List[RoomResponse])
async def check_room_availability(
    availability_request: Dict[str, Any],
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Check available rooms for given date range and room type

    Available to: All authenticated users
    """
    try:
        branchID = availability_request.get('branchID')
        typeID = availability_request.get('typeID')
        checkInDate = availability_request.get('checkInDate')
        checkOutDate = availability_request.get('checkOutDate')

        if not all([branchID, typeID, checkInDate, checkOutDate]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing required fields: branchID, typeID, checkInDate, checkOutDate"
            )

        logger.info(f"Checking availability: branch={branchID}, type={typeID}, dates={checkInDate} to {checkOutDate}")

        available_rooms = DatabaseOperations.execute_query(
            RoomQueries.CHECK_ROOM_AVAILABILITY,
            (branchID, typeID, branchID, checkOutDate, checkInDate,
             checkOutDate, checkInDate, checkInDate, checkOutDate),
            fetch_all=True
        )

        logger.info(f"Found {len(available_rooms) if available_rooms else 0} available rooms")

        return available_rooms if available_rooms else []

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to check availability: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to check room availability"
        )
