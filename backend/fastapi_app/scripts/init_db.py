"""
Database initialization script - creates collections, indexes, and seed data.

Usage:
    python -m backend.fastapi_app.scripts.init_db
"""

from datetime import datetime
from backend.fastapi_app.core.database import MongoDBConnection
from backend.fastapi_app.core.indexes import IndexManager


def create_collections_and_indexes():
    """Create collections and set up all indexes."""
    db = MongoDBConnection.get_database()
    
    # Create collections explicitly (optional but good practice)
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
    
    # Set up all indexes
    IndexManager.initialize_all_indexes(db)


def seed_sample_data():
    """Populate database with minimal sample data for testing."""
    db = MongoDBConnection.get_database()
    
    print("\n=== Seeding Sample Data ===\n")
    
    # Sample NIL data
    nil_data = [
        {
            "nome": "NIL 1 - Centro Storico",
            "numero": 1,
            "zona": "Centro",
            "geometria": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [9.17, 45.45],
                        [9.19, 45.45],
                        [9.19, 45.47],
                        [9.17, 45.47],
                        [9.17, 45.45]
                    ]
                ]
            },
            "descrizione": "Area centrale di Milano",
            "popolazione": 15000,
            "area_kmq": 2.5,
            "comuni_interessati": ["Milano"],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "fontanelle_count": 0
        },
        {
            "nome": "NIL 2 - Navigli",
            "numero": 2,
            "zona": "Ovest",
            "geometria": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [9.15, 45.43],
                        [9.17, 45.43],
                        [9.17, 45.45],
                        [9.15, 45.45],
                        [9.15, 45.43]
                    ]
                ]
            },
            "descrizione": "Area dei Navigli",
            "popolazione": 12000,
            "area_kmq": 2.0,
            "comuni_interessati": ["Milano"],
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow(),
            "fontanelle_count": 0
        }
    ]
    
    # Clear existing data (optional - comment out for production)
    db.nil.delete_many({})
    result_nil = db.nil.insert_many(nil_data)
    print(f"✓ Inserted {len(result_nil.inserted_ids)} NIL records")
    
    # Get NIL IDs for foreign key references
    nil_docs = list(db.nil.find({}, {"_id": 1}))
    nil_id_1 = str(nil_docs[0]["_id"])
    nil_id_2 = str(nil_docs[1]["_id"])
    
    # Sample Fontanelle data
    fontanelle_data = [
        {
            "nome": "Fontanella Piazza Duomo",
            "descrizione": "Fontanella storica in Piazza Duomo",
            "coordinate": {
                "type": "Point",
                "coordinates": [9.1845, 45.4642]  # [longitude, latitude]
            },
            "indirizzo": "Piazza Duomo, Milano",
            "quartiere": "Centro Storico",
            "nil_id": nil_id_1,
            "consorzio": "Consortium A",
            "data_installazione": datetime(2010, 6, 15),
            "stato": "attiva",
            "accessibilita": True,
            "note": "Fontanella ben mantenuta",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "nome": "Fontanella Via Torino",
            "descrizione": "Fontanella nelle vicinanze di Via Torino",
            "coordinate": {
                "type": "Point",
                "coordinates": [9.1780, 45.4520]
            },
            "indirizzo": "Via Torino, Milano",
            "quartiere": "Centro",
            "nil_id": nil_id_2,
            "consorzio": "Consortium B",
            "data_installazione": datetime(2015, 3, 22),
            "stato": "attiva",
            "accessibilita": False,
            "note": "Recentemente ristrutturata",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        },
        {
            "nome": "Fontanella Navigli",
            "descrizione": "Fontanella zona Navigli",
            "coordinate": {
                "type": "Point",
                "coordinates": [9.1620, 45.4410]
            },
            "indirizzo": "Ripa di Porta Ticinese, Milano",
            "quartiere": "Navigli",
            "nil_id": nil_id_2,
            "consorzio": "Consortium B",
            "data_installazione": datetime(2018, 9, 10),
            "stato": "manutenzione",
            "accessibilita": True,
            "note": "In manutenzione - riapertura prevista a fine mese",
            "createdAt": datetime.utcnow(),
            "updatedAt": datetime.utcnow()
        }
    ]
    
    # Clear existing data (optional - comment out for production)
    db.fontanelle.delete_many({})
    result_fontanelle = db.fontanelle.insert_many(fontanelle_data)
    print(f"✓ Inserted {len(result_fontanelle.inserted_ids)} fontanelle records")


def verify_setup():
    """Verify that the database is properly configured."""
    db = MongoDBConnection.get_database()
    
    print("\n=== Verification ===\n")
    
    # Check collections
    collections = db.list_collection_names()
    print(f"Collections: {collections}")
    
    # Check counts
    nil_count = db.nil.count_documents({})
    fontanelle_count = db.fontanelle.count_documents({})
    print(f"NIL documents: {nil_count}")
    print(f"Fontanelle documents: {fontanelle_count}")
    
    # Check indexes
    print("\nFontanelle indexes:")
    for index in db.fontanelle.list_indexes():
        print(f"  - {index['name']}")
    
    print("\nNIL indexes:")
    for index in db.nil.list_indexes():
        print(f"  - {index['name']}")
    
    # Test a geospatial query
    print("\n=== Testing Geospatial Query ===")
    fontanelle = db.fontanelle.find_one({
        "coordinate": {
            "$near": {
                "$geometry": {
                    "type": "Point",
                    "coordinates": [9.1845, 45.4642]
                },
                "$maxDistance": 1000  # 1 km
            }
        }
    })
    if fontanelle:
        print(f"✓ Found fontanella near coordinates: {fontanelle['nome']}")
    else:
        print("ℹ No fontanelle found in test radius")


def main():
    """Run all initialization steps."""
    print("=" * 50)
    print("MongoDB Database Initialization")
    print(f"Database: {MongoDBConnection.get_database().name}")
    print("=" * 50)
    
    try:
        # We don't create collections and indexes if they exist
        create_collections_and_indexes()
        
        # Seed data (optional - comment out for production)
        seed_sample_data()
        
        # Verify setup
        verify_setup()
        
        print("\n" + "=" * 50)
        print("✓ Database initialization completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n✗ Error during initialization: {e}")
        raise
    finally:
        MongoDBConnection.disconnect()


if __name__ == "__main__":
    main()
