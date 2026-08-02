"""
Company Data Models & Schemas.
Defines company profiles, executive summary, financial data, and technology stack models.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class FinancialMetrics(BaseModel):
    """Company financial overview schema."""

    revenue: Optional[str] = Field(default=None, description="Annual revenue estimate")
    funding_total: Optional[str] = Field(default=None, description="Total venture funding raised")
    valuation: Optional[str] = Field(default=None, description="Latest valuation")
    headcount: Optional[int] = Field(default=None, description="Total employee headcount")


class CompanyProfile(BaseModel):
    """Complete company metadata profile."""

    name: str = Field(..., description="Company legal or trade name")
    domain: Optional[str] = Field(default=None, description="Primary web domain (e.g. stripe.com)")
    website_url: Optional[HttpUrl] = Field(default=None, description="Official website URL")
    industry: Optional[str] = Field(default=None, description="Primary industry vertical")
    description: Optional[str] = Field(default=None, description="Brief company overview")
    headquarters: Optional[str] = Field(default=None, description="Headquarters location")
    founded_year: Optional[int] = Field(default=None, description="Year company was founded")
    financials: Optional[FinancialMetrics] = Field(default=None, description="Key financial metrics")
    key_executives: List[str] = Field(default_factory=list, description="List of notable executives & founders")
    tech_stack: List[str] = Field(default_factory=list, description="Key technologies & frameworks used")
    competitors: List[str] = Field(default_factory=list, description="Primary direct competitors")
