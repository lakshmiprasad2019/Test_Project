# 🔧 DNS Configuration Issue - CRITICAL FIX NEEDED

## ❌ Problem Identified

Your domain **lpitlabs.com** is pointing to **GoDaddy's servers**, NOT your AWS server!

### Current DNS (WRONG):
```
lpitlabs.com → 3.33.130.190 (GoDaddy parking page)
lpitlabs.com → 3.237.105.139 (GoDaddy parking page)
lpitlabs.com → 15.197.148.33 (GoDaddy parking page)
```

### Your AWS Server IP:
```bash
# Run this to get your server IP:
curl http://169.254.169.254/latest/meta-data/public-ipv4

# Or check AWS Console → EC2 → Instances → Public IPv4 address
```

---

## ✅ FIX: Update DNS in GoDaddy

### Step 1: Get Your Server IP

On your AWS server, run:
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

**Write down this IP address!** (Example: 18.212.213.21)

Or get it from AWS Console:
- Go to **EC2 Dashboard**
- Click on your instance
- Look for **Public IPv4 address**

---

### Step 2: Login to GoDaddy

1. Go to: https://www.godaddy.com
2. Login with your account
3. Click **My Products**
4. Find **lpitlabs.com** and click **DNS**

---

### Step 3: Update DNS A Record

In GoDaddy DNS Management:

1. **Find the A Record** with name "@" or "lpitlabs.com"
2. **Click Edit** (pencil icon)
3. **Change the Value** to your AWS server IP
4. **Set TTL** to 600 (10 minutes)
5. **Click Save**

**Configuration should be**:
```
Type: A
Name: @ (or leave blank)
Value: YOUR_AWS_SERVER_IP (from Step 1)
TTL: 600
```

---

### Step 4: Add www Subdomain (Optional)

While you're in GoDaddy DNS:

1. **Click Add** (or Add Record)
2. **Type**: A
3. **Name**: www
4. **Value**: YOUR_AWS_SERVER_IP (same as above)
5. **TTL**: 600
6. **Click Save**

---

### Step 5: Remove/Disable Parking Page

In GoDaddy:

1. Go to **Domain Settings** for lpitlabs.com
2. Look for **Forwarding** section
3. If there's any forwarding enabled, **Delete it**
4. Look for **Parked** status - **Disable** parking page

---

### Step 6: Wait for DNS Propagation

DNS changes take time to propagate:
- **Minimum**: 5-10 minutes
- **Typical**: 30 minutes
- **Maximum**: 48 hours (rare)

---

### Step 7: Verify DNS Update

After 10-15 minutes, check on your server:

```bash
# Check DNS
nslookup lpitlabs.com

# Should now show YOUR server IP, not GoDaddy's IPs
```

**Expected output**:
```
Name:   lpitlabs.com
Address: YOUR_AWS_SERVER_IP
```

---

### Step 8: Test HTTP Access

```bash
# Test from server
curl http://lpitlabs.com

# Should return your frontend HTML
```

---

### Step 9: Get SSL Certificate

Once DNS is pointing to your server:

```bash
# For main domain only
sudo certbot --nginx -d lpitlabs.com

# Or with www (if you added it)
sudo certbot --nginx -d lpitlabs.com -d www.lpitlabs.com
```

---

## 🖼️ GoDaddy DNS Configuration Screenshot Guide

### What You Should See in GoDaddy:

**DNS Records Table**:
```
Type | Name | Value              | TTL
-----|------|--------------------|---------
A    | @    | YOUR_SERVER_IP     | 600
A    | www  | YOUR_SERVER_IP     | 600
```

**What to DELETE/REMOVE**:
- ❌ Any CNAME pointing to GoDaddy
- ❌ Any A records pointing to GoDaddy IPs (3.33.x.x, 3.237.x.x, etc.)
- ❌ Any forwarding rules
- ❌ Parking page settings

---

## 🔍 Verification Checklist

After updating DNS, verify:

```bash
# 1. Check DNS points to your server
nslookup lpitlabs.com
# Should show YOUR IP

# 2. Check HTTP access
curl http://lpitlabs.com
# Should return HTML, not redirect

# 3. Check from external site
# Visit: https://dnschecker.org
# Enter: lpitlabs.com
# Should show your server IP globally

# 4. Test ping
ping lpitlabs.com
# Should ping your server IP
```

---

## ⏰ Timeline

1. **Now**: Update DNS in GoDaddy (5 minutes)
2. **Wait**: 10-30 minutes for DNS propagation
3. **Verify**: Check DNS points to your server
4. **Run**: Certbot to get SSL certificate
5. **Done**: Access https://lpitlabs.com

---

## 🚨 Common GoDaddy DNS Issues

### Issue 1: Nameservers

Make sure nameservers are set to GoDaddy's:
- ns1.domaincontrol.com
- ns2.domaincontrol.com

If using custom nameservers, you need to update DNS there instead.

### Issue 2: Parking Page

GoDaddy automatically parks domains. You must:
1. Add A record pointing to your server
2. Disable parking page
3. Remove any forwarding

### Issue 3: Multiple A Records

Delete all old A records pointing to GoDaddy IPs.
Keep only ONE A record pointing to your AWS server.

---

## 📞 Quick Reference

**Your AWS Server IP**: (Get with command below)
```bash
curl http://169.254.169.254/latest/meta-data/public-ipv4
```

**GoDaddy DNS**: https://dcc.godaddy.com/manage/lpitlabs.com/dns

**DNS Checker**: https://dnschecker.org

---

## ✅ After DNS is Fixed

Once DNS points to your server, run:

```bash
# Update Nginx config
sudo tee /etc/nginx/conf.d/washbooking.conf > /dev/null << 'EOF'
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
    }
}
EOF

# Restart Nginx
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d lpitlabs.com -d www.lpitlabs.com

# Update frontend
sudo sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = 'https://lpitlabs.com';|" /var/www/washbooking/app.js
```

---

## 🎯 Summary

**Problem**: Domain points to GoDaddy, not your server  
**Solution**: Update A record in GoDaddy DNS to your AWS server IP  
**Time**: 10-30 minutes for DNS propagation  
**Then**: Run Certbot to get SSL certificate  

**First step**: Get your server IP and update GoDaddy DNS NOW! 🚀
