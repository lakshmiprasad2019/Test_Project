// API Configuration
const API_BASE_URL = 'http://18.212.213.21:8000';  // Replace with your server IP

// State Management
let currentCustomerId = null;
let selectedService = null;
let vendors = [];
let services = [];

// Initialize App
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadInitialData();
});

// Initialize Application
function initializeApp() {
    setMinDate();
    generateTimeSlots();
}

// Setup Event Listeners
function setupEventListeners() {
    // Customer Form
    document.getElementById('customerForm').addEventListener('submit', handleCustomerSubmit);

    // Booking Form
    document.getElementById('bookingForm').addEventListener('submit', handleBookingSubmit);
    document.getElementById('customerCity').addEventListener('change', loadVendorsByCity);
    document.getElementById('vendorSelect').addEventListener('change', loadVendorServices);
    document.getElementById('serviceSelect').addEventListener('change', updateBookingSummary);
    document.getElementById('vehicleType').addEventListener('change', filterServicesByVehicle);

    // Vendor Form
    document.getElementById('vendorForm').addEventListener('submit', handleVendorSubmit);
}

// Load Initial Data
async function loadInitialData() {
    try {
        await Promise.all([
            loadStats(),
            loadAllServices()
        ]);
    } catch (error) {
        console.error('Error loading initial data:', error);
    }
}

// Load Statistics
async function loadStats() {
    try {
        // Load vendors
        const vendorsResponse = await fetch(`${API_BASE_URL}/api/vendors/`);
        const vendorsData = await vendorsResponse.json();
        document.getElementById('totalVendors').textContent = vendorsData.length;

        // Load bookings
        const bookingsResponse = await fetch(`${API_BASE_URL}/api/bookings/`);
        const bookingsData = await bookingsResponse.json();
        document.getElementById('totalBookings').textContent = bookingsData.length;

        // Estimate customers (unique customer IDs from bookings)
        const uniqueCustomers = new Set(bookingsData.map(b => b.customer_id));
        document.getElementById('totalCustomers').textContent = uniqueCustomers.size;

        animateNumbers();
    } catch (error) {
        console.error('Error loading stats:', error);
    }
}

// Animate Numbers
function animateNumbers() {
    document.querySelectorAll('.stat-number').forEach(el => {
        const target = parseInt(el.textContent);
        let current = 0;
        const increment = target / 50;
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                el.textContent = target;
                clearInterval(timer);
            } else {
                el.textContent = Math.floor(current);
            }
        }, 20);
    });
}

// Load All Services for Display
async function loadAllServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/vendors/`);
        vendors = await response.json();

        // Get services from all vendors
        const allServices = [];
        for (const vendor of vendors.slice(0, 6)) {  // Show first 6 vendors' services
            try {
                const servicesResponse = await fetch(`${API_BASE_URL}/api/vendors/${vendor.id}/services`);
                const vendorServices = await servicesResponse.json();
                allServices.push(...vendorServices.map(s => ({ ...s, vendorName: vendor.name })));
            } catch (error) {
                console.error(`Error loading services for vendor ${vendor.id}:`, error);
            }
        }

        displayServices(allServices);
    } catch (error) {
        console.error('Error loading services:', error);
        showToast('Failed to load services', 'error');
    }
}

// Display Services
function displayServices(services) {
    const grid = document.getElementById('servicesGrid');

    if (services.length === 0) {
        grid.innerHTML = '<p style="grid-column: 1/-1; text-align: center; color: var(--text-muted);">No services available yet. Be the first vendor to register!</p>';
        return;
    }

    grid.innerHTML = services.map(service => `
        <div class="service-card">
            <div class="service-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2">
                    <circle cx="12" cy="12" r="10"/>
                    <path d="M12 6v6l4 2"/>
                </svg>
            </div>
            <h3 class="service-name">${service.name}</h3>
            <p class="service-description">${service.description || 'Professional wash service'}</p>
            <span class="service-vehicle-type">${service.vehicle_type}</span>
            <div class="service-details">
                <div>
                    <div class="service-price">₹${parseFloat(service.price).toFixed(0)}</div>
                    <div class="service-duration">${service.duration_minutes} mins</div>
                </div>
                <div style="text-align: right; color: var(--text-muted); font-size: 0.875rem;">
                    ${service.vendorName || 'Vendor'}
                </div>
            </div>
        </div>
    `).join('');
}

// Handle Customer Form Submit
async function handleCustomerSubmit(e) {
    e.preventDefault();
    showLoading(true);

    const formData = {
        name: document.getElementById('customerName').value,
        email: document.getElementById('customerEmail').value,
        phone: document.getElementById('customerPhone').value,
        city: document.getElementById('customerCity').value
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/bookings/customers/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create customer');
        }

        const customer = await response.json();
        currentCustomerId = customer.id;

        // Load vendors for selected city
        await loadVendorsByCity();

        // Show booking form
        document.getElementById('bookingFormCard').style.display = 'block';
        document.getElementById('customerForm').style.display = 'none';

        showToast('Customer details saved! Now select your service.', 'success');
    } catch (error) {
        console.error('Error creating customer:', error);
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Load Vendors by City
async function loadVendorsByCity() {
    const city = document.getElementById('customerCity').value;
    if (!city) return;

    try {
        const response = await fetch(`${API_BASE_URL}/api/vendors/by-city/${city}`);
        vendors = await response.json();

        const select = document.getElementById('vendorSelect');
        if (vendors.length === 0) {
            select.innerHTML = '<option value="">No vendors available in this city</option>';
            return;
        }

        select.innerHTML = '<option value="">Select a vendor</option>' +
            vendors.map(v => `<option value="${v.id}">${v.name} - ${v.service_area}</option>`).join('');
    } catch (error) {
        console.error('Error loading vendors:', error);
        showToast('Failed to load vendors', 'error');
    }
}

// Load Vendor Services
async function loadVendorServices() {
    const vendorId = document.getElementById('vendorSelect').value;
    if (!vendorId) {
        document.getElementById('serviceSelect').disabled = true;
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/api/vendors/${vendorId}/services`);
        services = await response.json();

        const select = document.getElementById('serviceSelect');
        select.disabled = false;

        if (services.length === 0) {
            select.innerHTML = '<option value="">No services available</option>';
            return;
        }

        select.innerHTML = '<option value="">Select a service</option>' +
            services.map(s => `<option value="${s.id}" data-price="${s.price}" data-duration="${s.duration_minutes}" data-vehicle="${s.vehicle_type}">
                ${s.name} - ₹${parseFloat(s.price).toFixed(0)} (${s.vehicle_type})
            </option>`).join('');
    } catch (error) {
        console.error('Error loading services:', error);
        showToast('Failed to load services', 'error');
    }
}

// Filter Services by Vehicle Type
function filterServicesByVehicle() {
    const vehicleType = document.getElementById('vehicleType').value;
    const serviceSelect = document.getElementById('serviceSelect');

    if (!vehicleType || services.length === 0) return;

    const filteredServices = services.filter(s => s.vehicle_type === vehicleType);

    serviceSelect.innerHTML = '<option value="">Select a service</option>' +
        filteredServices.map(s => `<option value="${s.id}" data-price="${s.price}" data-duration="${s.duration_minutes}" data-vehicle="${s.vehicle_type}">
            ${s.name} - ₹${parseFloat(s.price).toFixed(0)}
        </option>`).join('');
}

// Update Booking Summary
function updateBookingSummary() {
    const serviceSelect = document.getElementById('serviceSelect');
    const selectedOption = serviceSelect.options[serviceSelect.selectedIndex];

    if (!selectedOption || !selectedOption.value) {
        document.getElementById('bookingSummary').style.display = 'none';
        return;
    }

    const price = selectedOption.dataset.price;
    const duration = selectedOption.dataset.duration;
    const serviceName = selectedOption.text.split(' - ')[0];

    document.getElementById('summaryService').textContent = serviceName;
    document.getElementById('summaryPrice').textContent = `₹${parseFloat(price).toFixed(0)}`;
    document.getElementById('summaryDuration').textContent = `${duration} minutes`;
    document.getElementById('bookingSummary').style.display = 'block';

    selectedService = services.find(s => s.id == selectedOption.value);
}

// Handle Booking Form Submit
async function handleBookingSubmit(e) {
    e.preventDefault();
    showLoading(true);

    const date = document.getElementById('bookingDate').value;
    const time = document.getElementById('bookingTime').value;
    const bookingDateTime = `${date}T${time}:00`;

    const formData = {
        customer_id: currentCustomerId,
        vendor_id: parseInt(document.getElementById('vendorSelect').value),
        service_id: parseInt(document.getElementById('serviceSelect').value),
        city: document.getElementById('customerCity').value,
        booking_date: bookingDateTime,
        vehicle_type: document.getElementById('vehicleType').value,
        vehicle_number: document.getElementById('vehicleNumber').value || null,
        service_address: document.getElementById('serviceAddress').value || null,
        pincode: document.getElementById('pincode').value || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/bookings/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to create booking');
        }

        const booking = await response.json();

        showToast(`Booking confirmed! Booking ID: ${booking.id}`, 'success');

        // Reset forms
        document.getElementById('customerForm').reset();
        document.getElementById('bookingForm').reset();
        document.getElementById('customerForm').style.display = 'block';
        document.getElementById('bookingFormCard').style.display = 'none';
        document.getElementById('bookingSummary').style.display = 'none';

        // Reload stats
        loadStats();

        // Scroll to top
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        console.error('Error creating booking:', error);
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Handle Vendor Form Submit
async function handleVendorSubmit(e) {
    e.preventDefault();
    showLoading(true);

    const formData = {
        name: document.getElementById('vendorName').value,
        email: document.getElementById('vendorEmail').value,
        phone: document.getElementById('vendorPhone').value,
        city: document.getElementById('vendorCity').value,
        service_area: document.getElementById('serviceArea').value,
        address: document.getElementById('vendorAddress').value || null
    };

    try {
        const response = await fetch(`${API_BASE_URL}/api/vendors/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Failed to register vendor');
        }

        const vendor = await response.json();

        showToast(`Vendor registered successfully! Vendor ID: ${vendor.id}`, 'success');
        document.getElementById('vendorForm').reset();

        // Reload stats
        loadStats();
    } catch (error) {
        console.error('Error registering vendor:', error);
        showToast(error.message, 'error');
    } finally {
        showLoading(false);
    }
}

// Utility Functions
function setMinDate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const minDate = `${year}-${month}-${day}`;

    // Set max date to end of current month
    const lastDay = new Date(year, today.getMonth() + 1, 0).getDate();
    const maxDate = `${year}-${month}-${lastDay}`;

    const dateInput = document.getElementById('bookingDate');
    dateInput.min = minDate;
    dateInput.max = maxDate;
}

function generateTimeSlots() {
    const select = document.getElementById('bookingTime');
    const slots = [];

    for (let hour = 9; hour < 18; hour++) {
        const time = `${String(hour).padStart(2, '0')}:00`;
        slots.push(`<option value="${time}">${formatTime(time)}</option>`);
    }

    select.innerHTML = '<option value="">Select Time</option>' + slots.join('');
}

function formatTime(time) {
    const [hour] = time.split(':');
    const h = parseInt(hour);
    const ampm = h >= 12 ? 'PM' : 'AM';
    const displayHour = h > 12 ? h - 12 : h;
    return `${displayHour}:00 ${ampm}`;
}

function scrollToSection(sectionId) {
    document.getElementById(sectionId).scrollIntoView({ behavior: 'smooth' });
}

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 4000);
}

function showLoading(show) {
    const overlay = document.getElementById('loadingOverlay');
    overlay.classList.toggle('show', show);
}

// Update active nav link on scroll
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;

    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');

        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});
