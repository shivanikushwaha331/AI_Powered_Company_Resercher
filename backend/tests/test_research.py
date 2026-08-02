"""
Research Endpoints Integration Test Skeletons.
"""

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_research_task_schema(async_client: AsyncClient):
    """Test research task request validation."""
    payload = {"company_name": "Stripe", "depth": "standard"}
    response = await async_client.post("/api/v1/research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
