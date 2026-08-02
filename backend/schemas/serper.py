"""
Serper.dev Search & Company Extraction Schemas.
"""

from typing import Optional
from pydantic import BaseModel, Field


class CompanyExtractedData(BaseModel):
    """Structured company data extracted from Serper.dev or direct URL parsing."""

    company_name: str = Field(..., description="Official company name")
    official_website: str = Field(..., description="Official website URL")
    phone: Optional[str] = Field(default=None, description="Contact phone number")
    address: Optional[str] = Field(default=None, description="Headquarters or physical address")
    description: str = Field(..., description="Overview or company summary snippet")
    industry: str = Field(default="Technology", description="Industry classification")
    is_direct_url: bool = Field(default=False, description="Flag indicating if search was skipped due to direct URL input")
