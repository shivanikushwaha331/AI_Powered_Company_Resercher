"""
Company Metadata Endpoints Router.
Provides company lookup, structured metadata profiles, and search operations.
"""

from fastapi import APIRouter, status
from app.schemas.common import APIResponse
from app.schemas.company import CompanyProfile

router = APIRouter()


@router.get(
    "/company/{company_name}",
    response_model=APIResponse[CompanyProfile],
    status_code=status.HTTP_200_OK,
    summary="Get Company Metadata Profile",
)
async def get_company(company_name: str):
    """Retrieves structured company profile by company name or domain."""
    return APIResponse(
        success=True,
        message=f"Company profile query for {company_name}",
        data=None,
    )
