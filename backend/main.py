"""
FastAPI Application Entrypoint.
Initializes the FastAPI application, CORS middleware, global exception handlers, and includes all routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config.settings import settings
from backend.routers import (
    crawl_router,
    discord_router,
    health_router,
    pdf_router,
    report_router,
    research_router,
)
from backend.routers.serper_router import router as serper_router
from backend.routers.ai_router import router as ai_router
from backend.routers.competitor_router import router as competitor_router
from backend.utils.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for startup and shutdown."""
    logger.info(f"Starting {settings.APP_NAME} in [{settings.APP_ENV}] mode (Mock Mode: {settings.MOCK_MODE})...")
    yield
    logger.info(f"Shutting down {settings.APP_NAME}...")


def create_app() -> FastAPI:
    """FastAPI Application Factory."""
    app = FastAPI(
        title=settings.APP_NAME,
        description="Production-grade AI Company Research Assistant REST API",
        version="0.1.0",
        debug=settings.DEBUG,
        lifespan=lifespan,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS Middleware Setup
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Global Exception Handler
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.error(f"Unhandled server error on {request.url}: {str(exc)}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "success": False,
                "message": "Internal server error occurred.",
                "data": None,
            },
        )

    # Include API Routers
    app.include_router(health_router)
    app.include_router(research_router)
    app.include_router(serper_router)
    app.include_router(ai_router)
    app.include_router(competitor_router)
    app.include_router(crawl_router)
    app.include_router(report_router)
    app.include_router(pdf_router)
    app.include_router(discord_router)

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
