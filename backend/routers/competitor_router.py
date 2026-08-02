"""
Competitor Research Endpoint Router.
Endpoint: POST /competitors
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.competitor import CompetitorResearchRequest, CompetitorResearchResponse
from backend.services.competitor_service import CompetitorService, get_competitor_service

router = APIRouter(tags=["Competitors"])


@router.post(
    "/competitors",
    response_model=APIResponse[CompetitorResearchResponse],
    status_code=status.HTTP_200_OK,
    summary="Analyze Corporate Competitors",
    description="Identifies direct competitors, resolves missing website URLs automatically via Serper.dev, and returns structured company, country, and competition reason data.",
)
async def analyze_competitors_endpoint(
    request: CompetitorResearchRequest,
    service: CompetitorService = Depends(get_competitor_service),
) -> APIResponse[CompetitorResearchResponse]:
    """POST /competitors async endpoint utilizing dependency injection."""
    result = await service.analyze_competitors(
        target_company=request.company_name,
        competitor_names=request.competitor_names,
    )
    return APIResponse(
        success=True,
        message=f"Competitor analysis completed for '{request.company_name}'.",
        data=result,
    )
