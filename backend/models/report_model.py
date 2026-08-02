"""
Report Domain Model.
Represents a generated report entity.
"""

from pydantic import BaseModel, Field
from backend.utils.helpers import generate_task_id, get_current_utc_timestamp


class ReportModel(BaseModel):
    """Domain model for a Report entity."""

    id: str = Field(default_factory=lambda: generate_task_id("rep"))
    company_name: str
    format: str = "markdown"
    title: str
    content: str
    created_at: str = Field(default_factory=get_current_utc_timestamp)
