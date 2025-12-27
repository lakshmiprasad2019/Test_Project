"""
Vendor API endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(
    prefix="/api/vendors",
    tags=["vendors"]
)


@router.post("/", response_model=schemas.VendorResponse, status_code=status.HTTP_201_CREATED)
def register_vendor(
    vendor: schemas.VendorCreate,
    db: Session = Depends(get_db)
):
    """
    Register a new vendor.
    
    Required fields:
    - name: Vendor business name
    - email: Unique email address
    - phone: Indian phone number (10 digits starting with 6-9)
    - city: Indian city where vendor operates
    - service_area: Pincode or neighborhood coverage
    - address: Optional physical address
    """
    # Check if vendor with email already exists
    existing_vendor = db.query(crud.models.Vendor).filter(
        crud.models.Vendor.email == vendor.email
    ).first()
    
    if existing_vendor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor with this email already exists"
        )
    
    # Check if vendor with phone already exists
    existing_phone = db.query(crud.models.Vendor).filter(
        crud.models.Vendor.phone == vendor.phone
    ).first()
    
    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vendor with this phone number already exists"
        )
    
    return crud.create_vendor(db=db, vendor=vendor)


@router.get("/{vendor_id}", response_model=schemas.VendorResponse)
def get_vendor(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get vendor details by ID.
    """
    vendor = crud.get_vendor(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    return vendor


@router.get("/", response_model=List[schemas.VendorResponse])
def list_vendors(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all vendors with pagination.
    """
    vendors = crud.get_all_vendors(db=db, skip=skip, limit=limit)
    return vendors


@router.get("/by-city/{city}", response_model=List[schemas.VendorResponse])
def get_vendors_by_city(
    city: str,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all active vendors in a specific city.
    Useful for customers to find vendors in their area.
    """
    vendors = crud.get_vendors_by_city(db=db, city=city, skip=skip, limit=limit)
    return vendors


@router.post("/{vendor_id}/services", response_model=schemas.ServiceResponse, status_code=status.HTTP_201_CREATED)
def create_vendor_service(
    vendor_id: int,
    service: schemas.ServiceBase,
    db: Session = Depends(get_db)
):
    """
    Create a new service for a vendor.
    
    Service types examples:
    - Deep Clean
    - Interior Detailing
    - Exterior Wash
    - Full Service
    - Polish & Wax
    """
    # Check if vendor exists
    vendor = crud.get_vendor(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    # Create service with vendor_id
    service_data = schemas.ServiceCreate(**service.model_dump(), vendor_id=vendor_id)
    return crud.create_service(db=db, service=service_data)


@router.get("/{vendor_id}/services", response_model=List[schemas.ServiceResponse])
def get_vendor_services(
    vendor_id: int,
    db: Session = Depends(get_db)
):
    """
    Get all active services offered by a vendor.
    """
    # Check if vendor exists
    vendor = crud.get_vendor(db=db, vendor_id=vendor_id)
    if not vendor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vendor not found"
        )
    
    services = crud.get_services_by_vendor(db=db, vendor_id=vendor_id)
    return services
