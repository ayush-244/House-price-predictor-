"""
Data Schemas
Pydantic models for verifying input and formatting output.
"""
from pydantic import BaseModel, Field, validator
from typing import Optional, Dict

class HouseFeaturesInput(BaseModel):
    # Core house details
    area: float = Field(..., gt=0, description="Square footage")
    bedrooms: int = Field(..., ge=0, le=20, description="No. of bedrooms")
    bathrooms: float = Field(..., ge=0, le=20, description="No. of bathrooms")
    location: str = Field(..., min_length=1, description="City/Neighborhood")
    year_built: int = Field(..., ge=1800, le=2030, description="Built year")
    
    # Modern features
    state: str = Field(..., min_length=1, description="State name")
    property_type: str = Field(..., description="House categorization")
    parking: int = Field(0, description="1 if parking is available")
    modular_kitchen: int = Field(0, description="1 if kitchen is upgraded")
    dining_hall: int = Field(0, description="1 if separate dining exists")
    
    @validator('area')
    def validate_area(cls, v):
        """Prevents unrealistic size inputs."""
        if v > 100000:
            raise ValueError('Area exceeds limit (100k sqft)')
        return v
    
    @validator('location', 'state', 'property_type')
    def validate_strings(cls, v):
        """Simple text cleanup."""
        return v.strip().title()

class PredictionResponse(BaseModel):
    # Output format for the API
    predicted_price: float
    model_used: str
    confidence_interval: Optional[Dict[str, float]] = None
    input_features: HouseFeaturesInput

class HealthResponse(BaseModel):
    # System status response
    status: str
    model_loaded: bool
    model_name: Optional[str] = None
    timestamp: str

class ErrorResponse(BaseModel):
    # Clean error format
    error: str
    message: str
    detail: Optional[str] = None
