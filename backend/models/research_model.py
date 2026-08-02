"""
Research Task Domain Model.
Represents a company research record in application domain memory/storage.
"""

from typing import List, Optional
from pydantic import BaseModel, Field
from backend.utils.helpers import generate_task_id, get_current_utc_timestamp


class ResearchTaskModel(BaseModel):
    """Domain model for a Research Task entity."""

    id: str = Field(default_factory=lambda: generate_task_id("res"))
    company_name: str
    depth: str = "standard"
    status: str = "completed"
    created_at: str = Field(default_factory=get_current_utc_timestamp)
    updated_at: str = Field(default_factory=get_current_utc_timestamp)
    tags: List[str] = Field(default_factory=list)
