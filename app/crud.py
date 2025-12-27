"""
CRUD (Create, Read, Update, Delete) operations for database models.
"""
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime, timedelta
from typing import List, Optional
from app import models, schemas


# ==================== Customer CRUD ====================

def create_customer(db: Session, customer: schemas.CustomerCreate) -> models.Customer:
    """Create a new customer."""
    db_customer = models.Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer


def get_customer(db: Session, customer_id: int) -> Optional[models.Customer]:
    """Get customer by ID."""
    return db.query(models.Customer).filter(models.Customer.id == customer_id).first()


def get_customer_by_email(db: Session, email: str) -> Optional[models.Customer]:
    """Get customer by email."""
    return db.query(models.Customer).filter(models.Customer.email == email).first()


# ==================== Vendor CRUD ====================

def create_vendor(db: Session, vendor: schemas.VendorCreate) -> models.Vendor:
    """Create a new vendor."""
    db_vendor = models.Vendor(**vendor.model_dump())
    db.add(db_vendor)
    db.commit()
    db.refresh(db_vendor)
    return db_vendor


def get_vendor(db: Session, vendor_id: int) -> Optional[models.Vendor]:
    """Get vendor by ID."""
    return db.query(models.Vendor).filter(models.Vendor.id == vendor_id).first()


def get_vendors_by_city(db: Session, city: str, skip: int = 0, limit: int = 100) -> List[models.Vendor]:
    """Get all active vendors in a specific city."""
    return db.query(models.Vendor).filter(
        and_(models.Vendor.city == city, models.Vendor.is_active == True)
    ).offset(skip).limit(limit).all()


def get_all_vendors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Vendor]:
    """Get all vendors."""
    return db.query(models.Vendor).offset(skip).limit(limit).all()


# ==================== Service CRUD ====================

def create_service(db: Session, service: schemas.ServiceCreate) -> models.Service:
    """Create a new service."""
    db_service = models.Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service


def get_service(db: Session, service_id: int) -> Optional[models.Service]:
    """Get service by ID."""
    return db.query(models.Service).filter(models.Service.id == service_id).first()


def get_services_by_vendor(db: Session, vendor_id: int) -> List[models.Service]:
    """Get all active services for a vendor."""
    return db.query(models.Service).filter(
        and_(models.Service.vendor_id == vendor_id, models.Service.is_active == True)
    ).all()


# ==================== Booking CRUD ====================

def create_booking(db: Session, booking: schemas.BookingCreate) -> models.Booking:
    """
    Create a new booking.
    Automatically fetches the service price and sets it as total_price.
    """
    # Get service to fetch price
    service = get_service(db, booking.service_id)
    if not service:
        raise ValueError("Service not found")
    
    # Create booking with service price
    booking_data = booking.model_dump()
    booking_data['total_price'] = service.price
    
    db_booking = models.Booking(**booking_data)
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    """Get booking by ID."""
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def get_bookings_by_customer(db: Session, customer_id: int) -> List[models.Booking]:
    """Get all bookings for a customer."""
    return db.query(models.Booking).filter(models.Booking.customer_id == customer_id).all()


def get_bookings_by_vendor(db: Session, vendor_id: int, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """Get all bookings for a vendor."""
    return db.query(models.Booking).filter(
        models.Booking.vendor_id == vendor_id
    ).offset(skip).limit(limit).all()


def get_bookings_by_date_and_vendor(
    db: Session, 
    vendor_id: int, 
    date: datetime
) -> List[models.Booking]:
    """
    Get all bookings for a vendor on a specific date.
    Used to check slot availability.
    """
    start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = start_of_day + timedelta(days=1)
    
    return db.query(models.Booking).filter(
        and_(
            models.Booking.vendor_id == vendor_id,
            models.Booking.booking_date >= start_of_day,
            models.Booking.booking_date < end_of_day,
            models.Booking.status.in_(['pending', 'confirmed'])
        )
    ).all()


def update_booking_status(db: Session, booking_id: int, status: str) -> Optional[models.Booking]:
    """Update booking status."""
    db_booking = get_booking(db, booking_id)
    if db_booking:
        db_booking.status = status
        db_booking.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_booking)
    return db_booking


def get_all_bookings(db: Session, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """Get all bookings."""
    return db.query(models.Booking).offset(skip).limit(limit).all()
