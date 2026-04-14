"""Bootstrap FastAPI application with MongoDB integration."""

from fastapi import FastAPI
from backend.fastapi_app.core.database import MongoDBConnection


def create_app() -> FastAPI:
    app = FastAPI(
        title="Fontanelle Milano API",
        version="0.1.0",
        description="API for geospatial data management: fontanelle and NIL"
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
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {
            "status": "ok",
            "application": "Fontanelle Milano API",
            "database": "dbSpaziali"
        }
    
    return app


app = create_app()

