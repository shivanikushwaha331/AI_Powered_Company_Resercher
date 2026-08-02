"""
OpenRouter AI Synthesis Schemas.
Validation models for structured 8-part LLM research reports.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class SWOTAnalysis(BaseModel):
    """SWOT Analysis 4-Quadrant Data Model."""

    strengths: List[str] = Field(default_factory=list, description="Internal strengths & competitive advantages")
    weaknesses: List[str] = Field(default_factory=list, description="Internal weaknesses & vulnerabilities")
    opportunities: List[str] = Field(default_factory=list, description="External market growth opportunities")
    threats: List[str] = Field(default_factory=list, description="External competitive threats & risks")


class AIStructuredReport(BaseModel):
    """Structured 8-part JSON report schema extracted by OpenRouter LLM."""

    company_summary: str = Field(..., description="Executive summary overview of the company")
    products: List[str] = Field(default_factory=list, description="Key products & software platforms")
    services: List[str] = Field(default_factory=list, description="Professional & managed services offered")
    pain_points: List[str] = Field(default_factory=list, description="Key customer pain points and problems solved")
    business_model: str = Field(..., description="Revenue model & monetization strategy")
    target_customers: List[str] = Field(default_factory=list, description="Ideal customer profiles & target markets")
    swot_analysis: SWOTAnalysis = Field(..., description="4-quadrant SWOT analysis")
    competitor_suggestions: List[str] = Field(default_factory=list, description="Primary direct & indirect competitors")
    selected_model: Optional[str] = Field(default=None, description="OpenRouter LLM model used for synthesis")


class AIGenerateRequest(BaseModel):
    """POST /ai/generate Request Schema."""

    company_name: str = Field(..., min_length=1, description="Company name or domain")
    crawled_content: str = Field(..., min_length=1, description="Extracted web page text content")
    model: Optional[str] = Field(default=None, description="OpenRouter model name (e.g. google/gemini-2.5-flash)")
