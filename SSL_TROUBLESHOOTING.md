# 🔧 SSL Certificate Issues - Solutions

## 🔍 Issues Identified

### Issue 1: www subdomain not configured
```
Domain: www.lpitlabs.com
Type: dns
Detail: NXDOMAIN - DNS record doesn't exist
```

### Issue 2: Domain has a redirect/landing page
```
Domain: lpitlabs.com
Type: unauthorized
Detail: Got landing page HTML instead of challenge file
```

---

## ✅ Solution 1: Get Certificate for Main Domain Only

Skip the www subdomain for now and get certificate just for `lpitlabs.com`:

### Step 1: Stop any interfering services

```bash
# Check what's running on port 80
sudo netstat -tlnp | grep :80

# If there's a landing page or redirect, we need to disable it temporarily
```

### Step 2: Make sure Nginx serves the challenge file

```bash
# Edit Nginx config
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Make sure it looks like this (remove any redirects):
```nginx
server {
    listen 80;
    server_name lpitlabs.com;
    
    root /var/www/washbooking;
    index index.html;
    
    # Important: Allow Let's Encrypt challenges
    location /.well-known/acme-challenge/ {
        root /var/www/washbooking;
        try_files $uri =404;
    }
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Step 3: Test and restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

### Step 4: Test if domain is accessible

```bash
# Test from server
curl http://lpitlabs.com

# Should return your frontend HTML, not a redirect
```

### Step 5: Get certificate for main domain only

```bash
sudo certbot --nginx \
    -d lpitlabs.com \
    --email jaggarapu.prasad@gmail.com \
    --agree-tos \
    --redirect \
    --non-interactive
```

---

## ✅ Solution 2: Add www DNS Record

If you want www subdomain too:

### Step 1: Add DNS A Record in GoDaddy

1. Login to GoDaddy
2. Go to DNS Management for lpitlabs.com
3. Add A Record:
   - **Type**: A
   - **Name**: www
   - **Value**: Your server IP (get it with: `curl http://169.254.169.254/latest/meta-data/public-ipv4`)
   - **TTL**: 600

### Step 2: Wait for DNS propagation (5-30 minutes)

```bash
# Check if www is configured
nslookup www.lpitlabs.com

# Should show your server IP
```

### Step 3: Then run Certbot with both domains

```bash
sudo certbot --nginx \
    -d lpitlabs.com \
    -d www.lpitlabs.com \
    --email jaggarapu.prasad@gmail.com \
    --agree-tos \
    --redirect \
    --non-interactive
```

---

## ✅ Solution 3: Check for GoDaddy Landing Page

GoDaddy sometimes adds a landing page. Check:

### Step 1: Check DNS settings

```bash
# Check what lpitlabs.com points to
nslookup lpitlabs.com

# Should show YOUR server IP, not GoDaddy's parking page
```

### Step 2: Disable GoDaddy forwarding/parking

1. Login to GoDaddy
2. Go to Domain Settings
3. Check "Forwarding" section
4. **Disable** any forwarding or parking page
5. Make sure DNS points directly to your server

### Step 3: Verify no redirect

```bash
# Test from server
curl -I http://lpitlabs.com

# Should return: HTTP/1.1 200 OK
# NOT: HTTP/1.1 301 or 302 (redirect)
```

---

## 🚀 Quick Fix - Run This Now

### Option A: Certificate for lpitlabs.com only (fastest)

```bash
# 1. Update Nginx config (no www)
sudo tee /etc/nginx/conf.d/washbooking.conf > /dev/null << 'EOF'
server {
    listen 80;
    server_name lpitlabs.com;
    
    root /var/www/washbooking;
    index index.html;
    
    location /.well-known/acme-challenge/ {
        root /var/www/washbooking;
    }
    
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
EOF

# 2. Restart Nginx
sudo systemctl restart nginx

# 3. Get certificate (main domain only)
sudo certbot --nginx \
    -d lpitlabs.com \
    --email jaggarapu.prasad@gmail.com \
    --agree-tos \
    --redirect \
    --non-interactive

# 4. Update frontend
sudo sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = 'https://lpitlabs.com';|" /var/www/washbooking/app.js
```

---

## 🔍 Debugging Commands

```bash
# 1. Check DNS
nslookup lpitlabs.com
nslookup www.lpitlabs.com

# 2. Check what's on port 80
sudo netstat -tlnp | grep :80

# 3. Test HTTP access
curl -I http://lpitlabs.com

# 4. Check Nginx config
sudo nginx -t

# 5. View Nginx logs
sudo tail -f /var/log/nginx/error.log

# 6. View Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

---

## 📊 What's Happening

The error message shows:
```
Expected challenge file
Got: <!DOCTYPE html>...<script>window.location.href="/lander"</script>
```

This means:
1. ❌ Domain is redirecting to a landing page
2. ❌ Certbot can't place its validation file
3. ❌ Let's Encrypt can't verify domain ownership

**Solution**: Remove any redirects/landing pages, ensure Nginx serves files directly.

---

## ✅ Recommended Action

**Run Option A above** - Get certificate for `lpitlabs.com` only (without www).

You can add www later after configuring its DNS record.

```bash
# Quick command:
sudo certbot --nginx -d lpitlabs.com
```

This will work if:
- ✅ lpitlabs.com points to your server
- ✅ No redirects interfering
- ✅ Nginx can serve files

---

## 🎯 After Success

Once you get the certificate:

```bash
# Test HTTPS
curl -I https://lpitlabs.com

# Should return: HTTP/2 200
```

Then access: **https://lpitlabs.com** 🔒

---

**Try Option A now - it should work!** 🚀
