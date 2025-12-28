# 🔧 HTTPS Setup for Amazon Linux 2023

## ⚠️ Amazon Linux 2023 Differences

Amazon Linux 2023 uses:
- ✅ **dnf** instead of yum
- ✅ **No EPEL** repository needed
- ✅ Certbot available directly

---

## 🚀 Quick Fix - Use Updated Script

I've created a new script specifically for Amazon Linux 2023:

### Step 1: Upload New Script
Upload `setup-https-al2023.sh` to your server

### Step 2: Make Executable
```bash
chmod +x setup-https-al2023.sh
```

### Step 3: Run Script
```bash
sudo ./setup-https-al2023.sh
```

### Step 4: Enter Details
- Domain: `lpitlabs.com`
- Email: `jaggarapu.prasad@gmail.com`

---

## 📋 Manual Installation (Alternative)

If you prefer to do it manually:

### Step 1: Install Certbot

```bash
# Install Certbot for Amazon Linux 2023
sudo dnf install -y python3-certbot-nginx
```

If that doesn't work, try:
```bash
# Install via pip
sudo dnf install -y python3-pip
sudo pip3 install certbot certbot-nginx
```

### Step 2: Configure Nginx

Create `/etc/nginx/conf.d/washbooking.conf`:

```bash
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Add:
```nginx
server {
    listen 80;
    server_name lpitlabs.com www.lpitlabs.com;
    
    root /var/www/washbooking;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Step 3: Test and Restart Nginx

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

### Step 4: Obtain SSL Certificate

```bash
sudo certbot --nginx \
    -d lpitlabs.com \
    -d www.lpitlabs.com \
    --email jaggarapu.prasad@gmail.com \
    --agree-tos \
    --redirect \
    --non-interactive
```

### Step 5: Verify

```bash
# Check certificate
sudo certbot certificates

# Test HTTPS
curl -I https://lpitlabs.com
```

---

## 🔍 Verify DNS First

Before running Certbot, make sure DNS is configured:

```bash
# Check if domain points to your server
nslookup lpitlabs.com

# Should show your server IP
# Get your server IP:
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

---

## 🔧 AWS Security Group

Make sure these ports are open:

1. **AWS Console** → **EC2** → **Security Groups**
2. **Add Inbound Rules**:
   - **HTTP** (80) - 0.0.0.0/0
   - **HTTPS** (443) - 0.0.0.0/0

---

## ✅ Quick Commands Summary

```bash
# 1. Install Certbot
sudo dnf install -y python3-certbot-nginx

# 2. Get certificate
sudo certbot --nginx -d lpitlabs.com -d www.lpitlabs.com

# 3. Test auto-renewal
sudo certbot renew --dry-run

# 4. Check status
sudo certbot certificates
```

---

## 🐛 Troubleshooting

### Issue: "certbot: command not found"

**Solution**:
```bash
# Install via pip
sudo dnf install -y python3-pip
sudo pip3 install certbot certbot-nginx

# Add to PATH
export PATH=$PATH:/usr/local/bin
```

### Issue: "Challenge failed"

**Solution**:
```bash
# Check DNS
nslookup lpitlabs.com

# Check if domain is accessible
curl http://lpitlabs.com

# Check Nginx is running
sudo systemctl status nginx
```

### Issue: "Port 80 connection refused"

**Solution**:
```bash
# Start Nginx
sudo systemctl start nginx

# Check if listening
sudo netstat -tlnp | grep :80
```

---

## 📊 Package Differences

| Amazon Linux 2 | Amazon Linux 2023 |
|----------------|-------------------|
| yum | dnf |
| epel-release | Not needed |
| certbot via EPEL | certbot via dnf |

---

## 🎯 Recommended Approach

**Use the updated script**: `setup-https-al2023.sh`

It handles all Amazon Linux 2023 specifics automatically!

```bash
chmod +x setup-https-al2023.sh
sudo ./setup-https-al2023.sh
```

---

**Your HTTPS setup will work perfectly on Amazon Linux 2023!** 🚀
