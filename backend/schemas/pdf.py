"""
PDF Export Schemas.
Validation models for POST /generate-pdf request and response payloads.
"""

from typing import Optional
from pydantic import BaseModel, Field


class PDFRequest(BaseModel):
    """POST /generate-pdf Request Schema."""

    report_id: Optional[str] = Field(
        default=None,
        description="Associated report ID to export to PDF",
    )
    content: Optional[str] = Field(
        default=None,
        description="Raw markdown/HTML content to convert if report_id is not provided",
    )
    title: str = Field(
        default="Company Research Report",
        min_length=1,
        max_length=255,
        description="Title for the PDF cover page",
    )
    include_header_footer: bool = Field(
        default=True,
        description="Whether to include page numbers and headers",
    )


class PDFResponse(BaseModel):
    """POST /generate-pdf Response Schema."""

    pdf_id: str = Field(..., description="Unique PDF document ID")
    file_name: str = Field(..., description="Generated PDF file name")
    file_size_bytes: int = Field(..., description="File size in bytes")
    download_url: str = Field(..., description="Download link URL for the PDF document")
    expires_at: str = Field(..., description="URL expiration timestamp")
    created_at: str = Field(..., description="Generation timestamp")
