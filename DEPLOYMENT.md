# Deployment Guide

## Quick Start - Local Development

### Prerequisites
- Docker and Docker Compose installed
- Python 3.11+ (for local development without Docker)

### Option 1: Using Docker Compose (Recommended)

1. **Start the application**:
   ```bash
   docker-compose up --build
   ```

2. **Access the application**:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Interactive API: http://localhost:8000/redoc

3. **Stop the application**:
   ```bash
   docker-compose down
   ```

4. **Stop and remove volumes** (clean slate):
   ```bash
   docker-compose down -v
   ```

### Option 2: Local Python Development

1. **Create virtual environment**:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Start PostgreSQL** (using Docker):
   ```bash
   docker run -d --name wash-db -e POSTGRES_USER=washuser -e POSTGRES_PASSWORD=washpass -e POSTGRES_DB=washbooking -p 5432:5432 postgres:15-alpine
   ```

4. **Update .env file**:
   ```
   DATABASE_URL=postgresql://washuser:washpass@localhost:5432/washbooking
   ```

5. **Run the application**:
   ```bash
   python -m app.main
   ```

## Kubernetes Deployment

### Prerequisites
- Kubernetes cluster (minikube, kind, GKE, EKS, AKS, etc.)
- kubectl configured to access your cluster
- Docker image built and pushed to a registry

### Step 1: Build and Push Docker Image

```bash
# Build the image
docker build -t your-registry/wash-booking:v1.0.0 .

# Push to registry
docker push your-registry/wash-booking:v1.0.0
```

### Step 2: Update Kubernetes Manifests

Edit `k8s/deployment.yaml` and update the image:
```yaml
image: your-registry/wash-booking:v1.0.0
```

### Step 3: Deploy to Kubernetes

```bash
# Apply all manifests
kubectl apply -f k8s/pvc.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Or apply all at once
kubectl apply -f k8s/
```

### Step 4: Verify Deployment

```bash
# Check pods
kubectl get pods

# Check services
kubectl get services

# Check logs
kubectl logs -l app=wash-booking,component=api

# Check database logs
kubectl logs -l app=wash-booking,component=database
```

### Step 5: Access the Application

**For LoadBalancer service**:
```bash
# Get external IP
kubectl get service wash-booking-service

# Access at http://<EXTERNAL-IP>:8000
```

**For local testing (port-forward)**:
```bash
kubectl port-forward service/wash-booking-service 8000:8000

# Access at http://localhost:8000
```

## Testing the API

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
    "price": 599.00,
    "duration_minutes": 60,
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

### Check Available Slots
```bash
curl "http://localhost:8000/api/bookings/available-slots/1?date=2025-12-28&service_id=1"
```

## Monitoring and Troubleshooting

### Docker Compose Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f app
docker-compose logs -f db
```

### Kubernetes Logs
```bash
# Application logs
kubectl logs -l app=wash-booking,component=api -f

# Database logs
kubectl logs -l app=wash-booking,component=database -f

# Describe pod for issues
kubectl describe pod <pod-name>
```

### Database Access

**Docker Compose**:
```bash
docker exec -it wash-booking-db psql -U washuser -d washbooking
```

**Kubernetes**:
```bash
kubectl exec -it deployment/postgres-deployment -- psql -U washuser -d washbooking
```

## Production Considerations

1. **Security**:
   - Use Kubernetes Secrets for sensitive data
   - Enable SSL/TLS with Ingress
   - Implement authentication and authorization
   - Use network policies

2. **Scalability**:
   - Adjust replica count based on load
   - Implement horizontal pod autoscaling
   - Use connection pooling for database

3. **Monitoring**:
   - Set up Prometheus and Grafana
   - Configure alerting
   - Implement distributed tracing

4. **Backup**:
   - Regular database backups
   - Volume snapshots
   - Disaster recovery plan

5. **CI/CD**:
   - Automated testing
   - Container scanning
   - GitOps deployment
