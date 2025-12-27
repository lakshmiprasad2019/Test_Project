#!/bin/bash

# Quick fix for email-validator missing dependency

echo "🔧 Installing email-validator in running container..."
docker exec wash-booking-app pip install email-validator==2.1.0

echo "🔄 Restarting application..."
docker-compose restart app

echo "⏳ Waiting for app to start..."
sleep 5

echo "📋 Checking logs..."
docker-compose logs --tail=20 app

echo ""
echo "✅ Done! Test with: curl http://localhost:8000/health"
