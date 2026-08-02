"""
Report Generation Endpoint Router.
Endpoint: POST /generate-report
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.report import ReportRequest, ReportResponse
from backend.services.report_service import ReportService, get_report_service

router = APIRouter(tags=["Report"])


@router.post(
    "/generate-report",
    response_model=APIResponse[ReportResponse],
    status_code=status.HTTP_200_OK,
    summary="Generate Research Report",
    description="Synthesizes company research data into a formatted report (Markdown, HTML, or JSON).",
)
async def generate_report_endpoint(
    request: ReportRequest,
    service: ReportService = Depends(get_report_service),
) -> APIResponse[ReportResponse]:
    """POST /generate-report async endpoint utilizing dependency injection."""
    result = await service.generate_report(request)
    return APIResponse(
        success=True,
        message=f"Report generated successfully in '{request.output_format}' format.",
        data=result,
    )
