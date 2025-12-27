# Amazon Linux Deployment Guide

## Issue Encountered

**Error**: `compose build requires buildx 0.17 or later`

This error occurs because Docker Compose v5.0.1 requires a newer version of buildx for the build process.

---

## ✅ Solution Options

### **Option 1: Use Deployment Script (Recommended)**

I've created a deployment script that builds the image first, then starts the services.

#### Steps:

1. **Make the script executable**:
   ```bash
   chmod +x deploy.sh
   ```

2. **Run the deployment script**:
   ```bash
   ./deploy.sh
   ```

This script will:
- Build the Docker image
- Stop any existing containers
- Start all services
- Show status and logs

---

### **Option 2: Manual Build and Deploy**

If you prefer manual control:

#### Step 1: Build the Docker image
```bash
docker build -t wash-booking-app:latest .
```

#### Step 2: Start the services
```bash
docker-compose up -d
```

#### Step 3: Check status
```bash
docker-compose ps
```

#### Step 4: View logs
```bash
docker-compose logs -f
```

---

### **Option 3: Use Production Compose File**

Use the alternative compose file that references a pre-built image:

```bash
# Build the image first
docker build -t wash-booking-app:latest .

# Use the production compose file
docker-compose -f docker-compose.prod.yaml up -d
```

---

### **Option 4: Update Docker Buildx (Advanced)**

If you want to fix the buildx issue:

```bash
# Install/update buildx plugin
docker buildx install

# Verify version
docker buildx version
```

---

## 🚀 Quick Start Commands

### Deploy the Application
```bash
# Option A: Using deployment script
chmod +x deploy.sh
./deploy.sh

# Option B: Manual deployment
docker build -t wash-booking-app:latest .
docker-compose up -d
```

### Check Status
```bash
# View running containers
docker-compose ps

# View logs (all services)
docker-compose logs -f

# View app logs only
docker-compose logs -f app

# View database logs only
docker-compose logs -f db
```

### Access the Application
```bash
# Get the server's public IP
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Access the API
# Replace <PUBLIC_IP> with your server's IP
curl http://<PUBLIC_IP>:8000
curl http://<PUBLIC_IP>:8000/docs
```

### Stop the Application
```bash
docker-compose down
```

### Restart the Application
```bash
docker-compose restart
```

---

## 🔧 Troubleshooting

### Issue: Container fails to start

**Check logs**:
```bash
docker-compose logs app
```

**Common causes**:
1. Database not ready - Wait a few seconds and check again
2. Port 8000 already in use - Change port in docker-compose.yaml
3. Permission issues - Run with sudo if needed

### Issue: Cannot access from browser

**Check security group**:
- Ensure port 8000 is open in AWS Security Group
- Add inbound rule: TCP port 8000 from 0.0.0.0/0

**Check firewall**:
```bash
# Check if firewall is running
sudo systemctl status firewalld

# If running, allow port 8000
sudo firewall-cmd --permanent --add-port=8000/tcp
sudo firewall-cmd --reload
```

### Issue: Database connection error

**Check database health**:
```bash
docker exec wash-booking-db pg_isready -U washuser -d washbooking
```

**Restart database**:
```bash
docker-compose restart db
```

---

## 📊 Testing the API

### Create a Customer
```bash
curl -X POST "http://localhost:8000/api/bookings/customers/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Rajesh Kumar",
    "email": "rajesh@example.com",
    "phone": "9876543210",
    "city": "Mumbai"
  }'
```

### Register a Vendor
```bash
curl -X POST "http://localhost:8000/api/vendors/" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Premium Car Wash",
    "email": "premium@carwash.com",
    "phone": "9123456789",
    "city": "Mumbai",
    "service_area": "400001, Andheri, Bandra",
    "address": "123 Main Street, Mumbai"
  }'
```

### Add a Service
```bash
curl -X POST "http://localhost:8000/api/vendors/1/services" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Deep Clean",
    "description": "Complete interior and exterior cleaning",
    "price": 799.00,
    "duration_minutes": 90,
    "vehicle_type": "car"
  }'
```

### Create a Booking
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
    "vehicle_number": "MH01AB1234",
    "service_address": "456 Park Road, Mumbai",
    "pincode": "400001"
  }'
```

---

## 🔒 AWS Security Group Configuration

To access the application from outside the server:

1. Go to AWS Console → EC2 → Security Groups
2. Select your instance's security group
3. Add inbound rule:
   - **Type**: Custom TCP
   - **Port**: 8000
   - **Source**: 0.0.0.0/0 (or your IP for security)
4. Save rules

---

## 📈 Monitoring

### View Resource Usage
```bash
# Container stats
docker stats

# Disk usage
docker system df

# View running processes
docker-compose top
```

### Database Access
```bash
# Connect to PostgreSQL
docker exec -it wash-booking-db psql -U washuser -d washbooking

# Run SQL queries
docker exec -it wash-booking-db psql -U washuser -d washbooking -c "SELECT * FROM customers;"
```

---

## 🔄 Update Deployment

When you make code changes:

```bash
# Rebuild and restart
docker build -t wash-booking-app:latest .
docker-compose up -d --force-recreate app

# Or use the deployment script
./deploy.sh
```

---

## 🛑 Cleanup

### Stop and remove containers
```bash
docker-compose down
```

### Remove containers and volumes (⚠️ deletes database data)
```bash
docker-compose down -v
```

### Remove images
```bash
docker rmi wash-booking-app:latest
docker rmi postgres:15-alpine
```

---

## ✅ Deployment Checklist

- [x] Docker installed (v25.0.13)
- [x] Docker Compose installed (v5.0.1)
- [x] Project files uploaded to server
- [x] Build Docker image: `docker build -t wash-booking-app:latest .`
- [x] Start services: `docker-compose up -d`
- [ ] Configure AWS Security Group (port 8000)
- [ ] Test API endpoints
- [ ] Set up monitoring
- [ ] Configure backups

---

## 📞 Support

For issues or questions, refer to:
- **API Testing**: `API_TESTING.md`
- **Quick Reference**: `QUICK_REFERENCE.md`
- **Architecture**: `ARCHITECTURE.md`

---

**Your application is ready to deploy on Amazon Linux!** 🚀
