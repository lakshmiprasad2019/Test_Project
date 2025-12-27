# Quick Reference Guide

## 🚀 Quick Start Commands

### Local Development (Docker Compose)
```bash
# Start everything
docker-compose up --build

# Start in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop everything
docker-compose down

# Clean everything (including volumes)
docker-compose down -v
```

### Kubernetes Deployment
```bash
# Deploy all resources
kubectl apply -f k8s/

# Check status
kubectl get all

# View logs
kubectl logs -l app=wash-booking,component=api -f

# Port forward for local access
kubectl port-forward service/wash-booking-service 8000:8000

# Scale application
kubectl scale deployment wash-booking-deployment --replicas=5

# Delete all resources
kubectl delete -f k8s/
```

---

## 📡 API Endpoints Quick Reference

### Base URL
- Local: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

### Customer
```bash
# Create customer
POST /api/bookings/customers/
{
  "name": "string",
  "email": "user@example.com",
  "phone": "9876543210",
  "city": "string"
}
```

### Vendor
```bash
# Register vendor
POST /api/vendors/
{
  "name": "string",
  "email": "vendor@example.com",
  "phone": "9123456789",
  "city": "string",
  "service_area": "string",
  "address": "string"
}

# Get vendors by city
GET /api/vendors/by-city/{city}

# Add service
POST /api/vendors/{vendor_id}/services
{
  "name": "Deep Clean",
  "price": 799.00,
  "duration_minutes": 90,
  "vehicle_type": "car"
}
```

### Booking
```bash
# Check available slots
GET /api/bookings/available-slots/{vendor_id}?date=2025-12-28&service_id=1

# Create booking
POST /api/bookings/
{
  "customer_id": 1,
  "vendor_id": 1,
  "service_id": 1,
  "city": "Mumbai",
  "booking_date": "2025-12-28T10:00:00",
  "vehicle_type": "car",
  "vehicle_number": "MH01AB1234",
  "pincode": "400001"
}

# Update status
PATCH /api/bookings/{id}/status?status=confirmed
```

---

## 🗄️ Database Quick Reference

### Connection Strings
```bash
# Docker Compose
postgresql://washuser:washpass@localhost:5432/washbooking

# Kubernetes (from within cluster)
postgresql://washuser:washpass@postgres-service:5432/washbooking
```

### Access Database
```bash
# Docker Compose
docker exec -it wash-booking-db psql -U washuser -d washbooking

# Kubernetes
kubectl exec -it deployment/postgres-deployment -- psql -U washuser -d washbooking
```

### Common SQL Queries
```sql
-- View all tables
\dt

-- View customers
SELECT * FROM customers;

-- View vendors by city
SELECT * FROM vendors WHERE city = 'Mumbai';

-- View bookings with details
SELECT b.id, c.name as customer, v.name as vendor, s.name as service, 
       b.booking_date, b.status
FROM bookings b
JOIN customers c ON b.customer_id = c.id
JOIN vendors v ON b.vendor_id = v.id
JOIN services s ON b.service_id = s.id;

-- Count bookings by status
SELECT status, COUNT(*) FROM bookings GROUP BY status;
```

---

## 🔧 Troubleshooting

### Docker Issues
```bash
# View container logs
docker-compose logs app
docker-compose logs db

# Restart specific service
docker-compose restart app

# Rebuild without cache
docker-compose build --no-cache

# Check container status
docker-compose ps
```

### Kubernetes Issues
```bash
# Describe pod (shows events and errors)
kubectl describe pod <pod-name>

# Get pod logs
kubectl logs <pod-name>

# Get previous pod logs (if crashed)
kubectl logs <pod-name> --previous

# Execute command in pod
kubectl exec -it <pod-name> -- /bin/sh

# Check resource usage
kubectl top pods
kubectl top nodes

# View events
kubectl get events --sort-by='.lastTimestamp'
```

### Database Issues
```bash
# Check database connection
docker exec wash-booking-db pg_isready -U washuser

# View database size
docker exec wash-booking-db psql -U washuser -d washbooking -c "SELECT pg_size_pretty(pg_database_size('washbooking'));"

# Restart database
docker-compose restart db
# or
kubectl rollout restart deployment/postgres-deployment
```

---

## 📊 Validation Rules

### Phone Number
- **Format**: 10 digits starting with 6-9
- **Regex**: `^[6-9]\d{9}$`
- **Valid**: `9876543210`, `8123456789`
- **Invalid**: `1234567890`, `98765432`

### Pincode
- **Format**: 6 digits
- **Regex**: `^\d{6}$`
- **Valid**: `400001`, `560001`
- **Invalid**: `12345`, `4000011`

### Booking Date
- **Rule**: Must be in current year and month
- **Rule**: Cannot be in the past
- **Valid**: `2025-12-28T10:00:00` (if current month is Dec 2025)
- **Invalid**: `2024-12-28T10:00:00`, `2025-11-28T10:00:00`

### Vehicle Type
- **Values**: `bike`, `car`
- **Case**: Lowercase only

### Booking Status
- **Values**: `pending`, `confirmed`, `completed`, `cancelled`
- **Default**: `pending`

---

## 🌆 Indian Cities Reference

Popular cities for testing:
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
- Surat
- Kanpur
- Nagpur
- Indore
- Thane

---

## 📝 Environment Variables

### Required Variables
```bash
DATABASE_URL=postgresql://washuser:washpass@db:5432/washbooking
POSTGRES_USER=washuser
POSTGRES_PASSWORD=washpass
POSTGRES_DB=washbooking
```

### Optional Variables (Production)
```bash
# Security
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=your-domain.com

# Database
DB_POOL_SIZE=10
DB_MAX_OVERFLOW=20

# Application
LOG_LEVEL=INFO
DEBUG=False
```

---

## 🔐 Security Checklist

### Before Production
- [ ] Change default database password
- [ ] Use Kubernetes Secrets for sensitive data
- [ ] Enable SSL/TLS
- [ ] Set up authentication (JWT)
- [ ] Configure CORS properly
- [ ] Enable rate limiting
- [ ] Set up monitoring and alerting
- [ ] Regular security updates
- [ ] Database backups configured
- [ ] Network policies in place

---

## 📈 Performance Tips

### Application
- Use connection pooling (already configured)
- Implement caching (Redis recommended)
- Enable compression
- Use async operations where possible

### Database
- Create appropriate indexes (see DATABASE_SCHEMA.md)
- Regular VACUUM and ANALYZE
- Monitor slow queries
- Consider read replicas for scaling

### Kubernetes
- Set appropriate resource limits
- Use horizontal pod autoscaling
- Implement pod disruption budgets
- Use node affinity for database pods

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README.md` | Project overview |
| `PROJECT_SUMMARY.md` | Complete deliverables summary |
| `DEPLOYMENT.md` | Deployment instructions |
| `API_TESTING.md` | API testing examples |
| `DATABASE_SCHEMA.md` | Database documentation |
| `ARCHITECTURE.md` | System architecture |
| `QUICK_REFERENCE.md` | This file |

---

## 🆘 Common Error Solutions

### "Database connection failed"
```bash
# Check if database is running
docker-compose ps db
# or
kubectl get pods -l component=database

# Verify connection string
echo $DATABASE_URL
```

### "Port already in use"
```bash
# Find process using port 8000
netstat -ano | findstr :8000

# Kill the process (Windows)
taskkill /PID <PID> /F

# Or change port in docker-compose.yaml
ports:
  - "8001:8000"  # Use 8001 instead
```

### "Booking date validation error"
- Ensure date is in current year and month
- Use ISO format: `YYYY-MM-DDTHH:MM:SS`
- Check that date is not in the past

### "Phone number validation error"
- Must be 10 digits
- Must start with 6, 7, 8, or 9
- Example: `9876543210`

---

## 🎯 Testing Workflow

### 1. Setup
```bash
docker-compose up -d
```

### 2. Create Test Data
```bash
# Create customer
curl -X POST "http://localhost:8000/api/bookings/customers/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test User","email":"test@example.com","phone":"9876543210","city":"Mumbai"}'

# Register vendor
curl -X POST "http://localhost:8000/api/vendors/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Vendor","email":"vendor@example.com","phone":"9123456789","city":"Mumbai","service_area":"400001"}'

# Add service
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{"name":"Deep Clean","price":799.00,"duration_minutes":90,"vehicle_type":"car"}'
```

### 3. Test Booking Flow
```bash
# Check slots
curl "http://localhost:8000/api/bookings/available-slots/1?date=2025-12-28&service_id=1"

# Create booking
curl -X POST "http://localhost:8000/api/bookings/" \
  -H "Content-Type: application/json" \
  -d '{"customer_id":1,"vendor_id":1,"service_id":1,"city":"Mumbai","booking_date":"2025-12-28T10:00:00","vehicle_type":"car"}'

# Update status
curl -X PATCH "http://localhost:8000/api/bookings/1/status?status=confirmed"
```

### 4. Verify
```bash
# Get booking details
curl "http://localhost:8000/api/bookings/1"
```

---

## 💡 Pro Tips

1. **Use the interactive docs**: Visit `/docs` for a user-friendly API interface
2. **Check logs first**: Most issues are visible in logs
3. **Use health checks**: `/health` endpoint for quick status check
4. **Test locally first**: Use Docker Compose before Kubernetes
5. **Keep backups**: Regular database backups are crucial
6. **Monitor resources**: Use `kubectl top` to watch resource usage
7. **Version your images**: Tag Docker images properly (not just `latest`)
8. **Use secrets**: Never commit passwords to git

---

## 🔄 Update Workflow

### Application Code Update
```bash
# Local (Docker Compose)
docker-compose up --build

# Kubernetes
docker build -t your-registry/wash-booking:v1.1.0 .
docker push your-registry/wash-booking:v1.1.0
kubectl set image deployment/wash-booking-deployment \
  wash-booking-api=your-registry/wash-booking:v1.1.0
```

### Database Schema Update
```bash
# Use Alembic for migrations (recommended for production)
# For now, tables auto-create on startup
# Manual migration:
kubectl exec -it deployment/postgres-deployment -- psql -U washuser -d washbooking -f /path/to/migration.sql
```

---

This quick reference should help you navigate the project efficiently! 🚀
