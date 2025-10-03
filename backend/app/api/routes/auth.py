"""
Authentication Routes
Handles login, registration, and token management
"""
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
import logging

from app.models.schemas import (
    UserLogin, UserCreate, TokenResponse, UserResponse, ResponseModel
)
from app.services.auth_service import AuthService
from app.api.dependencies import get_current_user, require_role

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin):
    """
    User login endpoint
    
    Returns JWT token on successful authentication
    """
    try:
        result = AuthService.login(credentials.username, credentials.password)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during login"
        )


@router.post("/register", response_model=ResponseModel, dependencies=[Depends(require_role("Admin", "Manager"))])
async def register_user(
    user_data: UserCreate,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Register a new user (Admin/Manager only)
    
    Only Admin and Manager roles can create new users
    """
    try:
        user_id = AuthService.create_user(user_data.dict())
        
        return {
            "success": True,
            "message": "User created successfully",
            "data": {"userID": user_id}
        }
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"User registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get current user information
    
    Returns the authenticated user's details
    """
    return current_user


@router.post("/verify-token")
async def verify_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Verify if the provided token is valid
    
    Used by frontend to check if user is still authenticated
    """
    return {
        "success": True,
        "message": "Token is valid",
        "data": {
            "userID": current_user['userID'],
            "username": current_user['username'],
            "role": current_user['userRole']
        }
    }