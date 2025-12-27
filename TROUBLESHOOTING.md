# 🔍 Troubleshooting Connection Issues

## ✅ Containers Are Running!

Good news - your containers are up:
- `wash-booking-db` - Healthy
- `wash-booking-app` - Starting (health: starting)

---

## 🔧 Troubleshooting Steps

### Step 1: Check Application Logs

The app container shows `health: starting`, which means it's still initializing.

```bash
# View application logs
docker-compose logs -f app

# Or
docker logs wash-booking-app -f
```

**Look for**:
- "Application startup complete"
- Any error messages
- Database connection status

---

### Step 2: Wait for Health Check

The application needs a few seconds to start. Wait 10-20 seconds, then check:

```bash
# Check container status
docker ps

# The STATUS should change from "health: starting" to "healthy"
```

---

### Step 3: Test Locally First

Test from the server itself:

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test root endpoint
curl http://localhost:8000

# If these work, the app is running fine
```

---

### Step 4: Check Firewall on Amazon Linux

Even with Security Groups open, check the local firewall:

```bash
# Check if firewalld is running
systemctl status firewalld

# If running, check rules
firewall-cmd --list-all

# Allow port 8000
firewall-cmd --permanent --add-port=8000/tcp
firewall-cmd --reload

# Or disable firewall temporarily for testing
systemctl stop firewalld
```

---

### Step 5: Check if Port is Listening

```bash
# Check if port 8000 is listening
netstat -tlnp | grep 8000

# Or
ss -tlnp | grep 8000

# Should show:
# tcp   0   0 0.0.0.0:8000   0.0.0.0:*   LISTEN   <pid>/docker-proxy
```

---

### Step 6: Verify Docker Network

```bash
# Check Docker network
docker network inspect test_project_wash-network

# Verify app container is connected
docker inspect wash-booking-app | grep IPAddress
```

---

### Step 7: Check Application Health

```bash
# Check detailed container status
docker inspect wash-booking-app --format='{{.State.Health.Status}}'

# Should eventually show: healthy
```

---

## 🚨 Common Issues and Solutions

### Issue 1: Application Still Starting

**Symptom**: Container shows "health: starting"

**Solution**: Wait 30-60 seconds for the application to fully start

```bash
# Watch the logs
docker-compose logs -f app

# Wait for: "Application startup complete" or similar message
```

---

### Issue 2: Database Connection Error

**Symptom**: Logs show "could not connect to database"

**Solution**: 
```bash
# Restart the app container
docker-compose restart app

# Check database is healthy
docker exec wash-booking-db pg_isready -U washuser -d washbooking
```

---

### Issue 3: Port Binding Issue

**Symptom**: Error about port already in use

**Solution**:
```bash
# Check what's using port 8000
lsof -i :8000

# Kill the process or change the port in docker-compose.yaml
```

---

### Issue 4: Firewall Blocking

**Symptom**: Works locally but not from outside

**Solution**:
```bash
# Check iptables
iptables -L -n | grep 8000

# Temporarily disable firewall for testing
systemctl stop firewalld

# Try curl again from outside
```

---

## 📊 Diagnostic Commands

Run these to gather information:

```bash
# 1. Container status
docker-compose ps

# 2. Application logs (last 50 lines)
docker-compose logs --tail=50 app

# 3. Database logs
docker-compose logs --tail=20 db

# 4. Network connectivity
docker exec wash-booking-app ping -c 3 db

# 5. Check if app is responding inside container
docker exec wash-booking-app curl http://localhost:8000/health

# 6. Port listening
netstat -tlnp | grep 8000

# 7. Firewall status
systemctl status firewalld
```

---

## ✅ Quick Fix Checklist

Run these commands in order:

```bash
# 1. Check logs for errors
docker-compose logs app

# 2. Test locally
curl http://localhost:8000/health

# 3. If local works, check firewall
systemctl stop firewalld

# 4. Try external connection again
curl http://18.212.213.21:8000

# 5. If still fails, check Security Group in AWS Console
# Ensure Inbound Rule: TCP 8000 from 0.0.0.0/0
```

---

## 🎯 Most Likely Issues

Based on your symptoms:

### 1. **Application Still Starting** (Most Likely)
The container shows "health: starting". Wait 30-60 seconds.

```bash
# Watch until status changes to "healthy"
watch -n 2 'docker ps | grep wash-booking-app'
```

### 2. **Firewalld Blocking**
Amazon Linux often has firewalld enabled by default.

```bash
# Quick test - disable firewall
systemctl stop firewalld

# Try connection again
curl http://18.212.213.21:8000
```

### 3. **Application Error**
Check logs for startup errors.

```bash
docker-compose logs app
```

---

## 🔄 If Nothing Works - Restart

```bash
# Stop everything
docker-compose down

# Start again
docker-compose up -d

# Watch logs
docker-compose logs -f
```

---

## 📞 Next Steps

1. **Run**: `docker-compose logs app` and share the output
2. **Run**: `curl http://localhost:8000/health` from the server
3. **Check**: `systemctl status firewalld`
4. **Wait**: 30-60 seconds for the app to fully start

The app is running - we just need to identify what's blocking the connection!
