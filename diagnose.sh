#!/bin/bash

# Quick diagnostic script for connection issues

echo "=========================================="
echo "🔍 Wash Booking App - Diagnostics"
echo "=========================================="
echo ""

echo "1️⃣ Container Status:"
echo "-------------------"
docker ps | grep wash-booking
echo ""

echo "2️⃣ Application Logs (last 20 lines):"
echo "------------------------------------"
docker-compose logs --tail=20 app
echo ""

echo "3️⃣ Testing Local Connection:"
echo "----------------------------"
echo "Testing http://localhost:8000/health ..."
curl -s http://localhost:8000/health || echo "❌ Failed to connect locally"
echo ""

echo "4️⃣ Port Listening Check:"
echo "-----------------------"
netstat -tlnp | grep 8000 || ss -tlnp | grep 8000
echo ""

echo "5️⃣ Firewall Status:"
echo "------------------"
systemctl status firewalld --no-pager | head -5
echo ""

echo "6️⃣ Container Health:"
echo "-------------------"
docker inspect wash-booking-app --format='Health Status: {{.State.Health.Status}}'
echo ""

echo "=========================================="
echo "📋 Summary"
echo "=========================================="
echo ""
echo "If local connection works but external doesn't:"
echo "  → Check firewall: systemctl stop firewalld"
echo "  → Verify AWS Security Group allows port 8000"
echo ""
echo "If local connection fails:"
echo "  → Check logs above for errors"
echo "  → Wait for health status to be 'healthy'"
echo "  → Run: docker-compose restart app"
echo ""
