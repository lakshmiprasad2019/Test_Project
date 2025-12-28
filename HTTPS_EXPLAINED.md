# 🔒 HTTPS Setup Script Explained

## 📚 Complete Breakdown of setup-https-al2023.sh

This document explains every step the script performed to enable HTTPS on your application.

---

## 🎯 Overview

The script automated the process of:
1. Installing SSL certificate tools
2. Configuring web server (Nginx)
3. Obtaining SSL certificate from Let's Encrypt
4. Enabling HTTPS with automatic HTTP redirect
5. Setting up auto-renewal

---

## 📋 Step-by-Step Explanation

### **Step 1: Install Certbot**

```bash
dnf install -y python3-certbot-nginx
```

**What it does**:
- Installs **Certbot** - Let's Encrypt's official client
- Installs **Nginx plugin** - Allows Certbot to automatically configure Nginx
- Uses `dnf` (Amazon Linux 2023's package manager)

**Why needed**:
- Certbot communicates with Let's Encrypt servers
- Handles certificate generation, installation, and renewal
- The Nginx plugin automates Nginx configuration

**Alternative** (if dnf fails):
```bash
pip3 install certbot certbot-nginx
```

---

### **Step 2: Backup Existing Nginx Config**

```bash
cp /etc/nginx/conf.d/washbooking.conf /etc/nginx/conf.d/washbooking.conf.backup
```

**What it does**:
- Creates a backup of your current Nginx configuration
- Saves to `.backup` file

**Why needed**:
- Safety measure - can restore if something goes wrong
- Allows rollback to previous configuration
- Good practice before making changes

---

### **Step 3: Create Nginx Configuration for HTTP**

```bash
cat > /etc/nginx/conf.d/washbooking.conf << EOF
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
        ...
    }
}
EOF
```

**What it does**:
- Creates Nginx server block for HTTP (port 80)
- Defines document root (`/var/www/washbooking`)
- Sets up routing for frontend and API

**Why needed**:
- Let's Encrypt needs HTTP access to verify domain ownership
- Certbot will modify this config to add HTTPS
- Establishes baseline configuration

**Key directives explained**:
- `listen 80` - Listen on HTTP port
- `server_name` - Domains this config applies to
- `root` - Where to find website files
- `location /` - How to serve frontend files
- `location /api` - Proxy API requests to backend (port 8000)

---

### **Step 4: Test Nginx Configuration**

```bash
nginx -t
```

**What it does**:
- Validates Nginx configuration syntax
- Checks for errors before applying

**Why needed**:
- Prevents breaking Nginx with invalid config
- Catches typos and syntax errors
- Ensures server won't crash on restart

**Output**:
```
nginx: the configuration file /etc/nginx/nginx.conf syntax is ok
nginx: configuration file /etc/nginx/nginx.conf test is successful
```

---

### **Step 5: Restart Nginx**

```bash
systemctl restart nginx
```

**What it does**:
- Stops and starts Nginx service
- Loads new configuration

**Why needed**:
- Apply the new HTTP configuration
- Make server accessible on port 80
- Prepare for Let's Encrypt validation

---

### **Step 6: Configure Firewall**

```bash
firewall-cmd --permanent --add-service=http
firewall-cmd --permanent --add-service=https
firewall-cmd --reload
```

**What it does**:
- Opens port 80 (HTTP) in firewall
- Opens port 443 (HTTPS) in firewall
- Makes changes permanent (survive reboot)
- Reloads firewall to apply changes

**Why needed**:
- Allow external access to your website
- Let's Encrypt needs to reach port 80 for validation
- Users need port 443 for HTTPS access

**Note**: This is for the **server firewall** (firewalld). You also need **AWS Security Group** rules!

---

### **Step 7: DNS Verification**

```bash
CURRENT_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
DOMAIN_IP=$(dig +short lpitlabs.com | head -n1)
```

**What it does**:
- Gets your server's public IP from AWS metadata
- Queries DNS to see where domain points
- Compares the two

**Why needed**:
- Verify DNS is configured correctly
- Prevent certificate request failure
- Warn user if DNS doesn't match

**Example**:
```
Server IP: 18.212.213.21
Domain IP: 18.212.213.21
✅ Match - proceed!
```

---

### **Step 8: Obtain SSL Certificate** (The Main Event!)

```bash
certbot --nginx \
    -d lpitlabs.com \
    -d www.lpitlabs.com \
    --non-interactive \
    --agree-tos \
    --email jaggarapu.prasad@gmail.com \
    --redirect
```

**What it does** (this is complex, so let's break it down):

#### **8a. Domain Validation (ACME Challenge)**

1. **Certbot contacts Let's Encrypt** servers
2. **Let's Encrypt issues a challenge**:
   - Creates a random token (e.g., `b1FZiXwdxQyI2IYbMXpaG27e1tKI9ejBGVyE71FqPns`)
   - Asks Certbot to place it at: `http://lpitlabs.com/.well-known/acme-challenge/TOKEN`

3. **Certbot creates the challenge file**:
   - Places file in `/var/www/washbooking/.well-known/acme-challenge/`
   - File contains the token

4. **Let's Encrypt verifies**:
   - Fetches `http://lpitlabs.com/.well-known/acme-challenge/TOKEN`
   - Checks if content matches expected token
   - If match → Domain ownership verified! ✅

#### **8b. Certificate Generation**

1. **Certbot generates a private key** (2048-bit RSA)
2. **Creates a Certificate Signing Request (CSR)**
3. **Sends CSR to Let's Encrypt**
4. **Let's Encrypt issues certificate**:
   - Certificate for `lpitlabs.com`
   - Certificate for `www.lpitlabs.com`
   - Valid for 90 days

#### **8c. Certificate Installation**

Certbot saves files to:
```
/etc/letsencrypt/live/lpitlabs.com/
├── fullchain.pem    # Certificate + Intermediate CA
├── privkey.pem      # Private key (keep secret!)
├── cert.pem         # Your certificate only
└── chain.pem        # Intermediate CA certificate
```

#### **8d. Nginx Auto-Configuration**

Certbot modifies `/etc/nginx/conf.d/washbooking.conf`:

**Before** (HTTP only):
```nginx
server {
    listen 80;
    server_name lpitlabs.com www.lpitlabs.com;
    ...
}
```

**After** (HTTP redirect + HTTPS):
```nginx
# HTTP server - redirect to HTTPS
server {
    listen 80;
    server_name lpitlabs.com www.lpitlabs.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS server
server {
    listen 443 ssl http2;
    server_name lpitlabs.com www.lpitlabs.com;
    
    # SSL certificates
    ssl_certificate /etc/letsencrypt/live/lpitlabs.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/lpitlabs.com/privkey.pem;
    
    # SSL configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    # Security headers
    add_header Strict-Transport-Security "max-age=31536000" always;
    
    # Your application config
    root /var/www/washbooking;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header X-Forwarded-Proto https;
        ...
    }
}
```

**Key additions**:
- `listen 443 ssl http2` - HTTPS on port 443 with HTTP/2
- `ssl_certificate` - Path to certificate
- `ssl_certificate_key` - Path to private key
- `ssl_protocols` - Only modern, secure protocols (TLS 1.2, 1.3)
- `ssl_ciphers` - Strong encryption algorithms
- `add_header Strict-Transport-Security` - Force HTTPS (HSTS)
- HTTP server now redirects to HTTPS

**Command flags explained**:
- `-d lpitlabs.com` - Domain to get certificate for
- `--nginx` - Use Nginx plugin (auto-configure)
- `--non-interactive` - Don't ask questions (use defaults)
- `--agree-tos` - Agree to Let's Encrypt Terms of Service
- `--email` - For renewal notifications
- `--redirect` - Automatically redirect HTTP → HTTPS

---

### **Step 9: Test Auto-Renewal**

```bash
certbot renew --dry-run
```

**What it does**:
- Simulates certificate renewal process
- Tests if auto-renewal will work
- Doesn't actually renew (dry run)

**Why needed**:
- Certificates expire in 90 days
- Auto-renewal must work to avoid downtime
- Verifies renewal configuration

**How auto-renewal works**:
1. **Certbot creates a systemd timer**:
   ```bash
   systemctl list-timers | grep certbot
   ```
   
2. **Timer runs twice daily**:
   - Checks if certificates expire in < 30 days
   - If yes, automatically renews
   - Reloads Nginx to use new certificate

3. **Renewal process**:
   - Same as initial: ACME challenge → verify → new certificate
   - Happens automatically, no manual intervention

---

### **Step 10: Update Frontend API URL**

```bash
sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = 'https://lpitlabs.com';|" /var/www/washbooking/app.js
```

**What it does**:
- Finds line in `app.js` with `API_BASE_URL`
- Replaces it with HTTPS URL
- Modifies file in-place (`-i` flag)

**Why needed**:
- Frontend was using HTTP for API calls
- Now needs to use HTTPS to avoid "mixed content" warnings
- Browsers block HTTP requests from HTTPS pages

**Before**:
```javascript
const API_BASE_URL = 'http://lpitlabs.com';
```

**After**:
```javascript
const API_BASE_URL = 'https://lpitlabs.com';
```

---

### **Step 11: Final Nginx Restart**

```bash
systemctl restart nginx
```

**What it does**:
- Restarts Nginx with SSL configuration
- Loads certificates
- Enables HTTPS

**Why needed**:
- Apply all Certbot's configuration changes
- Start serving HTTPS traffic
- Enable HTTP → HTTPS redirect

---

## 🔐 How SSL/TLS Works

### **The Handshake Process**

When a user visits `https://lpitlabs.com`:

1. **Client Hello**:
   - Browser: "I want to connect securely"
   - Sends supported TLS versions and ciphers

2. **Server Hello**:
   - Nginx: "Let's use TLS 1.3 with AES-256-GCM"
   - Sends SSL certificate

3. **Certificate Verification**:
   - Browser checks certificate:
     - ✅ Issued by trusted CA (Let's Encrypt)
     - ✅ Domain matches (lpitlabs.com)
     - ✅ Not expired
     - ✅ Signature valid

4. **Key Exchange**:
   - Browser and server create shared encryption key
   - Uses certificate's public key

5. **Encrypted Communication**:
   - All traffic encrypted with shared key
   - 🔒 Secure connection established!

---

## 📁 Files Created/Modified

### **Certificate Files**:
```
/etc/letsencrypt/
├── live/lpitlabs.com/
│   ├── fullchain.pem     # Certificate chain
│   ├── privkey.pem       # Private key (SECRET!)
│   ├── cert.pem          # Your certificate
│   └── chain.pem         # CA certificate
│
├── archive/lpitlabs.com/ # Actual files (live/ is symlink)
├── renewal/              # Auto-renewal config
└── accounts/             # Let's Encrypt account info
```

### **Nginx Configuration**:
```
/etc/nginx/conf.d/washbooking.conf       # Modified for HTTPS
/etc/nginx/conf.d/washbooking.conf.backup # Backup
```

### **Systemd Timer** (Auto-renewal):
```
/etc/systemd/system/timers.target.wants/certbot-renew.timer
```

---

## 🔄 Certificate Lifecycle

### **Day 0**: Certificate issued
- Valid for 90 days
- Installed and active

### **Day 1-59**: Normal operation
- Certificate valid
- Auto-renewal timer checks daily
- No action needed

### **Day 60**: Auto-renewal triggered
- Timer detects < 30 days remaining
- Runs `certbot renew`
- New certificate issued
- Nginx reloaded
- **No downtime!**

### **Day 61-150**: New certificate active
- Old certificate expires (Day 90)
- New certificate valid until Day 150
- Cycle repeats

---

## 🛡️ Security Features Enabled

### **1. Strong Encryption**
```nginx
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers HIGH:!aNULL:!MD5;
```
- Only modern TLS versions
- Strong cipher suites
- No weak algorithms

### **2. HSTS (HTTP Strict Transport Security)**
```nginx
add_header Strict-Transport-Security "max-age=31536000" always;
```
- Forces HTTPS for 1 year
- Prevents downgrade attacks
- Browsers remember to use HTTPS

### **3. HTTP/2**
```nginx
listen 443 ssl http2;
```
- Faster page loads
- Multiplexing
- Header compression

### **4. Automatic Redirect**
```nginx
return 301 https://$server_name$request_uri;
```
- All HTTP traffic → HTTPS
- Permanent redirect (301)
- No insecure connections

---

## 🎯 Summary

The script performed these key actions:

1. ✅ **Installed Certbot** - SSL certificate management tool
2. ✅ **Configured Nginx** - Web server for HTTP
3. ✅ **Verified DNS** - Domain points to server
4. ✅ **Obtained Certificate** - From Let's Encrypt (free, trusted)
5. ✅ **Configured HTTPS** - Nginx serves encrypted traffic
6. ✅ **Enabled Redirect** - HTTP → HTTPS automatic
7. ✅ **Set Up Auto-Renewal** - Certificate renews automatically
8. ✅ **Updated Frontend** - API calls use HTTPS
9. ✅ **Added Security Headers** - HSTS, modern TLS

**Result**: Your application is now secured with industry-standard HTTPS! 🔒

---

## 📊 What You Got

✅ **Free SSL Certificate** (worth $50-200/year)  
✅ **Automatic Renewal** (no maintenance)  
✅ **A+ Security Rating** (check: ssllabs.com/ssltest)  
✅ **Trusted by All Browsers** (no warnings)  
✅ **SEO Boost** (Google prefers HTTPS)  
✅ **User Trust** (🔒 padlock in browser)  

**All automated in one script!** 🚀
