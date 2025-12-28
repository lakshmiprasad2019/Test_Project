#!/bin/bash

# Automated HTTPS Setup Script with Let's Encrypt
# This script sets up SSL/TLS certificates for your Wash Booking application

set -e

echo "=========================================="
echo "🔒 HTTPS/SSL Setup for Wash Booking"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (sudo ./setup-https.sh)"
    exit 1
fi

# Get domain name from user
echo "📝 Enter your domain name (e.g., washbooking.com):"
read -r DOMAIN

if [ -z "$DOMAIN" ]; then
    echo "❌ Domain name is required"
    exit 1
fi

echo ""
echo "Domain: $DOMAIN"
echo "www subdomain will also be configured"
echo ""

# Get email for Let's Encrypt
echo "📧 Enter your email for Let's Encrypt notifications:"
read -r EMAIL

if [ -z "$EMAIL" ]; then
    echo "❌ Email is required"
    exit 1
fi

echo ""
echo "=========================================="
echo "Starting HTTPS setup..."
echo "=========================================="
echo ""

# Step 1: Install EPEL and Certbot
echo "Step 1: Installing Certbot..."
yum install epel-release -y > /dev/null 2>&1
yum install certbot python3-certbot-nginx -y > /dev/null 2>&1
echo "✅ Certbot installed"
echo ""

# Step 2: Backup existing Nginx config
echo "Step 2: Backing up Nginx configuration..."
if [ -f /etc/nginx/conf.d/washbooking.conf ]; then
    cp /etc/nginx/conf.d/washbooking.conf /etc/nginx/conf.d/washbooking.conf.backup
    echo "✅ Backup created: /etc/nginx/conf.d/washbooking.conf.backup"
else
    echo "⚠️  No existing config found, creating new one"
fi
echo ""

# Step 3: Create Nginx configuration for HTTP (for Certbot validation)
echo "Step 3: Creating Nginx configuration..."
cat > /etc/nginx/conf.d/washbooking.conf << EOF
server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;
    
    root /var/www/washbooking;
    index index.html;
    
    location / {
        try_files \$uri \$uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF
echo "✅ Nginx configuration created"
echo ""

# Step 4: Test Nginx configuration
echo "Step 4: Testing Nginx configuration..."
nginx -t
if [ $? -eq 0 ]; then
    echo "✅ Nginx configuration is valid"
else
    echo "❌ Nginx configuration has errors"
    exit 1
fi
echo ""

# Step 5: Restart Nginx
echo "Step 5: Restarting Nginx..."
systemctl restart nginx
echo "✅ Nginx restarted"
echo ""

# Step 6: Configure firewall
echo "Step 6: Configuring firewall..."
if systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-service=http > /dev/null 2>&1
    firewall-cmd --permanent --add-service=https > /dev/null 2>&1
    firewall-cmd --reload > /dev/null 2>&1
    echo "✅ Firewall configured (ports 80 and 443 opened)"
else
    echo "ℹ️  Firewalld not running, skipping"
fi
echo ""

# Step 7: Obtain SSL certificate
echo "Step 7: Obtaining SSL certificate from Let's Encrypt..."
echo "This may take a minute..."
echo ""

certbot --nginx \
    -d $DOMAIN \
    -d www.$DOMAIN \
    --non-interactive \
    --agree-tos \
    --email $EMAIL \
    --redirect

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ SSL certificate obtained and installed successfully!"
else
    echo ""
    echo "❌ Failed to obtain SSL certificate"
    echo "Please check:"
    echo "  1. Domain DNS is pointing to this server"
    echo "  2. Ports 80 and 443 are open in AWS Security Group"
    echo "  3. Domain is accessible via HTTP first"
    exit 1
fi
echo ""

# Step 8: Test auto-renewal
echo "Step 8: Testing certificate auto-renewal..."
certbot renew --dry-run > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "✅ Auto-renewal is configured correctly"
else
    echo "⚠️  Auto-renewal test failed, but certificate is installed"
fi
echo ""

# Step 9: Update frontend API URL
echo "Step 9: Updating frontend configuration..."
if [ -f /var/www/washbooking/app.js ]; then
    # Update API URL to use HTTPS
    sed -i "s|const API_BASE_URL = .*|const API_BASE_URL = 'https://$DOMAIN';|" /var/www/washbooking/app.js
    echo "✅ Frontend API URL updated to use HTTPS"
else
    echo "⚠️  Frontend not found at /var/www/washbooking/"
fi
echo ""

# Step 10: Final restart
echo "Step 10: Final Nginx restart..."
systemctl restart nginx
echo "✅ Nginx restarted with SSL configuration"
echo ""

# Get public IP
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)

echo "=========================================="
echo "✅ HTTPS Setup Complete!"
echo "=========================================="
echo ""
echo "Your application is now secured with HTTPS!"
echo ""
echo "Access your application at:"
echo "  🔒 https://$DOMAIN"
echo "  🔒 https://www.$DOMAIN"
echo ""
echo "API Documentation:"
echo "  📚 https://$DOMAIN/api/docs"
echo ""
echo "Certificate details:"
echo "  📜 Issuer: Let's Encrypt"
echo "  📅 Valid for: 90 days"
echo "  🔄 Auto-renewal: Enabled"
echo ""
echo "Important notes:"
echo "  1. HTTP (port 80) automatically redirects to HTTPS"
echo "  2. Certificate will auto-renew before expiration"
echo "  3. Make sure port 443 is open in AWS Security Group"
echo ""
echo "Verify SSL certificate:"
echo "  openssl s_client -connect $DOMAIN:443 -servername $DOMAIN"
echo ""
echo "Check renewal status:"
echo "  sudo certbot certificates"
echo ""
echo "=========================================="
