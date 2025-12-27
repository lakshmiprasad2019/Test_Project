# Bike and Car Wash Booking Application

A comprehensive web-based booking platform for bike and car wash services tailored for Indian cities.

## Tech Stack

- **Backend**: Python with FastAPI
- **Database**: PostgreSQL
- **Containerization**: Docker
- **Orchestration**: Kubernetes (K8s)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic schemas for validation
│   ├── database.py          # Database connection setup
│   ├── crud.py              # CRUD operations
│   └── routers/
│       ├── __init__.py
│       ├── bookings.py      # Booking endpoints
│       └── vendors.py       # Vendor endpoints
├── k8s/
│   ├── deployment.yaml      # Kubernetes deployment
│   ├── service.yaml         # Kubernetes service
│   └── pvc.yaml             # Persistent volume claim for Postgres
├── Dockerfile               # Docker image for the app
├── docker-compose.yaml      # Local development setup
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Features

### Customer Module
- Select city from Indian cities
- Pick date (restricted to current year/month)
- Select available time slots
- Book services

### Vendor Module
- Register with city information
- List specific services (Deep Clean, Interior Detailing, etc.)
- Define service area (Pincode/Neighborhood)

## Setup Instructions

### Local Development with Docker Compose

1. **Start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access the API**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Database: localhost:5432

### Kubernetes Deployment

1. **Apply Kubernetes manifests**:
   ```bash
   kubectl apply -f k8s/pvc.yaml
   kubectl apply -f k8s/deployment.yaml
   kubectl apply -f k8s/service.yaml
   ```

2. **Check deployment status**:
   ```bash
   kubectl get pods
   kubectl get services
   ```

3. **Access the application**:
   ```bash
   kubectl port-forward service/wash-booking-service 8000:8000
   ```

## API Endpoints

### Bookings
- `POST /api/bookings/` - Create a new booking
- `GET /api/bookings/{booking_id}` - Get booking details
- `GET /api/bookings/` - List all bookings

### Vendors
- `POST /api/vendors/` - Register a new vendor
- `GET /api/vendors/{vendor_id}` - Get vendor details
- `GET /api/vendors/` - List all vendors
- `GET /api/vendors/by-city/{city}` - Get vendors by city

## Database Schema

### Tables
- **customers**: User information
- **vendors**: Service provider information
- **services**: Available services
- **bookings**: Booking records

## Environment Variables

Create a `.env` file for local development:

```env
DATABASE_URL=postgresql://washuser:washpass@db:5432/washbooking
POSTGRES_USER=washuser
POSTGRES_PASSWORD=washpass
POSTGRES_DB=washbooking
```

## Development

### Install dependencies locally:
```bash
pip install -r requirements.txt
```

### Run migrations:
```bash
# The app will auto-create tables on startup
python -m app.main
```

## License

MIT License
