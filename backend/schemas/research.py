"""
Research Schemas.
Validation models for POST /research request and response payloads.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ResearchDepth(str, Enum):
    """Depth level for company research."""

    QUICK = "quick"
    STANDARD = "standard"
    DEEP = "deep"


class ResearchRequest(BaseModel):
    """POST /research Request Schema."""

    company_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Target company name or web domain (e.g. Stripe, OpenAI)",
        examples=["Stripe"],
    )
    depth: ResearchDepth = Field(
        default=ResearchDepth.STANDARD,
        description="Research depth level",
    )
    focus_areas: Optional[List[str]] = Field(
        default=None,
        description="Optional list of specific focus topics (e.g. ['financials', 'competitors'])",
        examples=[["financials", "tech_stack"]],
    )


class ResearchSource(BaseModel):
    """Cited research reference source."""

    title: str = Field(..., description="Source page title")
    url: str = Field(..., description="Source web link")
    snippet: str = Field(..., description="Excerpt snippet")


class CompanyOverview(BaseModel):
    """Structured company overview profile."""

    name: str = Field(..., description="Company name")
    domain: str = Field(..., description="Primary domain")
    industry: str = Field(..., description="Industry vertical")
    headquarters: str = Field(..., description="HQ Location")
    employee_count: str = Field(..., description="Estimated headcount")
    tech_stack: List[str] = Field(default_factory=list, description="Primary technologies")


class ResearchResponse(BaseModel):
    """POST /research Response Schema."""

    research_id: str = Field(..., description="Unique research task ID")
    company_name: str = Field(..., description="Target company name")
    status: str = Field(default="completed", description="Task status")
    depth: ResearchDepth = Field(..., description="Applied research depth")
    company_profile: CompanyOverview = Field(..., description="Extracted company profile")
    executive_summary: str = Field(..., description="Markdown executive summary")
    key_findings: List[str] = Field(default_factory=list, description="List of key findings")
    sources: List[ResearchSource] = Field(default_factory=list, description="Citations")
    created_at: str = Field(..., description="Task completion timestamp")
