"""
Report Generation Schemas.
Validation models for POST /generate-report request and response payloads.
"""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ReportFormat(str, Enum):
    """Output format for generated reports."""

    MARKDOWN = "markdown"
    HTML = "html"
    JSON = "json"


class ReportRequest(BaseModel):
    """POST /generate-report Request Schema."""

    company_name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="Target company name",
        examples=["Stripe"],
    )
    research_id: Optional[str] = Field(
        default=None,
        description="Associated research task ID if available",
    )
    output_format: ReportFormat = Field(
        default=ReportFormat.MARKDOWN,
        description="Desired output format",
    )
    include_sections: Optional[List[str]] = Field(
        default_factory=lambda: ["executive_summary", "financials", "competitors", "tech_stack"],
        description="Sections to include in the generated report",
    )


class ReportResponse(BaseModel):
    """POST /generate-report Response Schema."""

    report_id: str = Field(..., description="Unique generated report ID")
    company_name: str = Field(..., description="Target company name")
    format: ReportFormat = Field(..., description="Report output format")
    title: str = Field(..., description="Report title")
    content: str = Field(..., description="Full report content in requested format")
    word_count: int = Field(..., description="Report total word count")
    sections_included: List[str] = Field(default_factory=list, description="Included report sections")
    generated_at: str = Field(..., description="Generation timestamp")
