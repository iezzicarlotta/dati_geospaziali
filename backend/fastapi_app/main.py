"""Bootstrap FastAPI application with MongoDB integration."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.fastapi_app.core.database import MongoDBConnection
from backend.fastapi_app.api.v1.routes.fountains import router as fountains_router


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fontanelle Milano API",
        version="0.1.0",
        description="API for geospatial data management: fontanelle and NIL"
    )
    
    # Add CORS middleware for frontend integration
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, restrict to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.on_event("startup")
    async def startup():
        """Initialize MongoDB connection on startup."""
        try:
            MongoDBConnection.connect()
            print("✓ FastAPI started with MongoDB connection")
        except Exception as e:
            print(f"✗ Failed to connect to MongoDB during startup: {e}")
            raise
    
    @app.on_event("shutdown")
    async def shutdown():
        """Close MongoDB connection on shutdown."""
        MongoDBConnection.disconnect()
        print("✓ FastAPI shutdown, MongoDB disconnected")
    
    # Register routers
    app.include_router(fountains_router, prefix="/api/v1")
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "ok",
            "application": "Fontanelle Milano API",
            "database": "dbSpaziali"
        }
    
    @app.get("/")
    async def root():
        """API documentation redirect."""
        return {
            "message": "Fontanelle Milano API",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    
    return app


app = create_app()

