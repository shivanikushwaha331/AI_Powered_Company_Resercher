"""
Health Check Endpoint Router.
Provides system diagnostic health check.
"""

from fastapi import APIRouter
from app.core.config import settings
from app.schemas.common import HealthCheckResponse

router = APIRouter()


@router.get("/health", response_model=HealthCheckResponse, summary="System Health Check")
async def health_check() -> HealthCheckResponse:
    """Returns application health status, version, and environment details."""
    return HealthCheckResponse(
        status="healthy",
        app_name=settings.APP_NAME,
        environment=settings.APP_ENV,
        version="0.1.0",
    )
