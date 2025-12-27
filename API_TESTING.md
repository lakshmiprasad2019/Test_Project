# API Testing Examples

This document provides comprehensive examples for testing all API endpoints.

## Base URL
- Local: `http://localhost:8000`
- Kubernetes: `http://<EXTERNAL-IP>:8000`

## API Documentation
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

---

## Customer Endpoints

### Create Customer
```bash
POST /api/bookings/customers/

curl -X POST "http://localhost:8000/api/bookings/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Priya Sharma",
    "email": "priya.sharma@example.com",
    "phone": "9876543210",
    "city": "Bangalore"
  }'
```

**Response**:
```json
{
  "id": 1,
  "name": "Priya Sharma",
  "email": "priya.sharma@example.com",
  "phone": "9876543210",
  "city": "Bangalore",
  "created_at": "2025-12-27T15:00:00",
  "updated_at": "2025-12-27T15:00:00"
}
```

---

## Vendor Endpoints

### Register Vendor
```bash
POST /api/vendors/

curl -X POST "http://localhost:8000/api/vendors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SparkleClean Auto Services",
    "email": "contact@sparkleclean.com",
    "phone": "9123456789",
    "city": "Bangalore",
    "service_area": "560001, Koramangala, Indiranagar, HSR Layout",
    "address": "45 MG Road, Bangalore - 560001"
  }'
```

### Get Vendor by ID
```bash
GET /api/vendors/{vendor_id}

curl "http://localhost:8000/api/vendors/1"
```

### List All Vendors
```bash
GET /api/vendors/

curl "http://localhost:8000/api/vendors/?skip=0&limit=10"
```

### Get Vendors by City
```bash
GET /api/vendors/by-city/{city}

curl "http://localhost:8000/api/vendors/by-city/Bangalore"
```

---

## Service Endpoints

### Create Service for Vendor
```bash
POST /api/vendors/{vendor_id}/services

# Deep Clean Service for Cars
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deep Clean",
    "description": "Complete interior and exterior deep cleaning with wax polish",
    "price": 799.00,
    "duration_minutes": 90,
    "vehicle_type": "car"
  }'

# Quick Wash for Bikes
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Quick Wash",
    "description": "Fast exterior wash and dry",
    "price": 149.00,
    "duration_minutes": 30,
    "vehicle_type": "bike"
  }'

# Interior Detailing for Cars
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Interior Detailing",
    "description": "Complete interior cleaning, vacuum, and sanitization",
    "price": 599.00,
    "duration_minutes": 60,
    "vehicle_type": "car"
  }'
```

### Get Vendor Services
```bash
GET /api/vendors/{vendor_id}/services

curl "http://localhost:8000/api/vendors/1/services"
```

---

## Booking Endpoints

### Check Available Slots
```bash
GET /api/bookings/available-slots/{vendor_id}

curl "http://localhost:8000/api/bookings/available-slots/1?date=2025-12-28&service_id=1"
```

**Response**:
```json
{
  "date": "2025-12-28",
  "vendor_id": 1,
  "slots": [
    {
      "slot_time": "2025-12-28T09:00:00",
      "is_available": true
    },
    {
      "slot_time": "2025-12-28T10:00:00",
      "is_available": false
    },
    {
      "slot_time": "2025-12-28T11:00:00",
      "is_available": true
    }
  ]
}
```

### Create Booking
```bash
POST /api/bookings/

curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "vendor_id": 1,
    "service_id": 1,
    "city": "Bangalore",
    "booking_date": "2025-12-28T10:00:00",
    "vehicle_type": "car",
    "vehicle_number": "KA01AB1234",
    "service_address": "123 Residency Road, Bangalore",
    "pincode": "560001"
  }'
```

**Response**:
```json
{
  "id": 1,
  "customer_id": 1,
  "vendor_id": 1,
  "service_id": 1,
  "city": "Bangalore",
  "booking_date": "2025-12-28T10:00:00",
  "status": "pending",
  "vehicle_number": "KA01AB1234",
  "vehicle_type": "car",
  "service_address": "123 Residency Road, Bangalore",
  "pincode": "560001",
  "total_price": 799.00,
  "created_at": "2025-12-27T15:30:00",
  "updated_at": "2025-12-27T15:30:00"
}
```

### Get Booking Details
```bash
GET /api/bookings/{booking_id}

curl "http://localhost:8000/api/bookings/1"
```

### List All Bookings
```bash
GET /api/bookings/

curl "http://localhost:8000/api/bookings/?skip=0&limit=10"
```

### Get Customer Bookings
```bash
GET /api/bookings/customer/{customer_id}

curl "http://localhost:8000/api/bookings/customer/1"
```

### Get Vendor Bookings
```bash
GET /api/bookings/vendor/{vendor_id}

curl "http://localhost:8000/api/bookings/vendor/1?skip=0&limit=10"
```

### Update Booking Status
```bash
PATCH /api/bookings/{booking_id}/status

# Confirm booking
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=confirmed"

# Complete booking
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=completed"

# Cancel booking
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=cancelled"
```

---

## Complete Workflow Example

### 1. Create a Customer
```bash
curl -X POST "http://localhost:8000/api/bookings/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Amit Patel",
    "email": "amit.patel@example.com",
    "phone": "9988776655",
    "city": "Mumbai"
  }'
```

### 2. Register a Vendor
```bash
curl -X POST "http://localhost:8000/api/vendors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mumbai Premium Wash",
    "email": "info@mumbaiwash.com",
    "phone": "9876543210",
    "city": "Mumbai",
    "service_area": "400001, Andheri, Bandra, Juhu",
    "address": "789 Marine Drive, Mumbai - 400001"
  }'
```

### 3. Add Services
```bash
# Car Deep Clean
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Deep Clean",
    "description": "Complete car wash with interior detailing and wax",
    "price": 999.00,
    "duration_minutes": 120,
    "vehicle_type": "car"
  }'

# Bike Wash
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bike Wash & Polish",
    "description": "Exterior wash with polish",
    "price": 199.00,
    "duration_minutes": 45,
    "vehicle_type": "bike"
  }'
```

### 4. Check Available Slots
```bash
curl "http://localhost:8000/api/bookings/available-slots/1?date=2025-12-28&service_id=1"
```

### 5. Create Booking
```bash
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "vendor_id": 1,
    "service_id": 1,
    "city": "Mumbai",
    "booking_date": "2025-12-28T14:00:00",
    "vehicle_type": "car",
    "vehicle_number": "MH02CD5678",
    "service_address": "456 Linking Road, Bandra West, Mumbai",
    "pincode": "400050"
  }'
```

### 6. Update Booking Status
```bash
# Vendor confirms booking
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=confirmed"

# After service completion
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=completed"
```

---

## Error Handling Examples

### Invalid Phone Number
```bash
curl -X POST "http://localhost:8000/api/bookings/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "1234567890",
    "city": "Delhi"
  }'
```
**Error**: Phone number must start with 6-9

### Invalid Pincode
```bash
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "vendor_id": 1,
    "service_id": 1,
    "city": "Mumbai",
    "booking_date": "2025-12-28T10:00:00",
    "vehicle_type": "car",
    "pincode": "12345"
  }'
```
**Error**: Pincode must be 6 digits

### Booking in Past Month
```bash
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_id": 1,
    "vendor_id": 1,
    "service_id": 1,
    "city": "Mumbai",
    "booking_date": "2025-11-28T10:00:00",
    "vehicle_type": "car"
  }'
```
**Error**: Booking date must be in current year and month

---

## Testing with Python

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Create customer
customer_data = {
    "name": "Rahul Verma",
    "email": "rahul@example.com",
    "phone": "9876543210",
    "city": "Delhi"
}
response = requests.post(f"{BASE_URL}/api/bookings/customers/", json=customer_data)
customer = response.json()
print(f"Customer created: {customer['id']}")

# Register vendor
vendor_data = {
    "name": "Delhi Auto Spa",
    "email": "delhi@autospa.com",
    "phone": "9123456789",
    "city": "Delhi",
    "service_area": "110001, Connaught Place, Karol Bagh",
    "address": "123 CP, New Delhi"
}
response = requests.post(f"{BASE_URL}/api/vendors/", json=vendor_data)
vendor = response.json()
print(f"Vendor created: {vendor['id']}")

# Create booking
booking_data = {
    "customer_id": customer['id'],
    "vendor_id": vendor['id'],
    "service_id": 1,
    "city": "Delhi",
    "booking_date": "2025-12-28T11:00:00",
    "vehicle_type": "car",
    "vehicle_number": "DL01AB1234"
}
response = requests.post(f"{BASE_URL}/api/bookings/", json=booking_data)
booking = response.json()
print(f"Booking created: {booking['id']}")
```

---

## Popular Indian Cities for Testing

- Mumbai
- Delhi
- Bangalore
- Hyderabad
- Chennai
- Kolkata
- Pune
- Ahmedabad
- Jaipur
- Lucknow
