"""
Health Check Router.
Endpoint: GET /health
"""

from fastapi import APIRouter, status
from backend.config.settings import settings
from backend.schemas.common import HealthCheckResponse
from backend.utils.helpers import get_current_utc_timestamp

router = APIRouter(tags=["Health"])


@router.get(
    "/health",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="System Health Diagnostic Check",
    description="Returns API service health status, application metadata, and server timestamp.",
)
async def health_check() -> HealthCheckResponse:
    """GET /health endpoint."""
    return HealthCheckResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        version="0.1.0",
        timestamp=get_current_utc_timestamp(),
    )
