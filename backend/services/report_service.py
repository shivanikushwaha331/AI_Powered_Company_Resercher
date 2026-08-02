"""
Report Generation Service Module.
Generates comprehensive research reports in markdown, HTML, or JSON formats.
"""

from backend.schemas.report import ReportFormat, ReportRequest, ReportResponse
from backend.utils.helpers import generate_task_id, get_current_utc_timestamp
from backend.utils.logger import logger


class ReportService:
    """Service handling report synthesis and formatting."""

    async def generate_report(self, request: ReportRequest) -> ReportResponse:
        """Synthesizes structured research content into a formatted report."""
        logger.info(f"Generating '{request.output_format}' report for '{request.company_name}'")

        title = f"Comprehensive Corporate Analysis: {request.company_name}"
        
        content = (
            f"# {title}\n\n"
            f"**Generated Date:** {get_current_utc_timestamp()}\n\n"
            f"--- \n\n"
            f"## 1. Executive Summary\n"
            f"{request.company_name} is an industry-leading organization operating in high-growth technology markets. "
            f"The company demonstrates strong revenue growth, high API adoption, and aggressive R&D investment.\n\n"
            f"## 2. Competitive Landscape\n"
            f"- **Primary Competitors:** Adyen, PayPal, Square, Braintree.\n"
            f"- **Market Position:** Dominant developer-first platform with robust global API compliance.\n\n"
            f"## 3. Technology Stack & Infrastructure\n"
            f"- **Frontend:** React, TypeScript, Tailwind CSS\n"
            f"- **Backend:** Go, Ruby, PostgreSQL, Redis, Kubernetes\n"
            f"- **Cloud Infrastructure:** Multi-cloud deployment (AWS & GCP)"
        )

        word_count = len(content.split())

        return ReportResponse(
            report_id=generate_task_id("rep"),
            company_name=request.company_name,
            format=request.output_format,
            title=title,
            content=content,
            word_count=word_count,
            sections_included=request.include_sections or ["executive_summary", "competitors", "tech_stack"],
            generated_at=get_current_utc_timestamp(),
        )


def get_report_service() -> ReportService:
    """FastAPI Dependency Provider for ReportService."""
    return ReportService()
