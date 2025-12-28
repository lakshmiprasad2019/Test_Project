# 🔒 HTTPS/SSL Setup Guide

## Overview

This guide will help you enable HTTPS (port 443) for your Wash Booking application using free SSL certificates.

---

## 📋 Certificate Options

### **Option 1: Let's Encrypt (Recommended - Fully Automated)**
- ✅ **Free forever**
- ✅ **Automatic renewal**
- ✅ **Trusted by all browsers**
- ✅ **Easy setup with Certbot**
- ⚠️ Requires a domain name

### **Option 2: DigiCert Free Trial**
- ✅ Free for 90 days
- ⚠️ Requires manual renewal
- ⚠️ Requires domain validation
- ⚠️ More complex setup

### **Option 3: Self-Signed Certificate (Development Only)**
- ✅ Immediate setup
- ✅ No domain required
- ⚠️ Browser warnings
- ⚠️ Not for production

---

## 🚀 Option 1: Let's Encrypt with Certbot (RECOMMENDED)

### Prerequisites
- A domain name pointing to your server IP
- Ports 80 and 443 open in AWS Security Group

### Step 1: Point Domain to Your Server

1. **Get your server's public IP**:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

2. **Add DNS A Record**:
   - Go to your domain registrar (GoDaddy, Namecheap, etc.)
   - Add an A record:
     - **Name**: @ (or your subdomain)
     - **Type**: A
     - **Value**: Your server IP (e.g., 18.212.213.21)
     - **TTL**: 300

3. **Wait for DNS propagation** (5-30 minutes):
```bash
nslookup your-domain.com
```

### Step 2: Install Certbot

```bash
# Install EPEL repository
sudo yum install epel-release -y

# Install Certbot and Nginx plugin
sudo yum install certbot python3-certbot-nginx -y
```

### Step 3: Update Nginx Configuration

Edit `/etc/nginx/conf.d/washbooking.conf`:

```bash
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Replace with:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # SSL certificates (will be added by Certbot)
    # ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    # ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    
    root /var/www/washbooking;
    index index.html;
    
    # Serve frontend
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Proxy API requests to backend
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # CORS headers
        add_header 'Access-Control-Allow-Origin' '*' always;
        add_header 'Access-Control-Allow-Methods' 'GET, POST, PATCH, DELETE, OPTIONS' always;
        add_header 'Access-Control-Allow-Headers' 'Content-Type' always;
        
        if ($request_method = 'OPTIONS') {
            return 204;
        }
    }
    
    # Enable gzip compression
    gzip on;
    gzip_types text/css application/javascript application/json;
    gzip_min_length 1000;
}
```

### Step 4: Test Nginx Configuration

```bash
sudo nginx -t
```

### Step 5: Obtain SSL Certificate

```bash
# Get certificate and auto-configure Nginx
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Follow the prompts:
# - Enter your email
# - Agree to terms
# - Choose to redirect HTTP to HTTPS (option 2)
```

### Step 6: Test Auto-Renewal

```bash
# Test renewal process
sudo certbot renew --dry-run
```

### Step 7: Open Port 443 in AWS Security Group

1. AWS Console → EC2 → Security Groups
2. Add Inbound Rule:
   - **Type**: HTTPS
   - **Port**: 443
   - **Source**: 0.0.0.0/0

### Step 8: Restart Nginx

```bash
sudo systemctl restart nginx
```

### Step 9: Test HTTPS

```bash
# Test from server
curl https://your-domain.com

# Open in browser
https://your-domain.com
```

---

## 🔐 Option 2: DigiCert Free Certificate

### Step 1: Get DigiCert Free Trial Certificate

1. **Visit DigiCert**:
   - Go to: https://www.digicert.com/free-ssl-certificate
   - Or use their trial: https://www.digicert.com/tls-ssl/compare-certificates

2. **Sign up for free trial**:
   - Create an account
   - Request a free 90-day trial certificate
   - Choose "Single Domain" certificate

3. **Domain Validation**:
   - DigiCert will ask you to validate domain ownership
   - Choose one method:
     - **Email validation**: Receive email at admin@your-domain.com
     - **DNS validation**: Add TXT record to DNS
     - **File validation**: Upload file to your server

### Step 2: Download Certificate Files

After validation, download these files:
- `your-domain.crt` (Certificate)
- `your-domain.key` (Private Key)
- `DigiCertCA.crt` (Intermediate Certificate)

### Step 3: Upload Certificates to Server

```bash
# Create SSL directory
sudo mkdir -p /etc/ssl/washbooking

# Upload your files to server, then move them:
sudo mv your-domain.crt /etc/ssl/washbooking/
sudo mv your-domain.key /etc/ssl/washbooking/
sudo mv DigiCertCA.crt /etc/ssl/washbooking/

# Set permissions
sudo chmod 600 /etc/ssl/washbooking/your-domain.key
sudo chmod 644 /etc/ssl/washbooking/your-domain.crt
sudo chmod 644 /etc/ssl/washbooking/DigiCertCA.crt
```

### Step 4: Configure Nginx for DigiCert

```bash
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com www.your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com www.your-domain.com;
    
    # DigiCert SSL certificates
    ssl_certificate /etc/ssl/washbooking/your-domain.crt;
    ssl_certificate_key /etc/ssl/washbooking/your-domain.key;
    ssl_trusted_certificate /etc/ssl/washbooking/DigiCertCA.crt;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    
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
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### Step 5: Test and Restart

```bash
# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

---

## 🔧 Option 3: Self-Signed Certificate (Development)

### Step 1: Generate Self-Signed Certificate

```bash
# Create SSL directory
sudo mkdir -p /etc/ssl/washbooking

# Generate certificate (valid for 365 days)
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout /etc/ssl/washbooking/selfsigned.key \
  -out /etc/ssl/washbooking/selfsigned.crt \
  -subj "/C=IN/ST=Maharashtra/L=Mumbai/O=WashBooking/CN=washbooking.local"

# Set permissions
sudo chmod 600 /etc/ssl/washbooking/selfsigned.key
sudo chmod 644 /etc/ssl/washbooking/selfsigned.crt
```

### Step 2: Configure Nginx

```bash
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Add:
```nginx
server {
    listen 80;
    server_name _;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name _;
    
    # Self-signed certificate
    ssl_certificate /etc/ssl/washbooking/selfsigned.crt;
    ssl_certificate_key /etc/ssl/washbooking/selfsigned.key;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    root /var/www/washbooking;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}
```

### Step 3: Restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

**Note**: Browsers will show a security warning. Click "Advanced" → "Proceed anyway".

---

## 📝 Update Frontend API URL

Edit `frontend/app.js`:

```javascript
// Change from HTTP to HTTPS
const API_BASE_URL = 'https://your-domain.com';
```

Then update the file on server:
```bash
sudo cp frontend/app.js /var/www/washbooking/
```

---

## 🔒 AWS Security Group Configuration

Add HTTPS inbound rule:

1. AWS Console → EC2 → Security Groups
2. Add Inbound Rule:
   - **Type**: HTTPS
   - **Port**: 443
   - **Source**: 0.0.0.0/0
3. Keep port 80 open for HTTP → HTTPS redirect
4. Keep port 8000 open for API (or proxy through 443)

---

## ✅ Verification Checklist

```bash
# 1. Test Nginx configuration
sudo nginx -t

# 2. Check if Nginx is running
sudo systemctl status nginx

# 3. Test HTTP redirect
curl -I http://your-domain.com

# 4. Test HTTPS
curl -I https://your-domain.com

# 5. Check SSL certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# 6. Test in browser
# Open: https://your-domain.com
```

---

## 🔄 Certificate Renewal

### Let's Encrypt (Automatic)
Certbot auto-renews. Check with:
```bash
sudo certbot renew --dry-run
```

### DigiCert (Manual)
- Renew before 90 days
- Download new certificate
- Replace files in `/etc/ssl/washbooking/`
- Restart Nginx

---

## 🐛 Troubleshooting

### Port 443 Not Accessible

```bash
# Check if Nginx is listening on 443
sudo netstat -tlnp | grep :443

# Check firewall
sudo firewall-cmd --list-all

# Add HTTPS if missing
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### Certificate Errors

```bash
# Check certificate details
sudo openssl x509 -in /etc/letsencrypt/live/your-domain.com/fullchain.pem -text -noout

# Check Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Mixed Content Warnings

Update `app.js` to use HTTPS for API calls:
```javascript
const API_BASE_URL = window.location.protocol + '//' + window.location.host;
```

---

## 📊 Comparison

| Feature | Let's Encrypt | DigiCert | Self-Signed |
|---------|--------------|----------|-------------|
| Cost | Free | Free trial | Free |
| Validity | 90 days | 90 days | 365 days |
| Auto-renewal | ✅ Yes | ❌ No | ❌ No |
| Browser trust | ✅ Yes | ✅ Yes | ❌ No |
| Domain required | ✅ Yes | ✅ Yes | ❌ No |
| Setup difficulty | Easy | Medium | Easy |
| **Recommendation** | **Production** | Trial/Enterprise | Dev only |

---

## 🎯 Recommended Approach

**For Production**: Use **Let's Encrypt** with Certbot
- Free forever
- Automatic renewal
- Trusted by all browsers
- Easy setup

**Steps**:
1. Get a domain name
2. Point it to your server
3. Run Certbot
4. Done!

---

Your application will be accessible at **`https://your-domain.com`** 🔒
