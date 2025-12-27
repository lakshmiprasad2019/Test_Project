"""
FastAPI application entry point for Wash Booking System.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import bookings, vendors

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Wash Booking API",
    description="API for booking bike and car wash services in Indian cities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(bookings.router)
app.include_router(vendors.router)


@app.get("/")
def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Welcome to Wash Booking API",
        "version": "1.0.0",
        "status": "active",
        "docs": "/docs"
    }


@app.get("/health")
def health_check():
    """
    Health check endpoint for Kubernetes probes.
    """
    return {
        "status": "healthy",
        "service": "wash-booking-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
