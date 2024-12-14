from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import start_http_server
import uvicorn
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Import routes and services
from .api.routes import router as api_router
from .core.monitoring import MonitoringService
from .services.model_service import ModelService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.getenv('LOG_FILE', 'app.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="LLM Ops Demo",
    description="A demonstration of LLM Operations including model serving, monitoring, and logging",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
monitoring_service = MonitoringService()
model_service = ModelService()

# Include API routes
app.include_router(api_router, prefix="/api")

@app.on_event("startup")
async def startup_event():
    """
    Initialize services and start monitoring on application startup
    """
    try:
        # Start Prometheus metrics server if enabled
        if os.getenv('ENABLE_PROMETHEUS', 'True').lower() == 'true':
            prometheus_port = int(os.getenv('PROMETHEUS_PORT', 9090))
            start_http_server(prometheus_port)
            logger.info(f"Prometheus metrics server started on port {prometheus_port}")

        # Log startup
        logger.info("LLM Ops Demo application started successfully")
        
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """
    Cleanup resources on application shutdown
    """
    try:
        logger.info("Shutting down LLM Ops Demo application")
        # Add any cleanup code here
        
    except Exception as e:
        logger.error(f"Error during shutdown: {str(e)}")
        raise

@app.get("/")
async def root():
    """
    Root endpoint returning basic API information
    """
    return {
        "name": "LLM Ops Demo API",
        "version": "1.0.0",
        "status": "active",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    try:
        # Check model service health
        model_health = model_service.health_check()
        
        # Get system metrics
        system_metrics = monitoring_service.get_system_metrics()
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "model_status": model_health,
            "system_metrics": system_metrics
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(
            status_code=503,
            detail="Service unhealthy"
        )

if __name__ == "__main__":
    # Get configuration from environment variables
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 8000))
    debug = os.getenv('DEBUG', 'False').lower() == 'true'
    
    # Run the application
    uvicorn.run(
        "main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info" if debug else "error"
    )
