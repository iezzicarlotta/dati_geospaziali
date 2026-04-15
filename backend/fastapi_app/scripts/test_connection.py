"""
Minimal test script to verify MongoDB connection and data.

Usage:
    python -m backend.fastapi_app.scripts.test_connection
"""

from backend.fastapi_app.core.database import MongoDBConnection


def test_connection():
    """Test basic MongoDB connection."""
    print("\n=== Testing MongoDB Connection ===\n")
    
    try:
        db = MongoDBConnection.get_database()
        print(f"✓ Connected to database: {db.name}")
        
        # Verify database name
        if db.name != "dbSpaziali":
            raise ValueError(f"Wrong database name: {db.name}. Expected: dbSpaziali")
        print(f"✓ Database name verified: {db.name}")
        
        # Test ping
        db.client.admin.command("ping")
        print("✓ Ping successful")
        
        return True
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return False


def test_collections():
    """Test collection access and document count."""
    print("\n=== Testing Collections ===\n")
    
    try:
        db = MongoDBConnection.get_database()
        
        # Check collections
        collections = db.list_collection_names()
        print(f"Collections in database: {collections}")
        
        # Count documents
        fontanelle_count = db.fontanelle.count_documents({})
        nil_count = db.nil.count_documents({})
        
        print(f"✓ Fontanelle documents: {fontanelle_count}")
        print(f"✓ NIL documents: {nil_count}")
        
        return fontanelle_count >= 0 and nil_count >= 0
    except Exception as e:
        print(f"✗ Collection test failed: {e}")
        return False


def test_indexes():
    """Test that all indexes are present."""
    print("\n=== Testing Indexes ===\n")
    
    try:
        db = MongoDBConnection.get_database()
        
        # Expected indexes (GeoJSON Feature format)
        expected_fontanelle = {
            "idx_fontanelle_geometry_geospatial",
            "idx_fontanelle_nil_id",
            "idx_fontanelle_municipio",
            "idx_fontanelle_cap"
        }
        
        expected_nil = {
            "idx_nil_geometry_geospatial",
            "idx_nil_id_unique",
            "idx_nil_name"
        }
        
        # Get actual indexes
        fontanelle_indexes = {
            idx["name"]
            for idx in db.fontanelle.list_indexes()
            if idx["name"] != "_id_"  # Exclude default _id index
        }
        
        nil_indexes = {
            idx["name"]
            for idx in db.nil.list_indexes()
            if idx["name"] != "_id_"
        }
        
        print(f"Fontanelle indexes: {fontanelle_indexes}")
        print(f"NIL indexes: {nil_indexes}")
        
        # Check if all expected indexes exist
        fontanelle_ok = expected_fontanelle.issubset(fontanelle_indexes)
        nil_ok = expected_nil.issubset(nil_indexes)
        
        if fontanelle_ok:
            print("✓ All fontanelle indexes present")
        else:
            missing = expected_fontanelle - fontanelle_indexes
            print(f"✗ Missing fontanelle indexes: {missing}")
        
        if nil_ok:
            print("✓ All NIL indexes present")
        else:
            missing = expected_nil - nil_indexes
            print(f"✗ Missing NIL indexes: {missing}")
        
        return fontanelle_ok and nil_ok
    except Exception as e:
        print(f"✗ Index test failed: {e}")
        return False


def test_geospatial_query():
    """Test geospatial query functionality."""
    print("\n=== Testing Geospatial Query ===\n")
    
    try:
        db = MongoDBConnection.get_database()
        
        # Query fontanelle entro 2km dal Duomo (GeoJSON Feature format)
        fontanelle = list(db.fontanelle.find(
            {
                "geometry": {
                    "$near": {
                        "$geometry": {
                            "type": "Point",
                            "coordinates": [9.1845, 45.4642]
                        },
                        "$maxDistance": 2000  # 2 km
                    }
                }
            }
        ).limit(5))
        
        print(f"✓ Found {len(fontanelle)} fontanelle within 2km of Duomo")
        
        if fontanelle:
            for f in fontanelle:
                props = f.get('properties', {})
                print(f"  - NIL: {props.get('NIL', 'N/A')}, Coord: {props.get('LONG_X_4326', 'N/A')}, {props.get('LAT_Y_4326', 'N/A')}")
        
        # Query NIL containing a point (GeoJSON Feature format)
        nil = db.nil.find_one({
            "geometry": {
                "$geoIntersects": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": [9.1845, 45.4642]
                    }
                }
            }
        })
        
        if nil:
            props = nil.get('properties', {})
            print(f"✓ Found NIL containing Duomo point: {props.get('NIL', 'N/A')}")
        else:
            print("ℹ No NIL found containing Duomo (might be expected)")
        
        return True
    except Exception as e:
        print(f"✗ Geospatial query test failed: {e}")
        return False


def test_schemas():
    """Test Pydantic schemas."""
    print("\n=== Testing Pydantic Schemas ===\n")
    
    try:
        from backend.fastapi_app.schemas.fontanella import Fontanella, FontanellaCreate, Point, FontanellaProperties
        
        # Test Point schema
        point = Point(coordinates=(9.1845, 45.4642))
        print(f"✓ Point schema: {point.model_dump()}")
        
        # Test FontanellaCreate schema (GeoJSON Feature format)
        fontanella_data = {
            "type": "Feature",
            "properties": {
                "objectID": "test-1",
                "CAP": "20100",
                "MUNICIPIO": "1",
                "ID_NIL": "1",
                "NIL": "Test NIL"
            },
            "geometry": {"type": "Point", "coordinates": [9.1845, 45.4642]}
        }
        fontanella = FontanellaCreate(**fontanella_data)
        print(f"✓ FontanellaCreate schema validated: {fontanella.properties.objectID}")
        
        return True
    except Exception as e:
        print(f"✗ Schema test failed: {e}")
        return False


def run_all_tests():
    """Run all tests."""
    print("=" * 60)
    print("MongoDB Connection and Data Integrity Tests")
    print("=" * 60)
    
    results = {
        "Connection": test_connection(),
        "Collections": test_collections(),
        "Indexes": test_indexes(),
        "Geospatial Query": test_geospatial_query(),
        "Schemas": test_schemas()
    }
    
    print("\n" + "=" * 60)
    print("Test Results Summary")
    print("=" * 60)
    
    all_passed = True
    for test_name, passed in results.items():
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"{status} - {test_name}")
        if not passed:
            all_passed = False
    
    print("=" * 60)
    
    if all_passed:
        print("\n✓ All tests passed! Database is ready.")
    else:
        print("\n✗ Some tests failed. Check MongoDB setup.")
    
    return all_passed


if __name__ == "__main__":
    try:
        success = run_all_tests()
    finally:
        MongoDBConnection.disconnect()
        print("\n✓ Connection closed")
