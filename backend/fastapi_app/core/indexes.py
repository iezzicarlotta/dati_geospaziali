"""MongoDB indexes setup for geospatial queries and performance."""

from pymongo import ASCENDING, DESCENDING, GEOSPHERE
from pymongo.errors import DuplicateKeyError
from datetime import datetime


class IndexManager:
    """Manages MongoDB indexes for both collections."""
    
    @staticmethod
    def setup_fontanelle_indexes(collection):
        """
        Create indexes for fontanelle collection (GeoJSON Feature format).
        
        Indexes:
        - 2dsphere on geometry: for geospatial queries (distance, within area)
        - ascending on properties.ID_NIL: for joins/aggregations
        - ascending on properties.MUNICIPIO: for municipal filtering
        
        Args:
            collection: MongoDB collection for fontanelle
        """
        try:
            # Geospatial index on "geometry" field (GeoJSON Feature format)
            collection.create_index(
                [("geometry", GEOSPHERE)],
                name="idx_fontanelle_geometry_geospatial",
                background=True
            )
            print("✓ Created geospatial index on fontanelle.geometry")
        except DuplicateKeyError:
            print("ℹ Geospatial index on fontanelle.geometry already exists")
        
        try:
            # Foreign key index for joins with NIL
            collection.create_index(
                [("properties.ID_NIL", ASCENDING)],
                name="idx_fontanelle_nil_id",
                background=True
            )
            print("✓ Created index on fontanelle.properties.ID_NIL")
        except DuplicateKeyError:
            print("ℹ Index on fontanelle.properties.ID_NIL already exists")
        
        try:
            # Municipality filtering
            collection.create_index(
                [("properties.MUNICIPIO", ASCENDING)],
                name="idx_fontanelle_municipio",
                background=True
            )
            print("✓ Created index on fontanelle.properties.MUNICIPIO")
        except DuplicateKeyError:
            print("ℹ Index on fontanelle.properties.MUNICIPIO already exists")
        
        try:
            # CAP filtering
            collection.create_index(
                [("properties.CAP", ASCENDING)],
                name="idx_fontanelle_cap",
                background=True
            )
            print("✓ Created index on fontanelle.properties.CAP")
        except DuplicateKeyError:
            print("ℹ Index on fontanelle.properties.CAP already exists")
    
    @staticmethod
    def setup_nil_indexes(collection):
        """
        Create indexes for NIL collection (GeoJSON Feature format).
        
        Indexes:
        - 2dsphere on geometry: for geospatial queries (intersection, containment)
        - ascending on properties.ID_NIL: for direct lookups
        - ascending on properties.NIL: for name searches
        
        Args:
            collection: MongoDB collection for NIL
        """
        try:
            # Geospatial index for polygon queries (GeoJSON Feature format)
            collection.create_index(
                [("geometry", GEOSPHERE)],
                name="idx_nil_geometry_geospatial",
                background=True
            )
            print("✓ Created geospatial index on nil.geometry")
        except DuplicateKeyError:
            print("ℹ Geospatial index on nil.geometry already exists")
        
        try:
            # Direct lookup by NIL ID
            collection.create_index(
                [("properties.ID_NIL", ASCENDING)],
                name="idx_nil_id_unique",
                background=True
            )
            print("✓ Created index on nil.properties.ID_NIL")
        except DuplicateKeyError:
            print("ℹ Index on nil.properties.ID_NIL already exists")
        
        try:
            # Direct lookup by name
            collection.create_index(
                [("properties.NIL", ASCENDING)],
                name="idx_nil_name",
                background=True
            )
            print("✓ Created index on nil.properties.NIL")
        except DuplicateKeyError:
            print("ℹ Index on nil.properties.NIL already exists")
    
    @classmethod
    def initialize_all_indexes(cls, db):
        """
        Initialize all indexes for both collections.
        
        Args:
            db: MongoDB database instance
        """
        print("\n=== Setting up MongoDB Indexes ===\n")
        
        # Fontanelle indexes
        print("Setting up fontanelle indexes...")
        cls.setup_fontanelle_indexes(db.fontanelle)
        
        print("\nSetting up NIL indexes...")
        # NIL indexes
        cls.setup_nil_indexes(db.nil)
        
        print("\n✓ All indexes configured successfully\n")

