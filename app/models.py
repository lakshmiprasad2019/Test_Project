"""
SQLAlchemy database models for the Wash Booking application.
"""
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Numeric, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Customer(Base):
    """
    Customer model - stores user information.
    """
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    city = Column(String(100), nullable=False, index=True)  # Indian city
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    bookings = relationship("Booking", back_populates="customer")


class Vendor(Base):
    """
    Vendor model - stores service provider information.
    """
    __tablename__ = "vendors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    phone = Column(String(15), unique=True, nullable=False)
    city = Column(String(100), nullable=False, index=True)  # Indian city
    service_area = Column(String(200), nullable=False)  # Pincode/Neighborhood
    address = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    services = relationship("Service", back_populates="vendor")
    bookings = relationship("Booking", back_populates="vendor")


class Service(Base):
    """
    Service model - stores services offered by vendors.
    """
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    name = Column(String(100), nullable=False)  # e.g., Deep Clean, Interior Detailing
    description = Column(Text, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)  # Price in INR
    duration_minutes = Column(Integer, nullable=False)  # Service duration
    vehicle_type = Column(String(20), nullable=False)  # bike or car
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    vendor = relationship("Vendor", back_populates="services")
    bookings = relationship("Booking", back_populates="service")


class Booking(Base):
    """
    Booking model - stores booking information.
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    vendor_id = Column(Integer, ForeignKey("vendors.id"), nullable=False)
    service_id = Column(Integer, ForeignKey("services.id"), nullable=False)
    
    # Booking details
    city = Column(String(100), nullable=False, index=True)
    booking_date = Column(DateTime, nullable=False, index=True)  # Date and time of service
    status = Column(String(20), default="pending")  # pending, confirmed, completed, cancelled
    vehicle_number = Column(String(20), nullable=True)
    vehicle_type = Column(String(20), nullable=False)  # bike or car
    
    # Address details
    service_address = Column(Text, nullable=True)
    pincode = Column(String(10), nullable=True)
    
    # Pricing
    total_price = Column(Numeric(10, 2), nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    customer = relationship("Customer", back_populates="bookings")
    vendor = relationship("Vendor", back_populates="bookings")
    service = relationship("Service", back_populates="bookings")
