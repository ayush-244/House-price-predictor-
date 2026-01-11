"""
API Routes
Handles all incoming web requests for predictions, health checks, and metadata.
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import json
from pathlib import Path

from app.schemas.prediction import (
    HouseFeaturesInput, 
    PredictionResponse, 
    HealthResponse,
    ErrorResponse
)
from app.services.prediction_service import prediction_service
from app.core.logging import get_logger

logger = get_logger(__name__)
router = APIRouter()

@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get House Price Prediction"
)
async def predict_price(features: HouseFeaturesInput):
    """
    Predicts house price using the trained ML model.
    """
    try:
        logger.info(f"Prediction requested for: {features.location}")
        result = prediction_service.predict(features)
        return result
    except ValueError as e:
        logger.error(f"Input error: {e}")
        raise HTTPException(
            status_code=400,
            detail={"error": "Invalid Data", "message": str(e)}
        )
    except Exception as e:
        logger.error(f"Prediction failed: {e}")
        raise HTTPException(
            status_code=500,
            detail={"error": "Server Error", "message": "Could not complete prediction"}
        )

@router.get("/health", response_model=HealthResponse, summary="Check Service Health")
async def health_check():
    """
    Returns service health and model status.
    """
    try:
        model_info = prediction_service.get_model_info()
        return {
            "status": "healthy",
            "model_loaded": model_info.get("model_loaded", False),
            "model_name": model_info.get("model_name"),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return {"status": "unhealthy", "model_loaded": False}

@router.get("/model-info", summary="Get model metadata")
async def get_model_info():
    """
    Returns detailed information about the loaded model.
    """
    try:
        return prediction_service.get_model_info()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/options", response_model=dict, summary="Get dynamic form options")
async def get_form_options():
    """
    Serves states, cities, and property types for the frontend dropdowns.
    """
    try:
        mapping_path = Path(__file__).parent.parent / "data" / "location_mapping.json"
        
        if mapping_path.exists():
            with open(mapping_path, 'r') as f:
                location_mapping = json.load(f)
        else:
            location_mapping = {}
            
        return {
            "locations": location_mapping,
            "property_types": ["Apartment", "Independent House", "Villa"]
        }
    except Exception as e:
        logger.error(f"Failed to fetch options: {e}")
        return {"locations": {}, "property_types": []}
