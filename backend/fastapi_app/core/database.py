"""MongoDB connection and database management."""

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.errors import ServerSelectionTimeoutError, ConnectionFailure
from contextlib import contextmanager
from typing import Optional, Generator

from .config import settings


class MongoDBConnection:
    """Manages MongoDB connection and database access."""
    
    _client: Optional[MongoClient] = None
    
    @classmethod
    def connect(cls) -> MongoClient:
        """
        Establish connection to MongoDB.
        
        Returns:
            MongoClient: Connected MongoDB client
            
        Raises:
            ConnectionFailure: If connection to MongoDB fails
        """
        if cls._client is None:
            try:
                cls._client = MongoClient(
                    settings.mongodb_url,
                    serverSelectionTimeoutMS=settings.mongodb_timeout * 1000,
                    connectTimeoutMS=settings.mongodb_timeout * 1000,
                )
                # Verify connection
                cls._client.admin.command("ping")
                print(f"✓ Connected to MongoDB at {settings.mongodb_url}")
            except (ServerSelectionTimeoutError, ConnectionFailure) as e:
                print(f"✗ Failed to connect to MongoDB: {e}")
                raise
        return cls._client
    
    @classmethod
    def disconnect(cls) -> None:
        """Close MongoDB connection."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            print("✓ Disconnected from MongoDB")
    
    @classmethod
    def get_database(cls) -> Database:
        """
        Get database instance.
        
        Returns:
            Database: MongoDB database object
        """
        client = cls.connect()
        return client[settings.mongodb_database]
    
    @classmethod
    def get_collection(cls, collection_name: str) -> Collection:
        """
        Get collection instance.
        
        Args:
            collection_name: Name of the collection
            
        Returns:
            Collection: MongoDB collection object
        """
        db = cls.get_database()
        return db[collection_name]


@contextmanager
def get_db_context() -> Generator[Database, None, None]:
    """
    Context manager for database operations.
    Usage:
        with get_db_context() as db:
            db.fontanelle.find_one(...)
    """
    db = MongoDBConnection.get_database()
    try:
        yield db
    finally:
        pass  # Keep connection alive for reuse


# Singleton instance
db_connection = MongoDBConnection()
