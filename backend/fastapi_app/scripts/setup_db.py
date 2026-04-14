"""
Database initialization script - sets up indexes for existing data.

Usage:
    python -m backend.fastapi_app.scripts.init_db

Note: This script preserves existing data and only creates collections + indexes.
Perfect for real data already loaded in the database.
"""

from backend.fastapi_app.core.database import MongoDBConnection
from backend.fastapi_app.core.indexes import IndexManager


def setup():
    """Initialize database collections and indexes."""
    db = MongoDBConnection.get_database()
    
    print("=" * 60)
    print("MongoDB Database Setup")
    print(f"Database: {db.name}")
    print("=" * 60)
    
    # Ensure collections exist
    if "fontanelle" not in db.list_collection_names():
        db.create_collection("fontanelle")
        print("✓ Created collection: fontanelle")
    else:
        print("ℹ Collection fontanelle already exists")
    
    if "nil" not in db.list_collection_names():
        db.create_collection("nil")
        print("✓ Created collection: nil")
    else:
        print("ℹ Collection nil already exists")
    
    print()
    # Set up all indexes
    IndexManager.initialize_all_indexes(db)
    
    # Verify
    print("\n" + "=" * 60)
    print("Database Status")
    print("=" * 60)
    
    nil_count = db.nil.count_documents({})
    fontanelle_count = db.fontanelle.count_documents({})
    
    print(f"NIL documents: {nil_count}")
    print(f"Fontanelle documents: {fontanelle_count}")
    
    print("\nFontanelle indexes:")
    for idx in db.fontanelle.list_indexes():
        print(f"  ✓ {idx['name']}")
    
    print("\nNIL indexes:")
    for idx in db.nil.list_indexes():
        print(f"  ✓ {idx['name']}")
    
    print("\n" + "=" * 60)
    print("✓ Setup completed successfully!")
    print("Database is ready for geospatial queries")
    print("=" * 60)


if __name__ == "__main__":
    try:
        setup()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        MongoDBConnection.disconnect()
