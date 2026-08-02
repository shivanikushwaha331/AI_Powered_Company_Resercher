"""
PDF Generation Endpoint Router.
Endpoints:
- POST /generate-pdf
- GET  /downloads/pdf/{pdf_id}
"""

import os
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse

from backend.schemas.common import APIResponse
from backend.schemas.pdf import PDFRequest, PDFResponse
from backend.services.pdf_service import PDFService, get_pdf_service

router = APIRouter(tags=["PDF"])


@router.post(
    "/generate-pdf",
    response_model=APIResponse[PDFResponse],
    status_code=status.HTTP_200_OK,
    summary="Export Research Report to PDF",
    description="Compiles research content into a ReportLab PDF document with Cover Page, Company Info, Summary, Products, Services, Pain Points, SWOT Matrix, Competitors, and Numbered Canvas footers.",
)
async def generate_pdf_endpoint(
    request: PDFRequest,
    service: PDFService = Depends(get_pdf_service),
) -> APIResponse[PDFResponse]:
    """POST /generate-pdf async endpoint utilizing dependency injection."""
    result = await service.generate_pdf(request)
    return APIResponse(
        success=True,
        message=f"PDF document '{result.file_name}' generated successfully.",
        data=result,
    )


@router.get(
    "/downloads/pdf/{pdf_id}",
    summary="Download Compiled PDF Document",
    description="Serves binary PDF file for direct browser downloading.",
)
async def download_pdf_endpoint(
    pdf_id: str,
    service: PDFService = Depends(get_pdf_service),
):
    """GET /downloads/pdf/{pdf_id} file download route."""
    file_path = service.get_pdf_file_path(pdf_id)
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"PDF report document with ID '{pdf_id}' was not found.",
        )

    file_name = os.path.basename(file_path)
    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename=file_name,
    )
