"""
Direct Async Runner for Backend Endpoints Verification.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app


async def run_verifications():
    print("Beginning FastAPI Backend Endpoint Verification...")
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # 1. GET /health
        r1 = await client.get("/health")
        print(f"[GET /health] Status: {r1.status_code} | Payload: {r1.json()}")
        assert r1.status_code == 200, f"Expected 200, got {r1.status_code}"

        # 2. POST /research
        r2 = await client.post("/research", json={"company_name": "Stripe", "depth": "standard"})
        print(f"[POST /research] Status: {r2.status_code} | Success: {r2.json()['success']}")
        assert r2.status_code == 200, f"Expected 200, got {r2.status_code}"

        # 3. POST /crawl
        r3 = await client.post("/crawl", json={"url": "https://stripe.com", "max_pages": 3})
        print(f"[POST /crawl] Status: {r3.status_code} | Pages Crawled: {r3.json()['data']['pages_crawled']}")
        assert r3.status_code == 200, f"Expected 200, got {r3.status_code}"

        # 4. POST /generate-report
        r4 = await client.post("/generate-report", json={"company_name": "Stripe", "output_format": "markdown"})
        print(f"[POST /generate-report] Status: {r4.status_code} | Format: {r4.json()['data']['format']}")
        assert r4.status_code == 200, f"Expected 200, got {r4.status_code}"

        # 5. POST /generate-pdf
        r5 = await client.post("/generate-pdf", json={"title": "Stripe Report"})
        print(f"[POST /generate-pdf] Status: {r5.status_code} | URL: {r5.json()['data']['download_url']}")
        assert r5.status_code == 200, f"Expected 200, got {r5.status_code}"

        # 6. POST /discord
        r6 = await client.post(
            "/discord",
            json={"title": "Research Done", "summary": "Finished research", "company_name": "Stripe"},
        )
        print(f"[POST /discord] Status: {r6.status_code} | Message status: {r6.json()['data']['status']}")
        assert r6.status_code == 200, f"Expected 200, got {r6.status_code}"

    print("\nALL 6 ENDPOINTS VERIFIED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(run_verifications())
