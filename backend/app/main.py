"""
FastAPI Entry Point
Setup for routing, middleware, and ML model loading.
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import time

from app.core.config import settings
from app.core.logging import setup_logging, get_logger
from app.api.routes import router
from app.services.prediction_service import prediction_service

setup_logging()
logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup tasks: Load ML model
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")
    try:
        logger.info(f"Loading model from: {settings.model_path.resolve()}")
        prediction_service.load_model()
        logger.info("Model loaded successfully!")
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
    
    yield
    # Shutdown tasks
    logger.info("Service shutting down")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="API for House Price Prediction",
    docs_url="/docs",
    lifespan=lifespan
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Middleware for request/response logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Req: {request.method} {request.url.path}")
    response = await call_next(request)
    duration = time.time() - start_time
    logger.info(f"Res: {response.status_code} ({duration:.3f}s)")
    return response

# Standardized error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "Server Error",
            "message": "Something went wrong",
            "detail": str(exc) if settings.debug else None
        }
    )

app.include_router(router, prefix="/api/v1", tags=["Predictions"])

@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.app_name,
        "status": "active",
        "docs": "/docs",
        "health": "/api/v1/health"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=settings.debug)
