"""Main FastAPI application for EduPredict"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.core.config import settings
from app.api.routes import api_router

app = FastAPI(
    title="EduPredict API",
    description="AI Data-Driven Student Academic Performance Prediction System",
    version="1.0.0",
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Parse CORS origins from comma-separated string
cors_origins = [origin.strip() for origin in settings.cors_origins.split(",")]

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Mount static files if directory exists
if os.path.exists(settings.static_dir):
    app.mount("/static", StaticFiles(directory=settings.static_dir), name="static")


@app.get("/")
async def root():
    return {
        "message": "EduPredict API",
        "version": "1.0.0",
        "description": "AI Data-Driven Student Academic Performance Prediction System",
        "docs": "/docs" if settings.debug else "disabled",
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "EduPredict API"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
    )