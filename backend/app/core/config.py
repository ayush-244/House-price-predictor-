"""
Application Configuration
Loads settings for the API, CORS, and ML model paths.
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List

class Settings(BaseSettings):
    # App Identity
    app_name: str = "House Price Prediction API"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Authorized origins for frontend
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Path resolution for ML artifacts
    base_dir: Path = Path(__file__).parent.parent.parent.parent
    model_path: Path = base_dir / "ml" / "models" / "best_model.joblib"
    scaler_path: Path = base_dir / "ml" / "models" / "scaler.joblib"
    encoder_path: Path = base_dir / "ml" / "models" / "encoder.joblib"
    feature_names_path: Path = base_dir / "ml" / "models" / "feature_names.joblib"
    metadata_path: Path = base_dir / "ml" / "models" / "model_metadata.joblib"
    
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()
