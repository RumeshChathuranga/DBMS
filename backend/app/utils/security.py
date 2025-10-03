"""
Security Utilities
Handles password hashing and JWT token operations
"""
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt
from jose import JWTError, jwt
import logging

from app.config import settings

logger = logging.getLogger(__name__)


class PasswordHandler:
    """Handle password hashing and verification"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash a password using bcrypt
        
        Args:
            password: Plain text password
            
        Returns:
            Hashed password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash
        
        Args:
            plain_password: Plain text password to verify
            hashed_password: Hashed password to compare against
            
        Returns:
            True if password matches, False otherwise
        """
        try:
            return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logger.error(f"Password verification error: {e}")
            return False


class TokenHandler:
    """Handle JWT token creation and validation"""
    
    @staticmethod
    def create_access_token(
        data: Dict[str, Any], 
        expires_delta: Optional[timedelta] = None
    ) -> str:
        """
        Create a JWT access token
        
        Args:
            data: Data to encode in the token (user info)
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT token
        """
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=settings.JWT_EXPIRATION_MINUTES
            )
        
        to_encode.update({
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access"
        })
        
        encoded_jwt = jwt.encode(
            to_encode, 
            settings.JWT_SECRET_KEY, 
            algorithm=settings.JWT_ALGORITHM
        )
        
        return encoded_jwt
    
    @staticmethod
    def decode_access_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Decode and validate a JWT token
        
        Args:
            token: JWT token string
            
        Returns:
            Decoded token data or None if invalid
        """
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET_KEY, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload
        except JWTError as e:
            logger.error(f"JWT decode error: {e}")
            return None
    
    @staticmethod
    def create_token_for_user(
        user_id: int,
        username: str,
        role: str,
        branch_id: Optional[int] = None
    ) -> str:
        """
        Create a token with user information
        
        Args:
            user_id: User's ID
            username: User's username
            role: User's role
            branch_id: User's branch ID (if applicable)
            
        Returns:
            JWT token
        """
        token_data = {
            "sub": str(user_id),
            "username": username,
            "role": role,
            "branch_id": branch_id
        }
        
        return TokenHandler.create_access_token(token_data)
    
    @staticmethod
    def get_user_from_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Extract user information from token
        
        Args:
            token: JWT token
            
        Returns:
            User data dict or None
        """
        payload = TokenHandler.decode_access_token(token)
        
        if payload is None:
            return None
        
        return {
            "user_id": int(payload.get("sub")),
            "username": payload.get("username"),
            "role": payload.get("role"),
            "branch_id": payload.get("branch_id")
        }


# Convenience functions
def hash_password(password: str) -> str:
    """Hash a password"""
    return PasswordHandler.hash_password(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password"""
    return PasswordHandler.verify_password(plain_password, hashed_password)


def create_access_token(data: Dict[str, Any]) -> str:
    """Create an access token"""
    return TokenHandler.create_access_token(data)


def decode_token(token: str) -> Optional[Dict[str, Any]]:
    """Decode a token"""
    return TokenHandler.decode_access_token(token)


# Test function
if __name__ == "__main__":
    print("=== Testing Security Utils ===")
    
    # Test password hashing
    password = "SecurePassword123!"
    hashed = hash_password(password)
    print(f"Original password: {password}")
    print(f"Hashed password: {hashed}")
    print(f"Verification (correct): {verify_password(password, hashed)}")
    print(f"Verification (wrong): {verify_password('WrongPassword', hashed)}")
    
    # Test JWT tokens
    print("\n=== Testing JWT Tokens ===")
    token_data = {
        "sub": "1",
        "username": "admin",
        "role": "Admin",
        "branch_id": 1
    }
    token = create_access_token(token_data)
    print(f"Token created: {token[:50]}...")
    
    decoded = decode_token(token)
    print(f"Decoded token: {decoded}")