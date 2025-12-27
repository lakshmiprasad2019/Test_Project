#!/bin/bash

# Frontend Deployment Script for Amazon Linux

echo "=========================================="
echo "🎨 Wash Booking Frontend Deployment"
echo "=========================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    echo "❌ Please run as root (sudo ./deploy-frontend.sh)"
    exit 1
fi

# Step 1: Install Nginx
echo "Step 1: Installing Nginx..."
yum install nginx -y
echo "✅ Nginx installed"
echo ""

# Step 2: Create web directory
echo "Step 2: Creating web directory..."
mkdir -p /var/www/washbooking
echo "✅ Directory created"
echo ""

# Step 3: Copy frontend files
echo "Step 3: Copying frontend files..."
cp -r frontend/* /var/www/washbooking/
chmod -R 755 /var/www/washbooking
echo "✅ Files copied"
echo ""

# Step 4: Configure Nginx
echo "Step 4: Configuring Nginx..."
cat > /etc/nginx/conf.d/washbooking.conf << 'EOF'
server {
    listen 80;
    server_name _;
    
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
EOF
echo "✅ Nginx configured"
echo ""

# Step 5: Start Nginx
echo "Step 5: Starting Nginx..."
systemctl start nginx
systemctl enable nginx
echo "✅ Nginx started and enabled"
echo ""

# Step 6: Configure firewall
echo "Step 6: Configuring firewall..."
if systemctl is-active --quiet firewalld; then
    firewall-cmd --permanent --add-service=http
    firewall-cmd --reload
    echo "✅ Firewall configured"
else
    echo "ℹ️  Firewalld not running, skipping"
fi
echo ""

# Step 7: Get public IP
echo "Step 7: Getting server information..."
PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4)
echo "✅ Server IP: $PUBLIC_IP"
echo ""

echo "=========================================="
echo "✅ Frontend Deployment Complete!"
echo "=========================================="
echo ""
echo "Access your application at:"
echo "  🌐 http://$PUBLIC_IP"
echo ""
echo "API Documentation:"
echo "  📚 http://$PUBLIC_IP:8000/docs"
echo ""
echo "Useful commands:"
echo "  - Check Nginx status: systemctl status nginx"
echo "  - View Nginx logs: tail -f /var/log/nginx/access.log"
echo "  - Restart Nginx: systemctl restart nginx"
echo ""
echo "Note: Make sure port 80 is open in your AWS Security Group!"
echo ""
