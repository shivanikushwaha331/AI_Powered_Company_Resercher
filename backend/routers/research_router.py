"""
Research Endpoint Router.
Endpoint: POST /research
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.research import ResearchRequest, ResearchResponse
from backend.services.research_service import ResearchService, get_research_service

router = APIRouter(tags=["Research"])


@router.post(
    "/research",
    response_model=APIResponse[ResearchResponse],
    status_code=status.HTTP_200_OK,
    summary="Execute Company Research Task",
    description="Accepts target company query parameters and returns structured research report payload.",
)
async def create_research_task(
    request: ResearchRequest,
    service: ResearchService = Depends(get_research_service),
) -> APIResponse[ResearchResponse]:
    """POST /research async endpoint utilizing dependency injection."""
    result = await service.execute_research(request)
    return APIResponse(
        success=True,
        message=f"Research task for '{request.company_name}' successfully executed.",
        data=result,
    )
