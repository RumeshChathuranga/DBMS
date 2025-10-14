"""
Pydantic Schemas
Data models for request validation and response formatting
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from enum import Enum


# ============= Enums =============

class UserRole(str, Enum):
    """User role enumeration"""
    ADMIN = "Admin"
    MANAGER = "Manager"
    RECEPTION = "Reception"
    STAFF = "Staff"


class BookingStatus(str, Enum):
    """Booking status enumeration"""
    BOOKED = "Booked"
    CHECKED_IN = "CheckedIn"
    CHECKED_OUT = "CheckedOut"
    CANCELLED = "Cancelled"


class RoomStatus(str, Enum):
    """Room status enumeration"""
    AVAILABLE = "Available"
    OCCUPIED = "Occupied"


class PaymentMethod(str, Enum):
    """Payment method enumeration"""
    CASH = "Cash"
    CARD = "Card"
    ONLINE = "Online"
    OTHER = "Other"


class InvoiceStatus(str, Enum):
    """Invoice status enumeration"""
    PENDING = "Pending"
    PARTIALLY_PAID = "Partially Paid"
    PAID = "Paid"
    CANCELLED = "Cancelled"


class ServiceType(str, Enum):
    """Service type enumeration"""
    SPA = "Spa services"
    POOL = "Pool access"
    ROOM_SERVICE = "room service"
    LAUNDRY = "laundry"
    MINIBAR = "minibar usage"


# ============= Base Response Model =============

class ResponseModel(BaseModel):
    """Standard API response model"""
    success: bool
    message: str
    data: Optional[dict] = None


# ============= Authentication Schemas =============

class UserLogin(BaseModel):
    """User login request"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)


class UserCreate(BaseModel):
    """Create new user"""
    username: str = Field(..., min_length=3, max_length=100)
    password: str = Field(..., min_length=8)
    userRole: UserRole
    branchID: Optional[int] = None
    NIC: str = Field(..., min_length=10, max_length=20)
    first_name: str = Field(..., min_length=1, max_length=20)
    last_name: str = Field(..., min_length=1, max_length=20)
    phone: Optional[str] = Field(None, pattern=r'^\+94[0-9]{9}$')
    email: Optional[EmailStr] = None


class UserResponse(BaseModel):
    """User response model"""
    userID: int
    username: str
    userRole: str
    branchID: Optional[int]
    first_name: str
    last_name: str
    email: Optional[str]
    phone: Optional[str]
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Token response after login"""
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# ============= Password Reset Schemas =============

class ForgotPasswordRequest(BaseModel):
    """Request to initiate password reset via email"""
    email: EmailStr


class ForgotPasswordResponse(BaseModel):
    """Generic response to avoid user enumeration"""
    success: bool
    message: str


class ResetPasswordRequest(BaseModel):
    """Submit OTP + new password"""
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6, pattern=r"^[0-9]{6}$")
    new_password: str = Field(..., min_length=8)

    @validator('new_password')
    def strong_password(cls, v):  # basic check; extend as needed
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


# ============= Guest Schemas =============

class GuestCreate(BaseModel):
    """Create new guest"""
    firstName: str = Field(..., min_length=1, max_length=50)
    lastName: str = Field(..., min_length=1, max_length=50)
    phone: str = Field(..., pattern=r'^\+94[0-9]{9}$')
    email: Optional[EmailStr] = None
    idNumber: str = Field(..., min_length=10, max_length=30)


class GuestUpdate(BaseModel):
    """Update guest information"""
    firstName: Optional[str] = Field(None, min_length=1, max_length=50)
    lastName: Optional[str] = Field(None, min_length=1, max_length=50)
    phone: Optional[str] = Field(None, pattern=r'^\+94[0-9]{9}$')
    email: Optional[EmailStr] = None


class GuestResponse(BaseModel):
    """Guest response model"""
    guestID: int
    firstName: str
    lastName: str
    phone: str
    email: Optional[str]
    idNumber: str
    
    class Config:
        from_attributes = True


# ============= Branch Schemas =============

class BranchResponse(BaseModel):
    """Branch response model"""
    branchID: int
    branchLocation: str
    rating: Optional[Decimal]
    phone: str
    email: str
    
    class Config:
        from_attributes = True


# ============= Room Type Schemas =============

class RoomTypeResponse(BaseModel):
    """Room type response model"""
    typeID: int
    typeName: str
    capacity: int
    currRate: Decimal
    
    class Config:
        from_attributes = True


# ============= Room Schemas =============

class RoomResponse(BaseModel):
    """Room response model"""
    roomID: int
    branchID: int
    typeID: int
    roomNo: int
    roomStatus: str
    typeName: Optional[str] = None
    capacity: Optional[int] = None
    currRate: Optional[Decimal] = None
    branchLocation: Optional[str] = None
    
    class Config:
        from_attributes = True


class AvailableRoomQuery(BaseModel):
    """Query for available rooms"""
    branchID: int
    typeID: int
    checkInDate: datetime
    checkOutDate: datetime
    
    @validator('checkOutDate')
    def check_out_after_check_in(cls, v, values):
        if 'checkInDate' in values and v <= values['checkInDate']:
            raise ValueError('checkOutDate must be after checkInDate')
        return v


# ============= Booking Schemas =============

class BookingCreate(BaseModel):
    """Create new booking"""
    guestID: int
    branchID: int
    roomID: int
    checkInDate: datetime
    checkOutDate: datetime
    numGuests: int = Field(..., gt=0)
    
    @validator('checkOutDate')
    def check_out_after_check_in(cls, v, values):
        if 'checkInDate' in values and v <= values['checkInDate']:
            raise ValueError('checkOutDate must be after checkInDate')
        return v


class BookingUpdate(BaseModel):
    """Update booking details"""
    checkInDate: Optional[datetime] = None
    checkOutDate: Optional[datetime] = None
    numGuests: Optional[int] = Field(None, gt=0)
    
    @validator('checkOutDate')
    def check_out_after_check_in(cls, v, values):
        if v and 'checkInDate' in values and values['checkInDate'] and v <= values['checkInDate']:
            raise ValueError('checkOutDate must be after checkInDate')
        return v


class BookingResponse(BaseModel):
    """Booking response model"""
    bookingID: int
    guestID: int
    branchID: int
    roomID: int
    rate: Decimal
    checkInDate: datetime
    checkOutDate: datetime
    numGuests: int
    bookingStatus: str
    # Additional joined fields
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    roomNo: Optional[int] = None
    typeName: Optional[str] = None
    branchLocation: Optional[str] = None
    
    class Config:
        from_attributes = True


# ============= Service Schemas =============

class ServiceResponse(BaseModel):
    """Service response model"""
    serviceID: int
    serviceType: str
    unit: Optional[str]
    ratePerUnit: Decimal
    
    class Config:
        from_attributes = True


class ServiceUsageCreate(BaseModel):
    """Create service usage"""
    bookingID: int
    serviceID: int
    quantity: int = Field(default=1, gt=0)


class ServiceUsageResponse(BaseModel):
    """Service usage response model"""
    usageID: int
    bookingID: int
    serviceID: int
    rate: Decimal
    quantity: int
    usedAt: datetime
    serviceType: Optional[str] = None
    unit: Optional[str] = None
    totalCharge: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


# ============= Invoice & Payment Schemas =============

class InvoiceResponse(BaseModel):
    """Invoice response model"""
    invoiceID: int
    bookingID: int
    policyID: Optional[int]
    discountCode: Optional[int]
    paymentPlan: str
    roomCharges: Decimal
    serviceCharges: Decimal
    taxAmount: Decimal
    discountAmount: Decimal
    settledAmount: Decimal
    invoiceStatus: str
    totalAmount: Optional[Decimal] = None
    balanceDue: Optional[Decimal] = None
    
    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    """Create payment"""
    invoiceID: int
    paymentMethod: PaymentMethod
    amount: Decimal = Field(..., gt=0)


class PaymentResponse(BaseModel):
    """Payment response model"""
    transactionID: int
    invoiceID: int
    transactionDate: date
    paymentMethod: str
    amount: Decimal
    
    class Config:
        from_attributes = True


# ============= Report Schemas =============

class OccupancyReportQuery(BaseModel):
    """Occupancy report query parameters"""
    startDate: date
    endDate: date
    branchID: Optional[int] = 0  # 0 means all branches


class RevenueReportQuery(BaseModel):
    """Revenue report query parameters"""
    year: int = Field(..., ge=2000, le=2100)
    month: int = Field(..., ge=1, le=12)
    branchID: Optional[int] = 0


class ServiceUsageReportQuery(BaseModel):
    """Service usage report query parameters"""
    startDate: date
    endDate: date
    branchID: Optional[int] = 0


# ============= Pagination Schema =============

class PaginationParams(BaseModel):
    """Pagination parameters"""
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)