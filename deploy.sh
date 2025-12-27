#!/bin/bash

# Deployment script for Amazon Linux server
# This script builds the Docker image and starts the services

set -e  # Exit on error

echo "=========================================="
echo "Wash Booking Application Deployment"
echo "=========================================="
echo ""

# Step 1: Build the Docker image
echo "Step 1: Building Docker image..."
docker build -t wash-booking-app:latest .
echo "✅ Docker image built successfully"
echo ""

# Step 2: Stop existing containers (if any)
echo "Step 2: Stopping existing containers..."
docker-compose down 2>/dev/null || true
echo "✅ Existing containers stopped"
echo ""

# Step 3: Start the services
echo "Step 3: Starting services..."
docker-compose up -d
echo "✅ Services started successfully"
echo ""

# Step 4: Wait for services to be healthy
echo "Step 4: Waiting for services to be healthy..."
sleep 5

# Step 5: Check service status
echo "Step 5: Checking service status..."
docker-compose ps
echo ""

# Step 6: Show logs
echo "Step 6: Showing recent logs..."
docker-compose logs --tail=20
echo ""

echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "Access the application at:"
echo "  - API: http://localhost:8000"
echo "  - Docs: http://localhost:8000/docs"
echo ""
echo "Useful commands:"
echo "  - View logs: docker-compose logs -f"
echo "  - Stop services: docker-compose down"
echo "  - Restart: docker-compose restart"
echo ""
