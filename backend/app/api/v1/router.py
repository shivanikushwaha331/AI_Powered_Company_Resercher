"""
API v1 Router Aggregator.
Combines health check, research endpoints, and company profile routers.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import company, health, research

api_v1_router = APIRouter()

# Include endpoint sub-routers
api_v1_router.include_router(health.router, tags=["Health Checks"])
api_v1_router.include_router(research.router, tags=["Research Operations"])
api_v1_router.include_router(company.router, tags=["Company Profiles"])
