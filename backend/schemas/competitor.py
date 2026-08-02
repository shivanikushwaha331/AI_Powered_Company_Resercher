"""
Competitor Research Data Models & Schemas.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class CompetitorDetail(BaseModel):
    """Structured Competitor Detail Payload."""

    company_name: str = Field(..., description="Competitor company name")
    website: str = Field(..., description="Official website URL")
    country: str = Field(default="United States", description="Headquarters or country of origin")
    reason_for_competition: str = Field(..., description="Detailed reason for market competition")


class CompetitorResearchRequest(BaseModel):
    """POST /competitors Request Schema."""

    company_name: str = Field(..., min_length=1, description="Target company name")
    competitor_names: Optional[List[str]] = Field(
        default=None,
        description="Optional list of raw competitor names to resolve",
    )


class CompetitorResearchResponse(BaseModel):
    """POST /competitors Response Schema."""

    target_company: str = Field(..., description="Target company name")
    competitors: List[CompetitorDetail] = Field(default_factory=list, description="List of structured competitor details")
