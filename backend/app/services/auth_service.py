"""
Authentication Service
Handles user authentication and authorization logic
"""
from typing import Optional, Dict, Any
import logging

from app.database.connection import DatabaseOperations
from app.database.queries import UserQueries, LogQueries
from app.utils.security import PasswordHandler, TokenHandler
from app.utils.validators import Validators
from datetime import datetime, timedelta
import random
import smtplib
from email.message import EmailMessage
import os

logger = logging.getLogger(__name__)


class AuthService:
    """Authentication service"""
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User data dict if authenticated, None otherwise
        """
        try:
            # Get user from database
            user = DatabaseOperations.execute_query(
                UserQueries.GET_USER_BY_USERNAME,
                (username,),
                fetch_one=True
            )
            
            if not user:
                logger.warning(f"Authentication failed: User '{username}' not found")
                return None
            
            # Verify password
            if not PasswordHandler.verify_password(password, user['userPassword']):
                logger.warning(f"Authentication failed: Invalid password for user '{username}'")
                return None
            
            # Remove password from response
            user.pop('userPassword', None)
            
            logger.info(f"User '{username}' authenticated successfully")
            return user
            
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return None
    
    @staticmethod
    def create_user_token(user: Dict[str, Any]) -> str:
        """
        Create JWT token for authenticated user
        
        Args:
            user: User data dict
            
        Returns:
            JWT token
        """
        return TokenHandler.create_token_for_user(
            user_id=user['userID'],
            username=user['username'],
            role=user['userRole'],
            branch_id=user.get('branchID')
        )
    
    @staticmethod
    def login(username: str, password: str) -> Optional[Dict[str, Any]]:
        """
        Complete login process
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Dict with token and user info, or None
        """
        # Authenticate user
        user = AuthService.authenticate_user(username, password)
        
        if not user:
            return None
        
        # Create token
        token = AuthService.create_user_token(user)
        
        # Log the login
        try:
            DatabaseOperations.execute_insert(
                LogQueries.CREATE_LOG,
                (user.get('branchID'), user['userID'], None, 'Other', f"User {username} logged in")
            )
        except Exception as e:
            logger.error(f"Failed to log login event: {e}")
        
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": user
        }

    # ===== Password Reset (OTP) =====
    @staticmethod
    def _generate_otp() -> str:
        return f"{random.randint(0, 999999):06d}"

    @staticmethod
    def _send_otp_email(to_email: str, otp: str):
        """Send OTP email. Basic SMTP implementation; replace with robust mailer as needed."""
        host = os.getenv("EMAIL_HOST")
        port = int(os.getenv("EMAIL_PORT", "587"))
        user = os.getenv("EMAIL_USER")
        password = os.getenv("EMAIL_PASSWORD")
        if not (host and user and password):
            logger.warning("Email credentials not fully configured; skipping actual send")
            return
        try:
            msg = EmailMessage()
            msg["Subject"] = "Your Password Reset OTP"
            msg["From"] = user
            msg["To"] = to_email
            msg.set_content(f"Your OTP is: {otp}\nIt expires in 10 minutes.")
            with smtplib.SMTP(host, port) as server:
                server.starttls()
                server.login(user, password)
                server.send_message(msg)
            logger.info(f"Sent OTP email to {to_email}")
        except Exception as e:
            logger.error(f"Failed to send OTP email: {e}")

    @staticmethod
    def initiate_password_reset(email: str):
        """Generate and store OTP for given email (if exists)."""
        try:
            user = DatabaseOperations.execute_query(
                UserQueries.GET_USER_BY_EMAIL,
                (email,),
                fetch_one=True
            )
            if not user:
                return  # silent
            otp = AuthService._generate_otp()
            expires = datetime.utcnow() + timedelta(minutes=10)
            DatabaseOperations.execute_update(
                UserQueries.SET_RESET_OTP,
                (otp, expires, user['userID'])
            )
            AuthService._send_otp_email(email, otp)
            logger.info(f"OTP generated for user {user['userID']}")
        except Exception as e:
            logger.error(f"initiate_password_reset error: {e}")

    @staticmethod
    def reset_password_with_otp(email: str, otp: str, new_password: str) -> bool:
        try:
            user = DatabaseOperations.execute_query(
                UserQueries.GET_USER_BY_EMAIL,
                (email,),
                fetch_one=True
            )
            if not user:
                return False
            stored_otp = user.get('reset_token')
            expires = user.get('reset_expires')
            if not stored_otp or stored_otp != otp:
                return False
            if not expires or datetime.utcnow() > expires:
                return False
            hashed = PasswordHandler.hash_password(new_password)
            DatabaseOperations.execute_update(
                UserQueries.UPDATE_PASSWORD_AND_CLEAR_OTP,
                (hashed, user['userID'])
            )
            logger.info(f"Password reset for user {user['userID']}")
            return True
        except Exception as e:
            logger.error(f"reset_password_with_otp error: {e}")
            return False
    
    @staticmethod
    def create_user(user_data: Dict[str, Any]) -> Optional[int]:
        """
        Create a new user account
        
        Args:
            user_data: User information
            
        Returns:
            New user ID or None
        """
        try:
            # Validate email if provided
            if user_data.get('email') and not Validators.validate_email(user_data['email']):
                raise ValueError("Invalid email format")
            
            # Validate phone if provided
            if user_data.get('phone') and not Validators.validate_phone(user_data['phone']):
                raise ValueError("Invalid phone format")
            
            # Validate NIC
            if not Validators.validate_nic(user_data['NIC']):
                raise ValueError("Invalid NIC format")
            
            # Hash password
            hashed_password = PasswordHandler.hash_password(user_data['password'])
            
            # Insert user
            user_id = DatabaseOperations.execute_insert(
                UserQueries.CREATE_USER,
                (
                    user_data['username'],
                    hashed_password,
                    user_data['userRole'],
                    user_data.get('branchID'),
                    user_data['NIC'],
                    user_data['first_name'],
                    user_data['last_name'],
                    user_data.get('phone'),
                    user_data.get('email')
                )
            )
            
            logger.info(f"User created successfully: {user_data['username']} (ID: {user_id})")
            return user_id
            
        except Exception as e:
            logger.error(f"Failed to create user: {e}")
            raise
    
    @staticmethod
    def get_user_by_id(user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get user by ID
        
        Args:
            user_id: User ID
            
        Returns:
            User data or None
        """
        try:
            return DatabaseOperations.execute_query(
                UserQueries.GET_USER_BY_ID,
                (user_id,),
                fetch_one=True
            )
        except Exception as e:
            logger.error(f"Failed to get user: {e}")
            return None
    
    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, Any]]:
        """
        Verify JWT token and return user data
        
        Args:
            token: JWT token
            
        Returns:
            User data from token or None
        """
        return TokenHandler.get_user_from_token(token)