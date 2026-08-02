"""
Web Crawling Endpoint Router.
Endpoint: POST /crawl
"""

from fastapi import APIRouter, Depends, status
from backend.schemas.common import APIResponse
from backend.schemas.crawl import CrawlRequest, CrawlResponse
from backend.services.crawl_service import CrawlService, get_crawl_service
from backend.utils.logger import logger

router = APIRouter(tags=["Crawl"])


@router.post(
    "/crawl",
    response_model=APIResponse[CrawlResponse],
    status_code=status.HTTP_200_OK,
    summary="Crawl Target Website",
    description="Crawls a target website URL starting from homepage. Automatically discovers About, Products, Services, Pricing, and Contact pages while filtering out Login, Signup, Cart, Privacy, Terms, and duplicates.",
)
async def create_crawl_job(
    request: CrawlRequest,
    service: CrawlService = Depends(get_crawl_service),
) -> APIResponse[CrawlResponse]:
    """POST /crawl async endpoint utilizing dependency injection and progress reporting."""

    def log_progress(step: int, total: int, current_url: str, message: str):
        logger.info(f"[Crawl Progress {step}/{total}] {message}")

    result = await service.execute_crawl(request, on_progress=log_progress)
    return APIResponse(
        success=True,
        message=f"Website crawl for '{request.url}' successfully completed ({result.pages_crawled} pages extracted).",
        data=result,
    )
