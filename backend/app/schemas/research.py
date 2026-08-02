"""
Research Request and Response Schemas.
Models for research requests, multi-step analysis results, and research stream events.
"""

from enum import Enum
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.company import CompanyProfile


class ResearchDepth(str, Enum):
    """Depth level for company research."""

    QUICK = "quick"         # Fast summary using primary web sources
    STANDARD = "standard"   # Deep dive into company background, products, & financials
    DEEP = "deep"           # Comprehensive analysis including SWOT, competitors & market news


class ResearchRequest(BaseModel):
    """Research trigger payload."""

    company_name: str = Field(..., min_length=1, description="Target company name or domain")
    depth: ResearchDepth = Field(default=ResearchDepth.STANDARD, description="Research analysis depth")
    specific_focus: Optional[List[str]] = Field(
        default=None,
        description="Optional list of specific focus topics (e.g., ['financials', 'competitors'])",
    )


class SearchSource(BaseModel):
    """Reference citation source."""

    title: str = Field(..., description="Source page title")
    url: str = Field(..., description="Source web link")
    snippet: Optional[str] = Field(default=None, description="Relevant text snippet")


class ResearchResult(BaseModel):
    """Structured research synthesis output payload."""

    task_id: str = Field(..., description="Unique research task identifier")
    company_name: str = Field(..., description="Target company name")
    profile: Optional[CompanyProfile] = Field(default=None, description="Extracted company profile")
    summary: str = Field(..., description="Synthesized executive markdown summary")
    key_takeaways: List[str] = Field(default_factory=list, description="Bullet points of key findings")
    sources: List[SearchSource] = Field(default_factory=list, description="Citations and references")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Completion timestamp")
