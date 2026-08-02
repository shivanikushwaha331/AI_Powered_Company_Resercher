"""
Custom Exceptions & Global Exception Handlers Module.
Defines domain errors and registers custom FastAPI exception middleware handlers.
"""

from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.logging import logger


class BaseAppException(Exception):
    """Base application exception."""

    def __init__(self, message: str, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ResearchTaskError(BaseAppException):
    """Raised when research execution encounters a failure."""

    def __init__(self, message: str):
        super().__init__(message=message, status_code=status.HTTP_502_BAD_GATEWAY)


class CompanyNotFoundError(BaseAppException):
    """Raised when company metadata cannot be located."""

    def __init__(self, company_name: str):
        super().__init__(
            message=f"Company '{company_name}' not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler fallback for uncaught errors."""
    logger.error(f"Unhandled error processing request {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred. Please try again later."},
    )


async def custom_app_exception_handler(request: Request, exc: BaseAppException) -> JSONResponse:
    """Handler for application domain exceptions."""
    logger.warning(f"Domain error processing request {request.url}: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message},
    )
