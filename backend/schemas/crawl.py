"""
Web Crawl Schemas.
Validation models for POST /crawl request and response payloads.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl


class CrawlRequest(BaseModel):
    """POST /crawl Request Schema."""

    url: str = Field(
        ...,
        description="Target website URL to crawl (e.g. https://stripe.com or stripe.com)",
        examples=["https://stripe.com"],
    )
    max_pages: int = Field(
        default=5,
        ge=1,
        le=50,
        description="Maximum pages to crawl (1-50)",
    )
    extract_technologies: bool = Field(
        default=True,
        description="Whether to extract technology stack signals",
    )


class ExtractedPage(BaseModel):
    """Details of an extracted webpage."""

    url: str = Field(..., description="Page URL")
    page_type: str = Field(default="general", description="Categorized page type (homepage, about, products, services, pricing, contact)")
    title: str = Field(..., description="Page title")
    status_code: int = Field(default=200, description="HTTP status code")
    content_length: int = Field(..., description="Extracted content byte length")
    headings: List[str] = Field(default_factory=list, description="Extracted H1/H2 headings")
    clean_text: str = Field(default="", description="Cleaned, meaningful body text extracted from HTML")
    word_count: int = Field(default=0, description="Clean text word count")


class CrawlProgressUpdate(BaseModel):
    """Progress event during crawling execution."""

    step: int = Field(..., description="Current step index")
    total_steps: int = Field(..., description="Total estimated steps")
    current_url: str = Field(..., description="URL currently being processed")
    message: str = Field(..., description="Readable status description")


class CrawlResponse(BaseModel):
    """POST /crawl Response Schema."""

    crawl_id: str = Field(..., description="Unique crawl job ID")
    target_url: str = Field(..., description="Target website homepage URL")
    pages_crawled: int = Field(..., description="Total pages successfully crawled")
    crawler_engine: str = Field(default="Crawl4AI / BeautifulSoup", description="Active crawler engine used")
    extracted_pages: List[ExtractedPage] = Field(default_factory=list, description="Extracted page metadata")
    detected_technologies: List[str] = Field(default_factory=list, description="Detected frameworks & tools")
    completed_at: str = Field(..., description="Completion timestamp")
