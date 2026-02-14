"""
Logging Setup
Configures how the app records events to the console and files.
"""
import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging():
    # Setup log storage
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # Define how log entries look
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # Initialize basic logging configuration
    logging.basicConfig(
        level=getattr(logging, settings.log_level),
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(log_dir / "app.log")
        ]
    )
    
    # Reduce noise from external libraries
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.WARNING)

def get_logger(name: str) -> logging.Logger:
    # Returns a named logger instance
    return logging.getLogger(name)
