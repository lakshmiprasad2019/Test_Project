"""
Booking API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/api/bookings",
    tags=["bookings"]
)


@router.post("/", response_model=schemas.BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new booking.
    
    Validations:
    - Booking date must be in current year and month
    - Customer, vendor, and service must exist
    - Checks for slot availability (basic implementation)
    
    Required fields:
    - customer_id: ID of the customer making the booking
    - vendor_id: ID of the vendor providing the service
    - service_id: ID of the service to be booked
    - city: City where service will be provided
    - booking_date: Date and time of service (current year/month only)
    - vehicle_type: 'bike' or 'car'
    - vehicle_number: Optional vehicle registration number
    - service_address: Optional address for service
    - pincode: Optional 6-digit Indian pincode
    """
    # Validate customer exists
    customer = crud.get_customer(db=db, customer_id=booking.customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    # Validate vendor exists and is active
    vendor = crud.get_vendor(db=db, vendor_id=booking.vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    if not vendor.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor is not active"
        )
    
    # Validate service exists and belongs to vendor
    service = crud.get_service(db=db, service_id=booking.service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    if service.vendor_id != booking.vendor_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service does not belong to the specified vendor"
        )
    if not service.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Service is not active"
        )
    
    # Validate vehicle type matches service
    if service.vehicle_type != booking.vehicle_type:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Service is for {service.vehicle_type} only, but booking is for {booking.vehicle_type}"
        )
    
    # Check if slot is available (basic check - can be enhanced)
    existing_bookings = crud.get_bookings_by_date_and_vendor(
        db=db,
        vendor_id=booking.vendor_id,
        date=booking.booking_date
    )
    
    # Check for time conflicts (within service duration)
    for existing in existing_bookings:
        time_diff = abs((existing.booking_date - booking.booking_date).total_seconds() / 60)
        if time_diff < service.duration_minutes:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time slot not available. Please choose a different time."
            )
    
    # Create booking
    try:
        return crud.create_booking(db=db, booking=booking)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{booking_id}", response_model=schemas.BookingDetailResponse)
def get_booking(
    booking_id: int,
    db: Session = Depends(get_db)
):
    """
    Get booking details by ID with related customer, vendor, and service information.
    """
    booking = crud.get_booking(db=db, booking_id=booking_id)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking


@router.get("/", response_model=List[schemas.BookingResponse])
def list_bookings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all bookings with pagination.
    """
    bookings = crud.get_all_bookings(db=db, skip=skip, limit=limit)
    return bookings


@router.get("/customer/{customer_id}", response_model=List[schemas.BookingResponse])
def get_customer_bookings(
    customer_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all bookings for a specific customer.
    """
    customer = crud.get_customer(db=db, customer_id=customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found"
        )
    
    bookings = crud.get_bookings_by_customer(db=db, customer_id=customer_id)
    return bookings


@router.get("/vendor/{vendor_id}", response_model=List[schemas.BookingResponse])
def get_vendor_bookings(
    vendor_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all bookings for a specific vendor.
    """
    vendor = crud.get_vendor(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    bookings = crud.get_bookings_by_vendor(db=db, vendor_id=vendor_id, skip=skip, limit=limit)
    return bookings


@router.patch("/{booking_id}/status", response_model=schemas.BookingResponse)
def update_booking_status(
    booking_id: int,
    status: str = Query(..., regex="^(pending|confirmed|completed|cancelled)$"),
    db: Session = Depends(get_db)
):
    """
    Update booking status.
    
    Valid statuses: pending, confirmed, completed, cancelled
    """
    booking = crud.update_booking_status(db=db, booking_id=booking_id, status=status)
    if not booking:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Booking not found"
        )
    return booking


@router.get("/available-slots/{vendor_id}", response_model=schemas.AvailableSlotsResponse)
def get_available_slots(
    vendor_id: int,
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    service_id: int = Query(..., description="Service ID to check availability for"),
    db: Session = Depends(get_db)
):
    """
    Get available time slots for a vendor on a specific date.
    
    Returns slots from 9 AM to 6 PM in 1-hour intervals.
    Marks slots as unavailable if they conflict with existing bookings.
    """
    # Validate vendor
    vendor = crud.get_vendor(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Validate service
    service = crud.get_service(db=db, service_id=service_id)
    if not service:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service not found"
        )
    
    # Parse date
    try:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid date format. Use YYYY-MM-DD"
        )
    
    # Validate date is in current year and month
    now = datetime.now()
    if target_date.year != now.year or target_date.month != now.month:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Date must be in current year and month"
        )
    
    # Get existing bookings for the date
    existing_bookings = crud.get_bookings_by_date_and_vendor(
        db=db,
        vendor_id=vendor_id,
        date=target_date
    )
    
    # Generate time slots (9 AM to 6 PM, hourly)
    slots = []
    for hour in range(9, 18):  # 9 AM to 5 PM (last slot at 5 PM)
        slot_time = target_date.replace(hour=hour, minute=0, second=0, microsecond=0)
        
        # Check if slot is available
        is_available = True
        for booking in existing_bookings:
            time_diff = abs((booking.booking_date - slot_time).total_seconds() / 60)
            if time_diff < service.duration_minutes:
                is_available = False
                break
        
        slots.append(schemas.AvailableSlot(
            slot_time=slot_time,
            is_available=is_available
        ))
    
    return schemas.AvailableSlotsResponse(
        date=date,
        vendor_id=vendor_id,
        slots=slots
    )


@router.post("/customers/", response_model=schemas.CustomerResponse, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new customer.
    
    Required fields:
    - name: Customer name
    - email: Unique email address
    - phone: Indian phone number (10 digits starting with 6-9)
    - city: Indian city
    """
    # Check if customer with email already exists
    existing_customer = crud.get_customer_by_email(db=db, email=customer.email)
    if existing_customer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Customer with this email already exists"
        )
    
    return crud.create_customer(db=db, customer=customer)
