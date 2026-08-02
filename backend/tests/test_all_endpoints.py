"""
Comprehensive Unit Test Suite for FastAPI Backend Endpoints.
Tests: GET /health, POST /research, POST /crawl, POST /generate-report, POST /generate-pdf, POST /discord.
"""

import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app


@pytest.fixture
async def client():
    """Async client fixture."""
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c


@pytest.mark.asyncio
async def test_get_health(client: AsyncClient):
    """Test GET /health."""
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "app_name" in data


@pytest.mark.asyncio
async def test_post_research(client: AsyncClient):
    """Test POST /research."""
    payload = {"company_name": "Stripe", "depth": "standard"}
    response = await client.post("/research", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["company_name"] == "Stripe"


@pytest.mark.asyncio
async def test_post_crawl(client: AsyncClient):
    """Test POST /crawl."""
    payload = {"url": "https://stripe.com", "max_pages": 3}
    response = await client.post("/crawl", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["pages_crawled"] > 0


@pytest.mark.asyncio
async def test_post_generate_report(client: AsyncClient):
    """Test POST /generate-report."""
    payload = {"company_name": "Stripe", "output_format": "markdown"}
    response = await client.post("/generate-report", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["format"] == "markdown"


@pytest.mark.asyncio
async def test_post_generate_pdf(client: AsyncClient):
    """Test POST /generate-pdf."""
    payload = {"title": "Stripe Market Analysis Report"}
    response = await client.post("/generate-pdf", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["download_url"].startswith("http")


@pytest.mark.asyncio
async def test_post_discord(client: AsyncClient):
    """Test POST /discord."""
    payload = {
        "title": "Research Complete",
        "summary": "Stripe research summary report completed.",
        "company_name": "Stripe",
    }
    response = await client.post("/discord", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["data"]["status"] == "sent"
