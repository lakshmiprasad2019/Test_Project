# 🔒 Quick HTTPS Setup Guide

## ⚡ Fastest Way to Enable HTTPS

### Prerequisites
1. **Domain name** (e.g., washbooking.com)
2. **DNS configured** - Point A record to your server IP
3. **Ports 80 and 443 open** in AWS Security Group

---

## 🚀 Automated Setup (Recommended)

### Step 1: Upload Script to Server
Upload `setup-https.sh` to your server

### Step 2: Make Executable
```bash
chmod +x setup-https.sh
```

### Step 3: Run Script
```bash
sudo ./setup-https.sh
```

### Step 4: Enter Details
- Domain name: `your-domain.com`
- Email: `your@email.com`

### Step 5: Wait for Completion
The script will:
- Install Certbot
- Configure Nginx
- Obtain SSL certificate
- Enable auto-renewal
- Update frontend

### Step 6: Access Your Site
```
https://your-domain.com
```

**Done!** 🎉

---

## 📋 Manual Setup (If You Prefer)

### 1. Install Certbot
```bash
sudo yum install epel-release -y
sudo yum install certbot python3-certbot-nginx -y
```

### 2. Get Certificate
```bash
sudo certbot --nginx -d your-domain.com -d www.your-domain.com
```

### 3. Follow Prompts
- Enter email
- Agree to terms
- Choose redirect (option 2)

### 4. Done!
Certificate installed and auto-renewal configured.

---

## 🔧 AWS Security Group Setup

### Add HTTPS Rule

1. **AWS Console** → **EC2** → **Security Groups**
2. **Add Inbound Rule**:
   - Type: **HTTPS**
   - Port: **443**
   - Source: **0.0.0.0/0**
3. **Keep port 80** for HTTP → HTTPS redirect
4. **Save**

---

## 🌐 DNS Configuration

### Point Domain to Server

1. **Get server IP**:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

2. **Add DNS A Record**:
   - **Name**: @ (or subdomain)
   - **Type**: A
   - **Value**: Your server IP
   - **TTL**: 300

3. **Add www subdomain** (optional):
   - **Name**: www
   - **Type**: A
   - **Value**: Your server IP

4. **Wait 5-30 minutes** for DNS propagation

5. **Verify**:
```bash
nslookup your-domain.com
```

---

## ✅ Verification

### Test HTTPS
```bash
# From server
curl -I https://your-domain.com

# Check certificate
openssl s_client -connect your-domain.com:443 -servername your-domain.com

# Test in browser
https://your-domain.com
```

### Check Auto-Renewal
```bash
sudo certbot certificates
sudo certbot renew --dry-run
```

---

## 🔄 Certificate Renewal

### Automatic (Default)
Certbot automatically renews certificates before expiration.

### Manual Renewal
```bash
sudo certbot renew
sudo systemctl restart nginx
```

### Check Renewal Status
```bash
sudo certbot certificates
```

---

## 🐛 Common Issues

### Issue: "Domain not pointing to server"

**Solution**:
```bash
# Check DNS
nslookup your-domain.com

# Should show your server IP
```

### Issue: "Port 443 not accessible"

**Solution**:
```bash
# Check AWS Security Group
# Add HTTPS inbound rule for port 443

# Check firewall
sudo firewall-cmd --list-all
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### Issue: "Certificate validation failed"

**Solution**:
```bash
# Make sure Nginx is running
sudo systemctl status nginx

# Make sure port 80 is accessible
curl http://your-domain.com

# Try again
sudo certbot --nginx -d your-domain.com
```

---

## 📊 What Gets Configured

✅ **SSL/TLS Certificate** from Let's Encrypt  
✅ **HTTPS on port 443**  
✅ **HTTP to HTTPS redirect**  
✅ **Auto-renewal** (every 60 days)  
✅ **Security headers**  
✅ **Modern TLS protocols** (1.2, 1.3)  
✅ **Strong ciphers**  

---

## 🎯 Summary

**Easiest Method**:
1. Get a domain name
2. Point DNS to your server
3. Run `sudo ./setup-https.sh`
4. Enter domain and email
5. Done!

**Access at**: `https://your-domain.com` 🔒

---

## 📞 Support

### Check Logs
```bash
# Nginx logs
sudo tail -f /var/log/nginx/error.log

# Certbot logs
sudo tail -f /var/log/letsencrypt/letsencrypt.log
```

### Get Help
```bash
# Certbot help
sudo certbot --help

# Nginx test
sudo nginx -t
```

---

**Your application will be secured with HTTPS in minutes!** 🚀
