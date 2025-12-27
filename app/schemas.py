"""
Pydantic schemas for request/response validation.
"""
from pydantic import BaseModel, EmailStr, Field, validator
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


# ==================== Customer Schemas ====================

class CustomerBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^[6-9]\d{9}$")  # Indian phone number format
    city: str = Field(..., min_length=1, max_length=100)


class CustomerCreate(CustomerBase):
    pass


class CustomerResponse(CustomerBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Vendor Schemas ====================

class VendorBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: str = Field(..., pattern=r"^[6-9]\d{9}$")  # Indian phone number format
    city: str = Field(..., min_length=1, max_length=100)
    service_area: str = Field(..., min_length=1, max_length=200, description="Pincode or Neighborhood")
    address: Optional[str] = None


class VendorCreate(VendorBase):
    pass


class VendorResponse(VendorBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Service Schemas ====================

class ServiceBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    price: Decimal = Field(..., gt=0, decimal_places=2)
    duration_minutes: int = Field(..., gt=0)
    vehicle_type: str = Field(..., pattern=r"^(bike|car)$")


class ServiceCreate(ServiceBase):
    vendor_id: int


class ServiceResponse(ServiceBase):
    id: int
    vendor_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# ==================== Booking Schemas ====================

class BookingBase(BaseModel):
    city: str = Field(..., min_length=1, max_length=100)
    booking_date: datetime
    vehicle_type: str = Field(..., pattern=r"^(bike|car)$")
    vehicle_number: Optional[str] = Field(None, max_length=20)
    service_address: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r"^\d{6}$")  # Indian pincode format

    @validator('booking_date')
    def validate_booking_date(cls, v):
        """
        Validate that booking date is in the current year and month.
        """
        now = datetime.now()
        if v.year != now.year or v.month != now.month:
            raise ValueError('Booking date must be in the current year and month')
        if v < now:
            raise ValueError('Booking date cannot be in the past')
        return v


class BookingCreate(BookingBase):
    customer_id: int
    vendor_id: int
    service_id: int


class BookingResponse(BookingBase):
    id: int
    customer_id: int
    vendor_id: int
    service_id: int
    status: str
    total_price: Decimal
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingDetailResponse(BookingResponse):
    """
    Extended booking response with related entity details.
    """
    customer: CustomerResponse
    vendor: VendorResponse
    service: ServiceResponse

    class Config:
        from_attributes = True


# ==================== Available Slots Schema ====================

class AvailableSlot(BaseModel):
    """
    Schema for available time slots.
    """
    slot_time: datetime
    is_available: bool


class AvailableSlotsResponse(BaseModel):
    """
    Response schema for available slots query.
    """
    date: str
    vendor_id: int
    slots: List[AvailableSlot]
