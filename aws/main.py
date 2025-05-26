from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from dotenv import load_dotenv

from aws.config import get_settings
from aws.api.v1.endpoints import costs

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize settings
settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    debug=settings.DEBUG
)

# Add error handling
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global error handler caught: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )

# Include routers
app.include_router(
    costs.router,
    prefix=f"{settings.API_V1_STR}/costs",
    tags=["costs"]
)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}