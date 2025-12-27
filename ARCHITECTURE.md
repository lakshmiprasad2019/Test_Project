# System Architecture

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                             │
│  (Web Browser, Mobile App, API Clients, curl, Postman)          │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             │ HTTP/HTTPS
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    KUBERNETES CLUSTER                            │
│                                                                  │
│  ┌────────────────────────────────────────────────────────┐    │
│  │              LoadBalancer Service                       │    │
│  │         (wash-booking-service:8000)                     │    │
│  └──────────────────────┬─────────────────────────────────┘    │
│                         │                                        │
│                         │ Routes to                              │
│                         │                                        │
│  ┌──────────────────────▼─────────────────────────────────┐    │
│  │         FastAPI Application Pods (3 replicas)          │    │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐         │    │
│  │  │  Pod 1   │    │  Pod 2   │    │  Pod 3   │         │    │
│  │  │ FastAPI  │    │ FastAPI  │    │ FastAPI  │         │    │
│  │  │ Uvicorn  │    │ Uvicorn  │    │ Uvicorn  │         │    │
│  │  │ Port:8000│    │ Port:8000│    │ Port:8000│         │    │
│  │  └─────┬────┘    └─────┬────┘    └─────┬────┘         │    │
│  └────────┼───────────────┼───────────────┼──────────────┘    │
│           │               │               │                     │
│           └───────────────┼───────────────┘                     │
│                           │                                     │
│                           │ Database Connection                 │
│                           │                                     │
│  ┌────────────────────────▼────────────────────────────────┐   │
│  │           ClusterIP Service (Internal)                   │   │
│  │         (postgres-service:5432)                          │   │
│  └──────────────────────┬──────────────────────────────────┘   │
│                         │                                       │
│  ┌──────────────────────▼──────────────────────────────────┐   │
│  │         PostgreSQL Database Pod                          │   │
│  │  ┌────────────────────────────────────────┐             │   │
│  │  │  PostgreSQL 15                         │             │   │
│  │  │  Port: 5432                            │             │   │
│  │  │  Database: washbooking                 │             │   │
│  │  └────────────────┬───────────────────────┘             │   │
│  └───────────────────┼─────────────────────────────────────┘   │
│                      │                                          │
│  ┌───────────────────▼─────────────────────────────────────┐   │
│  │      Persistent Volume (PVC)                            │   │
│  │      Storage: 5Gi                                       │   │
│  │      Data: /var/lib/postgresql/data                     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Application Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      FastAPI Application                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    main.py (Entry Point)                  │  │
│  │  - FastAPI app initialization                            │  │
│  │  - CORS middleware                                        │  │
│  │  - Router registration                                    │  │
│  │  - Health check endpoints                                 │  │
│  └────────────────────┬─────────────────────────────────────┘  │
│                       │                                          │
│  ┌────────────────────┴─────────────────────────────────────┐  │
│  │                    Routers Layer                          │  │
│  │  ┌─────────────────────┐  ┌──────────────────────────┐   │  │
│  │  │  bookings.py        │  │  vendors.py              │   │  │
│  │  │  - Create booking   │  │  - Register vendor       │   │  │
│  │  │  - Get bookings     │  │  - Get vendors           │   │  │
│  │  │  - Check slots      │  │  - Add services          │   │  │
│  │  │  - Update status    │  │  - Get by city           │   │  │
│  │  └──────────┬──────────┘  └──────────┬───────────────┘   │  │
│  └─────────────┼────────────────────────┼───────────────────┘  │
│                │                        │                       │
│  ┌─────────────┴────────────────────────┴───────────────────┐  │
│  │                    Business Logic Layer                   │  │
│  │  ┌──────────────────────────────────────────────────┐    │  │
│  │  │  crud.py (CRUD Operations)                       │    │  │
│  │  │  - create_customer()                             │    │  │
│  │  │  - create_vendor()                               │    │  │
│  │  │  - create_booking()                              │    │  │
│  │  │  - get_available_slots()                         │    │  │
│  │  │  - update_booking_status()                       │    │  │
│  │  └──────────────────┬───────────────────────────────┘    │  │
│  └─────────────────────┼───────────────────────────────────┘  │
│                        │                                       │
│  ┌─────────────────────┴───────────────────────────────────┐  │
│  │                  Validation Layer                        │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  schemas.py (Pydantic Models)                    │   │  │
│  │  │  - CustomerCreate, CustomerResponse              │   │  │
│  │  │  - VendorCreate, VendorResponse                  │   │  │
│  │  │  - BookingCreate, BookingResponse                │   │  │
│  │  │  - Input validation (phone, pincode, dates)      │   │  │
│  │  └──────────────────┬───────────────────────────────┘   │  │
│  └─────────────────────┼───────────────────────────────────┘  │
│                        │                                       │
│  ┌─────────────────────┴───────────────────────────────────┐  │
│  │                    Data Layer                            │  │
│  │  ┌──────────────────────────────────────────────────┐   │  │
│  │  │  models.py (SQLAlchemy Models)                   │   │  │
│  │  │  - Customer, Vendor, Service, Booking            │   │  │
│  │  │  - Relationships and constraints                 │   │  │
│  │  └──────────────────┬───────────────────────────────┘   │  │
│  │                     │                                    │  │
│  │  ┌──────────────────▼───────────────────────────────┐   │  │
│  │  │  database.py (Database Connection)               │   │  │
│  │  │  - SQLAlchemy engine                             │   │  │
│  │  │  - Session management                            │   │  │
│  │  │  - Connection pooling                            │   │  │
│  │  └──────────────────┬───────────────────────────────┘   │  │
│  └─────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼──────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  PostgreSQL Database │
              │  - customers         │
              │  - vendors           │
              │  - services          │
              │  - bookings          │
              └──────────────────────┘
```

---

## Request Flow

### Example: Create Booking

```
1. Client Request
   │
   ├─► POST /api/bookings/
   │   Body: {customer_id, vendor_id, service_id, ...}
   │
   ▼
2. Kubernetes LoadBalancer
   │
   ├─► Routes to one of 3 FastAPI pods
   │
   ▼
3. FastAPI Application (main.py)
   │
   ├─► CORS middleware check
   ├─► Route to bookings router
   │
   ▼
4. Bookings Router (routers/bookings.py)
   │
   ├─► Validate request with Pydantic schema
   │   (BookingCreate schema)
   │
   ▼
5. Validation Layer (schemas.py)
   │
   ├─► Check phone format: ^[6-9]\d{9}$
   ├─► Check pincode format: ^\d{6}$
   ├─► Check date: current year/month only
   ├─► Check vehicle type: bike or car
   │
   ▼
6. Business Logic (crud.py)
   │
   ├─► Verify customer exists
   ├─► Verify vendor exists and is active
   ├─► Verify service exists and matches vendor
   ├─► Check vehicle type matches service
   ├─► Check slot availability
   ├─► Calculate total price
   │
   ▼
7. Data Layer (models.py + database.py)
   │
   ├─► Create Booking object
   ├─► Add to database session
   ├─► Commit transaction
   │
   ▼
8. PostgreSQL Database
   │
   ├─► Insert into bookings table
   ├─► Update indexes
   ├─► Persist to disk (PVC)
   │
   ▼
9. Response
   │
   ├─► Return BookingResponse schema
   ├─► HTTP 201 Created
   │
   ▼
10. Client receives booking confirmation
```

---

## Data Flow Diagram

```
┌──────────────┐
│   Customer   │
└──────┬───────┘
       │
       │ 1. Browse vendors by city
       ▼
┌──────────────────────────────┐
│  GET /api/vendors/by-city/   │
│  Returns: List of vendors    │
└──────┬───────────────────────┘
       │
       │ 2. View vendor services
       ▼
┌──────────────────────────────┐
│  GET /api/vendors/{id}/      │
│       services               │
│  Returns: Available services │
└──────┬───────────────────────┘
       │
       │ 3. Check available slots
       ▼
┌──────────────────────────────┐
│  GET /api/bookings/          │
│      available-slots/        │
│  Returns: Time slots         │
└──────┬───────────────────────┘
       │
       │ 4. Create booking
       ▼
┌──────────────────────────────┐
│  POST /api/bookings/         │
│  Creates: New booking        │
└──────┬───────────────────────┘
       │
       │ 5. Vendor confirms
       ▼
┌──────────────────────────────┐
│  PATCH /api/bookings/{id}/   │
│        status                │
│  Updates: Status to confirmed│
└──────┬───────────────────────┘
       │
       │ 6. Service completed
       ▼
┌──────────────────────────────┐
│  PATCH /api/bookings/{id}/   │
│        status                │
│  Updates: Status to completed│
└──────────────────────────────┘
```

---

## Deployment Architecture

### Local Development (Docker Compose)

```
┌─────────────────────────────────────────┐
│         Docker Host                      │
│                                          │
│  ┌────────────────────────────────┐     │
│  │  wash-network (Bridge)         │     │
│  │                                 │     │
│  │  ┌──────────────────────────┐  │     │
│  │  │  wash-booking-app        │  │     │
│  │  │  Port: 8000:8000         │  │     │
│  │  │  Depends on: db          │  │     │
│  │  └──────────┬───────────────┘  │     │
│  │             │                   │     │
│  │  ┌──────────▼───────────────┐  │     │
│  │  │  wash-booking-db         │  │     │
│  │  │  Port: 5432:5432         │  │     │
│  │  │  Volume: postgres_data   │  │     │
│  │  └──────────────────────────┘  │     │
│  └─────────────────────────────────┘     │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │  Volumes                         │    │
│  │  - postgres_data (persistent)    │    │
│  └─────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

### Production (Kubernetes)

```
┌──────────────────────────────────────────────────────────┐
│                  Kubernetes Cluster                       │
│                                                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │  Namespace: default                                │  │
│  │                                                     │  │
│  │  ┌──────────────────────────────────────────────┐ │  │
│  │  │  Service: wash-booking-service               │ │  │
│  │  │  Type: LoadBalancer                          │ │  │
│  │  │  External IP: <CLOUD_PROVIDER_IP>            │ │  │
│  │  └────────────┬─────────────────────────────────┘ │  │
│  │               │                                    │  │
│  │  ┌────────────▼─────────────────────────────────┐ │  │
│  │  │  Deployment: wash-booking-deployment         │ │  │
│  │  │  Replicas: 3                                 │ │  │
│  │  │  Strategy: RollingUpdate                     │ │  │
│  │  │  ┌──────┐  ┌──────┐  ┌──────┐               │ │  │
│  │  │  │ Pod1 │  │ Pod2 │  │ Pod3 │               │ │  │
│  │  │  └──────┘  └──────┘  └──────┘               │ │  │
│  │  └──────────────────────────────────────────────┘ │  │
│  │                                                     │  │
│  │  ┌──────────────────────────────────────────────┐ │  │
│  │  │  Service: postgres-service                   │ │  │
│  │  │  Type: ClusterIP (Internal)                  │ │  │
│  │  └────────────┬─────────────────────────────────┘ │  │
│  │               │                                    │  │
│  │  ┌────────────▼─────────────────────────────────┐ │  │
│  │  │  Deployment: postgres-deployment             │ │  │
│  │  │  Replicas: 1                                 │ │  │
│  │  │  ┌──────────────┐                            │ │  │
│  │  │  │ PostgreSQL   │                            │ │  │
│  │  │  │ Pod          │                            │ │  │
│  │  │  └──────┬───────┘                            │ │  │
│  │  └─────────┼──────────────────────────────────┘ │  │
│  │            │                                      │  │
│  │  ┌─────────▼──────────────────────────────────┐ │  │
│  │  │  PersistentVolumeClaim: postgres-pvc       │ │  │
│  │  │  Size: 5Gi                                 │ │  │
│  │  │  AccessMode: ReadWriteOnce                 │ │  │
│  │  └────────────┬───────────────────────────────┘ │  │
│  └───────────────┼─────────────────────────────────┘  │
│                  │                                     │
│  ┌───────────────▼─────────────────────────────────┐  │
│  │  PersistentVolume (Cloud Provider Storage)      │  │
│  │  - AWS EBS / GCP Persistent Disk / Azure Disk   │  │
│  └─────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────┘
```

---

## Technology Stack Layers

```
┌─────────────────────────────────────────────────────┐
│  Presentation Layer                                  │
│  - REST API (FastAPI)                               │
│  - Swagger UI / ReDoc                               │
│  - JSON responses                                   │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Application Layer                                   │
│  - Python 3.11                                      │
│  - FastAPI framework                                │
│  - Uvicorn ASGI server                              │
│  - Pydantic validation                              │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Business Logic Layer                                │
│  - CRUD operations                                  │
│  - Slot availability logic                          │
│  - Validation rules                                 │
│  - Indian context handling                          │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Data Access Layer                                   │
│  - SQLAlchemy ORM                                   │
│  - Database models                                  │
│  - Relationships                                    │
│  - Connection pooling                               │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Database Layer                                      │
│  - PostgreSQL 15                                    │
│  - ACID compliance                                  │
│  - Indexes and constraints                          │
│  - Persistent storage                               │
└─────────────────────────────────────────────────────┘
```

---

## Security Architecture

```
┌─────────────────────────────────────────────────────┐
│  Network Security                                    │
│  - CORS configuration                               │
│  - LoadBalancer with firewall rules                │
│  - Internal ClusterIP for database                  │
│  - Network policies (optional)                      │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Application Security                                │
│  - Input validation (Pydantic)                      │
│  - SQL injection prevention (ORM)                   │
│  - Non-root container user                          │
│  - No hardcoded secrets                             │
└────────────────────┬────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────┐
│  Data Security                                       │
│  - Encrypted connections (SSL ready)                │
│  - Persistent volume encryption (cloud provider)    │
│  - Backup and recovery                              │
│  - Access control (K8s RBAC ready)                  │
└─────────────────────────────────────────────────────┘
```

---

## Scalability Architecture

```
Horizontal Scaling (Application Tier)
┌──────────────────────────────────────────┐
│  Auto-scaling based on:                  │
│  - CPU utilization                       │
│  - Memory usage                          │
│  - Request rate                          │
│                                          │
│  Min replicas: 3                         │
│  Max replicas: 10 (configurable)         │
└──────────────────────────────────────────┘

Vertical Scaling (Database Tier)
┌──────────────────────────────────────────┐
│  Resource adjustments:                   │
│  - CPU: 250m → 2000m                     │
│  - Memory: 256Mi → 4Gi                   │
│  - Storage: 5Gi → 100Gi                  │
└──────────────────────────────────────────┘

Read Replicas (Future Enhancement)
┌──────────────────────────────────────────┐
│  Master-Slave replication:               │
│  - 1 Master (write)                      │
│  - N Slaves (read)                       │
│  - Load balancing for reads              │
└──────────────────────────────────────────┘
```

This architecture provides a solid foundation for a production-grade application with room for future enhancements!
