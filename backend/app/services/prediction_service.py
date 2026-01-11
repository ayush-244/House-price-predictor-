"""
Prediction Service
Contains the logic for loading the ML model and running inference.
"""
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from typing import Dict, Optional
from datetime import datetime

from app.core.config import settings
from app.core.logging import get_logger
from app.schemas.prediction import HouseFeaturesInput

logger = get_logger(__name__)

class PredictionService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.encoders = None
        self.feature_names = None
        self.metadata = None
        self.model_loaded = False
        
    def load_model(self):
        """Loads all ML artifacts into memory."""
        try:
            if not settings.model_path.exists():
                raise FileNotFoundError(f"Model file missing at {settings.model_path}")
            
            self.model = joblib.load(settings.model_path)
            self.scaler = joblib.load(settings.scaler_path)
            self.encoders = joblib.load(settings.encoder_path)
            self.feature_names = joblib.load(settings.feature_names_path)
            
            if settings.metadata_path.exists():
                self.metadata = joblib.load(settings.metadata_path)
            
            self.model_loaded = True
            logger.info("Successfully loaded all ML components.")
        except Exception as e:
            logger.error(f"Error loading model artifacts: {e}")
            self.model_loaded = False
            raise
    
    def preprocess_input(self, features: HouseFeaturesInput) -> np.ndarray:
        """Transforms raw input data into ML-ready numerical format."""
        try:
            data = {
                'area': [features.area],
                'bedrooms': [features.bedrooms],
                'bathrooms': [features.bathrooms],
                'location': [features.location],
                'year_built': [features.year_built],
                'state': [features.state],
                'property_type': [features.property_type],
                'parking': [features.parking],
                'modular_kitchen': [features.modular_kitchen],
                'dining_hall': [features.dining_hall]
            }
            df = pd.DataFrame(data)
            
            # Label encoding for categorical fields
            for col, encoder in self.encoders.items():
                if col in df.columns:
                    try:
                        df[col] = encoder.transform(df[col])
                    except ValueError:
                        # Fallback for unseen labels
                        safe_class = encoder.classes_[0]
                        df[col] = df[col].apply(lambda x: x if x in encoder.classes_ else safe_class)
                        df[col] = encoder.transform(df[col])
            
            # Align features and scale
            df = df[self.feature_names]
            return self.scaler.transform(df)
        except Exception as e:
            logger.error(f"Preprocessing failed: {e}")
            raise
    
    def predict(self, features: HouseFeaturesInput) -> Dict:
        """Generates a price prediction with confidence intervals."""
        if not self.model_loaded:
            raise RuntimeError("ML model is not loaded!")
        
        try:
            X = self.preprocess_input(features)
            prediction = self.model.predict(X)[0]
            
            # Calculate a simplified 5% confidence margin
            margin = prediction * 0.05
            
            return {
                "predicted_price": float(prediction),
                "model_used": "Random Forest Pro",
                "confidence_interval": {
                    "lower": float(prediction - margin),
                    "upper": float(prediction + margin)
                },
                "input_features": features
            }
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise
    
    def get_model_info(self) -> Dict:
        """Returns metadata about the currently loaded model."""
        if not self.model_loaded:
            return {"model_loaded": False}
        
        return {
            "model_loaded": True,
            "accuracy": self.metadata.get('accuracy') if self.metadata else "N/A",
            "features": self.feature_names
        }

# Singleton instance for the app
prediction_service = PredictionService()
