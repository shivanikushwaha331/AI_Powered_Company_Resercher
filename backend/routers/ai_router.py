"""
OpenRouter AI Endpoint Router.
Endpoints:
- POST /ai/generate
- POST /ai/stream
- GET  /ai/models
"""

from typing import List
from fastapi import APIRouter, Depends, status
from fastapi.responses import StreamingResponse

from backend.config.settings import settings
from backend.schemas.ai import AIGenerateRequest, AIStructuredReport
from backend.schemas.common import APIResponse
from backend.services.ai_service import AIService, get_ai_service

router = APIRouter(tags=["OpenRouter AI"])


@router.get(
    "/ai/models",
    response_model=APIResponse[List[str]],
    summary="Get Available OpenRouter Models",
    description="Returns list of supported OpenRouter LLM models for selection in the frontend.",
)
async def get_available_models() -> APIResponse[List[str]]:
    """GET /ai/models endpoint."""
    return APIResponse(
        success=True,
        message="Available OpenRouter models retrieved.",
        data=settings.AVAILABLE_OPENROUTER_MODELS,
    )


@router.post(
    "/ai/generate",
    response_model=APIResponse[AIStructuredReport],
    status_code=status.HTTP_200_OK,
    summary="Generate 8-Part Structured AI Research Report",
    description="Sends crawled web content to OpenRouter LLM and returns structured JSON (Company Summary, Products, Services, Pain Points, Business Model, Target Customers, SWOT Analysis, Competitors).",
)
async def generate_ai_report(
    request: AIGenerateRequest,
    service: AIService = Depends(get_ai_service),
) -> APIResponse[AIStructuredReport]:
    """POST /ai/generate async endpoint utilizing dependency injection."""
    result = await service.generate_structured_report(
        company_name=request.company_name,
        crawled_content=request.crawled_content,
        model=request.model,
    )
    return APIResponse(
        success=True,
        message=f"Structured AI report generated using model [{result.selected_model}].",
        data=result,
    )


@router.post(
    "/ai/stream",
    summary="Stream Real-time LLM Synthesis Progress via SSE",
    description="Streams real-time token chunks and progress events over Server-Sent Events (SSE).",
)
async def stream_ai_report(
    request: AIGenerateRequest,
    service: AIService = Depends(get_ai_service),
):
    """POST /ai/stream SSE streaming endpoint."""
    generator = service.stream_report_generation(
        company_name=request.company_name,
        crawled_content=request.crawled_content,
        model=request.model,
    )
    return StreamingResponse(generator, media_type="text/event-stream")
