"""
Common Schemas & API Response Wrappers.
"""

from typing import Generic, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class APIResponse(BaseModel, Generic[DataT]):
    """Standardized API Response Wrapper."""

    success: bool = Field(default=True, description="Indicates request success")
    message: str = Field(default="Operation completed successfully", description="Status message")
    data: Optional[DataT] = Field(default=None, description="Response payload data")


class HealthCheckResponse(BaseModel):
    """Health check response payload model."""

    status: str = Field(default="healthy", description="System health status")
    app_name: str = Field(..., description="Application name")
    environment: str = Field(..., description="Runtime environment")
    version: str = Field(default="0.1.0", description="Application version")
    timestamp: str = Field(..., description="ISO UTC timestamp")
