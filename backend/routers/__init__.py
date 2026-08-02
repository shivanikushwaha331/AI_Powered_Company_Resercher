"""
Routers Package.
FastAPI Endpoint Routers.
"""

from backend.routers.health_router import router as health_router
from backend.routers.research_router import router as research_router
from backend.routers.crawl_router import router as crawl_router
from backend.routers.report_router import router as report_router
from backend.routers.pdf_router import router as pdf_router
from backend.routers.discord_router import router as discord_router

__all__ = [
    "health_router",
    "research_router",
    "crawl_router",
    "report_router",
    "pdf_router",
    "discord_router",
]
