"""
Serper Search Endpoint Router.
Endpoint: POST /serper/search
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.serper import CompanyExtractedData
from backend.services.serper_service import SerperService, get_serper_service
from pydantic import BaseModel, Field

router = APIRouter(tags=["Serper Search"])


class SerperSearchRequest(BaseModel):
    query: str = Field(..., min_length=1, description="Company name (e.g. Microsoft, Tesla, Stripe) or direct URL (e.g. https://stripe.com)")


@router.post(
    "/serper/search",
    response_model=APIResponse[CompanyExtractedData],
    status_code=status.HTTP_200_OK,
    summary="Search Serper.dev for Company Knowledge & Official Website",
    description="Queries Serper.dev for company official website, phone, address, description, and industry, or parses directly if URL input.",
)
async def serper_company_search(
    request: SerperSearchRequest,
    service: SerperService = Depends(get_serper_service),
) -> APIResponse[CompanyExtractedData]:
    """POST /serper/search endpoint."""
    result = await service.extract_company_info(request.query)
    return APIResponse(
        success=True,
        message=f"Company metadata extracted for '{request.query}'.",
        data=result,
    )
