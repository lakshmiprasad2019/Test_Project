# Database Schema Documentation

## Entity Relationship Diagram (ERD)

```
┌─────────────────────┐
│     CUSTOMERS       │
├─────────────────────┤
│ id (PK)            │
│ name               │
│ email (UNIQUE)     │
│ phone (UNIQUE)     │
│ city               │
│ created_at         │
│ updated_at         │
└─────────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────────┐       ┌─────────────────────┐
│     BOOKINGS        │ N:1   │      VENDORS        │
├─────────────────────┤◄──────┤─────────────────────┤
│ id (PK)            │       │ id (PK)            │
│ customer_id (FK)   │       │ name               │
│ vendor_id (FK)     │       │ email (UNIQUE)     │
│ service_id (FK)    │       │ phone (UNIQUE)     │
│ city               │       │ city               │
│ booking_date       │       │ service_area       │
│ status             │       │ address            │
│ vehicle_number     │       │ is_active          │
│ vehicle_type       │       │ created_at         │
│ service_address    │       │ updated_at         │
│ pincode            │       └─────────────────────┘
│ total_price        │                │
│ created_at         │                │ 1:N
│ updated_at         │                ▼
└─────────────────────┘       ┌─────────────────────┐
         │                    │      SERVICES       │
         │ N:1                ├─────────────────────┤
         └───────────────────►│ id (PK)            │
                              │ vendor_id (FK)     │
                              │ name               │
                              │ description        │
                              │ price              │
                              │ duration_minutes   │
                              │ vehicle_type       │
                              │ is_active          │
                              │ created_at         │
                              │ updated_at         │
                              └─────────────────────┘
```

## Table Definitions

### CUSTOMERS
Stores customer/user information.

| Column      | Type         | Constraints           | Description                    |
|-------------|--------------|----------------------|--------------------------------|
| id          | INTEGER      | PRIMARY KEY          | Auto-incrementing ID           |
| name        | VARCHAR(100) | NOT NULL             | Customer name                  |
| email       | VARCHAR(100) | UNIQUE, NOT NULL     | Email address                  |
| phone       | VARCHAR(15)  | UNIQUE, NOT NULL     | Indian phone (10 digits)       |
| city        | VARCHAR(100) | NOT NULL, INDEXED    | Indian city                    |
| created_at  | TIMESTAMP    | DEFAULT NOW()        | Record creation time           |
| updated_at  | TIMESTAMP    | DEFAULT NOW()        | Last update time               |

**Indexes**: `email`, `phone`, `city`

---

### VENDORS
Stores service provider information.

| Column        | Type         | Constraints           | Description                    |
|---------------|--------------|----------------------|--------------------------------|
| id            | INTEGER      | PRIMARY KEY          | Auto-incrementing ID           |
| name          | VARCHAR(100) | NOT NULL             | Vendor business name           |
| email         | VARCHAR(100) | UNIQUE, NOT NULL     | Email address                  |
| phone         | VARCHAR(15)  | UNIQUE, NOT NULL     | Indian phone (10 digits)       |
| city          | VARCHAR(100) | NOT NULL, INDEXED    | Operating city                 |
| service_area  | VARCHAR(200) | NOT NULL             | Pincode/Neighborhood coverage  |
| address       | TEXT         | NULLABLE             | Physical address               |
| is_active     | BOOLEAN      | DEFAULT TRUE         | Vendor active status           |
| created_at    | TIMESTAMP    | DEFAULT NOW()        | Record creation time           |
| updated_at    | TIMESTAMP    | DEFAULT NOW()        | Last update time               |

**Indexes**: `email`, `phone`, `city`

---

### SERVICES
Stores services offered by vendors.

| Column            | Type          | Constraints           | Description                    |
|-------------------|---------------|----------------------|--------------------------------|
| id                | INTEGER       | PRIMARY KEY          | Auto-incrementing ID           |
| vendor_id         | INTEGER       | FOREIGN KEY, NOT NULL| References vendors(id)         |
| name              | VARCHAR(100)  | NOT NULL             | Service name                   |
| description       | TEXT          | NULLABLE             | Service description            |
| price             | NUMERIC(10,2) | NOT NULL             | Price in INR                   |
| duration_minutes  | INTEGER       | NOT NULL             | Service duration               |
| vehicle_type      | VARCHAR(20)   | NOT NULL             | 'bike' or 'car'                |
| is_active         | BOOLEAN       | DEFAULT TRUE         | Service active status          |
| created_at        | TIMESTAMP     | DEFAULT NOW()        | Record creation time           |
| updated_at        | TIMESTAMP     | DEFAULT NOW()        | Last update time               |

**Foreign Keys**: 
- `vendor_id` → `vendors(id)` ON DELETE CASCADE

**Constraints**:
- `vehicle_type` CHECK IN ('bike', 'car')

---

### BOOKINGS
Stores booking information.

| Column           | Type          | Constraints           | Description                    |
|------------------|---------------|----------------------|--------------------------------|
| id               | INTEGER       | PRIMARY KEY          | Auto-incrementing ID           |
| customer_id      | INTEGER       | FOREIGN KEY, NOT NULL| References customers(id)       |
| vendor_id        | INTEGER       | FOREIGN KEY, NOT NULL| References vendors(id)         |
| service_id       | INTEGER       | FOREIGN KEY, NOT NULL| References services(id)        |
| city             | VARCHAR(100)  | NOT NULL, INDEXED    | Service city                   |
| booking_date     | TIMESTAMP     | NOT NULL, INDEXED    | Service date & time            |
| status           | VARCHAR(20)   | DEFAULT 'pending'    | Booking status                 |
| vehicle_number   | VARCHAR(20)   | NULLABLE             | Vehicle registration           |
| vehicle_type     | VARCHAR(20)   | NOT NULL             | 'bike' or 'car'                |
| service_address  | TEXT          | NULLABLE             | Service location               |
| pincode          | VARCHAR(10)   | NULLABLE             | 6-digit Indian pincode         |
| total_price      | NUMERIC(10,2) | NOT NULL             | Total booking price            |
| created_at       | TIMESTAMP     | DEFAULT NOW()        | Record creation time           |
| updated_at       | TIMESTAMP     | DEFAULT NOW()        | Last update time               |

**Foreign Keys**:
- `customer_id` → `customers(id)` ON DELETE CASCADE
- `vendor_id` → `vendors(id)` ON DELETE CASCADE
- `service_id` → `services(id)` ON DELETE CASCADE

**Indexes**: `city`, `booking_date`, `customer_id`, `vendor_id`

**Constraints**:
- `status` CHECK IN ('pending', 'confirmed', 'completed', 'cancelled')
- `vehicle_type` CHECK IN ('bike', 'car')

---

## Relationships

### One-to-Many Relationships

1. **Customer → Bookings** (1:N)
   - One customer can have multiple bookings
   - Each booking belongs to one customer

2. **Vendor → Services** (1:N)
   - One vendor can offer multiple services
   - Each service belongs to one vendor

3. **Vendor → Bookings** (1:N)
   - One vendor can have multiple bookings
   - Each booking is with one vendor

4. **Service → Bookings** (1:N)
   - One service can be booked multiple times
   - Each booking is for one service

---

## Sample Data

### Customers
```sql
INSERT INTO customers (name, email, phone, city) VALUES
('Rajesh Kumar', 'rajesh@example.com', '9876543210', 'Mumbai'),
('Priya Sharma', 'priya@example.com', '9123456789', 'Bangalore'),
('Amit Patel', 'amit@example.com', '9988776655', 'Delhi');
```

### Vendors
```sql
INSERT INTO vendors (name, email, phone, city, service_area, address) VALUES
('Premium Car Wash', 'premium@carwash.com', '9111222333', 'Mumbai', '400001, Andheri, Bandra', '123 Main St, Mumbai'),
('SparkleClean Auto', 'info@sparkle.com', '9444555666', 'Bangalore', '560001, Koramangala, HSR', '45 MG Road, Bangalore');
```

### Services
```sql
INSERT INTO services (vendor_id, name, description, price, duration_minutes, vehicle_type) VALUES
(1, 'Deep Clean', 'Complete interior and exterior cleaning', 799.00, 90, 'car'),
(1, 'Quick Wash', 'Fast exterior wash', 149.00, 30, 'bike'),
(2, 'Interior Detailing', 'Complete interior cleaning', 599.00, 60, 'car');
```

### Bookings
```sql
INSERT INTO bookings (customer_id, vendor_id, service_id, city, booking_date, vehicle_type, vehicle_number, total_price) VALUES
(1, 1, 1, 'Mumbai', '2025-12-28 10:00:00', 'car', 'MH01AB1234', 799.00),
(2, 2, 3, 'Bangalore', '2025-12-28 14:00:00', 'car', 'KA01CD5678', 599.00);
```

---

## Indexes Strategy

### Primary Indexes
- All `id` columns are primary keys with automatic indexes

### Secondary Indexes
- **customers**: `email`, `phone`, `city`
- **vendors**: `email`, `phone`, `city`
- **bookings**: `city`, `booking_date`, `customer_id`, `vendor_id`

### Composite Indexes (Recommended for Production)
```sql
CREATE INDEX idx_bookings_vendor_date ON bookings(vendor_id, booking_date);
CREATE INDEX idx_bookings_customer_status ON bookings(customer_id, status);
CREATE INDEX idx_services_vendor_active ON services(vendor_id, is_active);
```

---

## Data Validation Rules

### Phone Numbers
- Format: 10 digits starting with 6-9
- Regex: `^[6-9]\d{9}$`
- Example: `9876543210`

### Pincodes
- Format: 6 digits
- Regex: `^\d{6}$`
- Example: `400001`

### Booking Dates
- Must be in current year and month
- Cannot be in the past
- Validated at application level

### Vehicle Types
- Allowed values: `bike`, `car`
- Case-sensitive

### Booking Status
- Allowed values: `pending`, `confirmed`, `completed`, `cancelled`
- Default: `pending`

---

## Performance Considerations

### Query Optimization
1. Use indexes on frequently queried columns
2. Implement connection pooling
3. Use prepared statements
4. Limit result sets with pagination

### Scaling Strategies
1. **Read Replicas**: For read-heavy workloads
2. **Partitioning**: Partition bookings by date
3. **Caching**: Cache vendor and service data
4. **Archiving**: Archive old bookings

### Backup Strategy
1. Daily full backups
2. Point-in-time recovery enabled
3. Backup retention: 30 days
4. Test restore procedures monthly
