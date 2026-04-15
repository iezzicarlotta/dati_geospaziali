"""Schemas for geospatial data: Fontanelle and NIL (GeoJSON Features format)."""

from pydantic import BaseModel, Field
from typing import Optional, List, Literal, Dict, Any
from datetime import datetime
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom type for MongoDB ObjectId."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)
    
    def __repr__(self):
        return f"ObjectId('{self}')"


# ====================== GeoJSON Base Models ======================

class Point(BaseModel):
    """GeoJSON Point for coordinates."""
    type: Literal["Point"] = "Point"
    coordinates: tuple[float, float] = Field(
        ..., 
        description="[longitude, latitude] in WGS84"
    )


class Polygon(BaseModel):
    """GeoJSON Polygon for areas."""
    type: Literal["Polygon"] = "Polygon"
    coordinates: List[List[tuple[float, float]]] = Field(
        ...,
        description="Array of linear rings (exterior ring + holes)"
    )


# ====================== Fontanelle Schema (GeoJSON Feature) ======================

class FontanellaProperties(BaseModel):
    """Properties for fontanella GeoJSON feature."""
    objectID: str = Field(..., alias="objectID")
    CAP: Optional[str] = None
    MUNICIPIO: Optional[str] = None
    ID_NIL: Optional[str] = None
    NIL: Optional[str] = None
    LONG_X_4326: Optional[float] = None
    LAT_Y_4326: Optional[float] = None
    Location: Optional[str] = None
    
    class Config:
        populate_by_name = True


class FontanellaCreate(BaseModel):
    """Schema for creating a fontanella (GeoJSON Feature format)."""
    type: Literal["Feature"] = "Feature"
    properties: FontanellaProperties
    geometry: Point


class Fontanella(FontanellaCreate):
    """Complete fontanella record from database (with _id)."""
    id: Optional[PyObjectId] = Field(None, alias="_id")
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


# ====================== NIL Schema (GeoJSON Feature) ======================

class NILProperties(BaseModel):
    """Properties for NIL GeoJSON feature."""
    ID_NIL: int = Field(...)
    NIL: str = Field(...)
    Valido_dal: Optional[str] = None
    Valido_al: Optional[str] = None
    Fonte: Optional[str] = None
    Shape_Length: Optional[float] = None
    Shape_Area: Optional[float] = None
    OBJECTID: Optional[int] = None
    
    class Config:
        populate_by_name = True


class NILCreate(BaseModel):
    """Schema for creating a NIL (GeoJSON Feature format)."""
    type: Literal["Feature"] = "Feature"
    id: Optional[int] = None
    properties: NILProperties
    geometry: Polygon


class NIL(NILCreate):
    """Complete NIL record from database (with _id)."""
    _id: Optional[PyObjectId] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

