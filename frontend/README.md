# 🎨 Wash Booking Frontend

Beautiful, modern frontend UI for the Wash Booking application.

## ✨ Features

- **Modern Dark Theme** with premium design
- **Responsive Layout** - works on all devices
- **Real-time API Integration** with your backend
- **Smooth Animations** and transitions
- **Interactive Forms** with validation
- **Dynamic Content** loading
- **Toast Notifications** for user feedback
- **Loading States** and error handling

---

## 📁 Files

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # Premium dark theme CSS
├── app.js          # JavaScript with API integration
└── README.md       # This file
```

---

## 🚀 Quick Start

### Option 1: Serve with Python (Recommended)

```bash
cd frontend
python3 -m http.server 3000
```

Then open: `http://localhost:3000`

### Option 2: Serve with Node.js

```bash
cd frontend
npx http-server -p 3000
```

### Option 3: Open Directly

Simply open `index.html` in your browser (may have CORS issues with API calls).

---

## ⚙️ Configuration

### Update API URL

Edit `app.js` and change the API_BASE_URL:

```javascript
const API_BASE_URL = 'http://YOUR_SERVER_IP:8000';
```

Replace `YOUR_SERVER_IP` with your actual server IP address.

---

## 🌐 Deploy to Production

### Option 1: Serve with Nginx

1. **Install Nginx** on your server:
```bash
sudo yum install nginx -y
```

2. **Copy frontend files**:
```bash
sudo mkdir -p /var/www/washbooking
sudo cp -r frontend/* /var/www/washbooking/
```

3. **Configure Nginx**:
```bash
sudo nano /etc/nginx/conf.d/washbooking.conf
```

Add:
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    root /var/www/washbooking;
    index index.html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # Enable CORS for API calls
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

4. **Start Nginx**:
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

### Option 2: Add to Docker Compose

Add this service to your `docker-compose.yaml`:

```yaml
  frontend:
    image: nginx:alpine
    container_name: wash-booking-frontend
    volumes:
      - ./frontend:/usr/share/nginx/html:ro
    ports:
      - "80:80"
    networks:
      - wash-network
    restart: unless-stopped
```

Then run:
```bash
docker-compose up -d
```

---

## 🔧 Enable CORS on Backend

To allow the frontend to call the API, CORS is already enabled in the FastAPI backend.

If you face CORS issues, verify in `app/main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📱 Features Overview

### 1. **Home Section**
- Hero banner with call-to-action buttons
- Live statistics (bookings, vendors, customers)
- Smooth animations

### 2. **Services Section**
- Dynamic service cards loaded from API
- Shows service details, pricing, duration
- Filtered by vehicle type

### 3. **Booking Section**
- Two-step booking process
- Customer registration
- Service selection with real-time availability
- Date/time picker (current month only)
- Booking summary with pricing

### 4. **Vendor Registration**
- Simple vendor onboarding form
- City and service area selection
- Instant registration

---

## 🎨 Customization

### Change Colors

Edit `styles.css` and modify the CSS variables:

```css
:root {
    --primary: #6366f1;        /* Primary color */
    --secondary: #10b981;      /* Secondary color */
    --bg-primary: #0f172a;     /* Background */
    /* ... more variables */
}
```

### Add Your Logo

Replace the SVG logo in `index.html`:

```html
<div class="nav-brand">
    <img src="your-logo.png" alt="Logo" class="logo-icon">
    <span class="brand-name">YourBrand</span>
</div>
```

---

## 📊 API Integration

The frontend connects to these API endpoints:

- `GET /api/vendors/` - List all vendors
- `GET /api/vendors/by-city/{city}` - Vendors by city
- `GET /api/vendors/{id}/services` - Vendor services
- `POST /api/bookings/customers/` - Create customer
- `POST /api/bookings/` - Create booking
- `POST /api/vendors/` - Register vendor
- `GET /api/bookings/` - List bookings (for stats)

---

## 🐛 Troubleshooting

### CORS Errors

**Problem**: "Access to fetch has been blocked by CORS policy"

**Solution**: 
1. Make sure CORS is enabled in backend (it already is)
2. Use a proper web server (not file://)
3. Serve frontend from same domain as API

### API Connection Failed

**Problem**: Cannot connect to API

**Solution**:
1. Check API_BASE_URL in `app.js`
2. Verify backend is running: `curl http://YOUR_IP:8000`
3. Check firewall allows port 8000
4. Verify AWS Security Group settings

### Forms Not Submitting

**Problem**: Forms don't work

**Solution**:
1. Check browser console for errors
2. Verify API is responding
3. Check form validation (phone, email format)

---

## 🚀 Performance Tips

1. **Enable Gzip** in Nginx:
```nginx
gzip on;
gzip_types text/css application/javascript;
```

2. **Add Caching Headers**:
```nginx
location ~* \.(css|js)$ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

3. **Minify CSS/JS** for production:
```bash
# Install minifier
npm install -g minify

# Minify files
minify styles.css > styles.min.css
minify app.js > app.min.js
```

---

## 📱 Mobile Responsive

The UI is fully responsive and works on:
- ✅ Desktop (1920px+)
- ✅ Laptop (1366px)
- ✅ Tablet (768px)
- ✅ Mobile (375px+)

---

## 🎯 Browser Support

- ✅ Chrome/Edge (latest)
- ✅ Firefox (latest)
- ✅ Safari (latest)
- ✅ Mobile browsers

---

## 📞 Support

For issues or questions:
- Check browser console for errors
- Verify API is running
- Check network tab in DevTools
- Ensure CORS is enabled

---

**Your beautiful frontend is ready to use!** 🎉

Open `index.html` in a browser or serve it with a web server to get started!
