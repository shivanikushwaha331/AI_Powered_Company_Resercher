"""
Research Endpoints Router.
Provides REST endpoints for initiating company research tasks and streaming SSE responses.
"""

from fastapi import APIRouter, status
from fastapi.responses import StreamingResponse
from app.schemas.common import APIResponse
from app.schemas.research import ResearchRequest, ResearchResult

router = APIRouter()


@router.post(
    "/research",
    response_model=APIResponse[ResearchResult],
    status_code=status.HTTP_200_OK,
    summary="Initiate Company Research Task",
)
async def create_research_task(request: ResearchRequest):
    """Executes research workflow for specified company and returns report payload."""
    # Skeleton route endpoint
    return APIResponse(
        success=True,
        message=f"Research task initialized for {request.company_name}",
        data=None,
    )


@router.post(
    "/research/stream",
    summary="Stream Real-time Company Research Progress",
)
async def stream_research_task(request: ResearchRequest):
    """Streams real-time research synthesis progress over Server-Sent Events (SSE)."""

    async def dummy_generator():
        yield f"data: {{\"status\": \"initialized\", \"company\": \"{request.company_name}\"}}\n\n"

    return StreamingResponse(dummy_generator(), media_type="text/event-stream")
