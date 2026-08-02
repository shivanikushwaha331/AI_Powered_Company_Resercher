"""
Common API Schemas.
Standardized response wrappers, pagination, and status payloads.
"""

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    """Generic API Response Wrapper."""

    success: bool = Field(default=True, description="Indicates if request was successful")
    message: str = Field(default="Operation completed successfully", description="Status or summary message")
    data: Optional[DataT] = Field(default=None, description="Payload data")


class HealthCheckResponse(BaseModel):
    """Health check endpoint status schema."""

    status: str = Field(default="healthy", description="Application health status")
    app_name: str = Field(..., description="Application name")
    environment: str = Field(..., description="Active environment name")
    version: str = Field(default="0.1.0", description="Application version")
