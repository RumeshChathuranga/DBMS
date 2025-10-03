"""
API Dependencies
Authentication and authorization middleware
"""
from fastapi import Depends, HTTPException, status, Header
from typing import Optional, Dict, Any
import logging

from app.utils.security import TokenHandler
from app.services.auth_service import AuthService

logger = logging.getLogger(__name__)


def get_token_from_header(authorization: Optional[str] = Header(None)) -> str:
    """
    Extract token from Authorization header
    
    Args:
        authorization: Authorization header value
        
    Returns:
        JWT token
        
    Raises:
        HTTPException: If token is missing or invalid format
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Expected format: "Bearer <token>"
    parts = authorization.split()
    
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format. Expected: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return parts[1]


def get_current_user(token: str = Depends(get_token_from_header)) -> Dict[str, Any]:
    """
    Get current user from JWT token
    
    Args:
        token: JWT token
        
    Returns:
        User data dict
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    user_data = TokenHandler.get_user_from_token(token)
    
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Get full user details from database
    user = AuthService.get_user_by_id(user_data['user_id'])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


def require_role(*allowed_roles: str):
    """
    Dependency factory for role-based access control
    
    Usage:
        @app.get("/admin", dependencies=[Depends(require_role("Admin"))])
        
    Args:
        allowed_roles: Roles that are allowed to access the endpoint
        
    Returns:
        Dependency function
    """
    def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """Check if user has required role"""
        user_role = current_user.get('userRole')
        
        if user_role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required role: {', '.join(allowed_roles)}"
            )
        
        return current_user
    
    return role_checker


def require_branch_access(branch_id: int, current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """
    Check if user has access to specified branch
    Admins have access to all branches
    
    Args:
        branch_id: Branch ID to check access for
        current_user: Current user data
        
    Returns:
        User data if access granted
        
    Raises:
        HTTPException: If user doesn't have access to the branch
    """
    user_role = current_user.get('userRole')
    user_branch = current_user.get('branchID')
    
    # Admins and Managers can access all branches
    if user_role in ['Admin', 'Manager']:
        return current_user
    
    # Other users can only access their assigned branch
    if user_branch != branch_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this branch"
        )
    
    return current_user


# Optional authentication - returns None if no token provided
def get_current_user_optional(authorization: Optional[str] = Header(None)) -> Optional[Dict[str, Any]]:
    """
    Get current user but don't raise error if not authenticated
    Used for endpoints that work differently for authenticated users
    
    Args:
        authorization: Authorization header
        
    Returns:
        User data or None
    """
    if not authorization:
        return None
    
    try:
        token = get_token_from_header(authorization)
        return get_current_user(token)
    except HTTPException:
        return None