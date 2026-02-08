"""Main FastAPI application"""

from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from app.config import settings
from app.routes import auth, profile, nutrition

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Health Tracker API for nutrition tracking and user management",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(nutrition.router)


@app.get("/")
def root():
    """Root endpoint - API info"""
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "online",
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.get("/DEPLOY_INFO.txt")
def deploy_info():
    """Serve deployment info for verification systems."""
    info_file = Path("DEPLOY_INFO.txt")
    if info_file.exists():
        return PlainTextResponse(info_file.read_text())
    return PlainTextResponse("DEPLOY_INFO.txt not found", status_code=404)
