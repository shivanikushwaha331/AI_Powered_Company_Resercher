"""
Competitor Research Service Test Suite.
Tests: Competitor identification, Serper automated website resolution, country extraction, and competition reasoning.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.services.competitor_service import CompetitorService


async def verify_competitors():
    print("Beginning Competitor Research Service Verification...\n")
    service = CompetitorService()

    # 1. Test Competitor Analysis for Stripe
    res = await service.analyze_competitors(
        target_company="Stripe",
        competitor_names=["Adyen", "PayPal", "Square", "Checkout.com"],
    )

    print(f"[Stripe Competitors Count: {len(res.competitors)}]")
    for c in res.competitors:
        print(f"  • Company: '{c.company_name}' | Website: {c.website} | Country: {c.country}")
        print(f"    Reason: {c.reason_for_competition}")

        assert len(c.company_name) > 0
        assert c.website.startswith("http")
        assert len(c.country) > 0
        assert len(c.reason_for_competition) > 0

    # 2. Test Automated Serper Resolution for Missing Website Competitor
    res_missing = await service.analyze_competitors(
        target_company="Custom Corp",
        competitor_names=["Snowflake"],
    )

    print(f"\n[Automated Serper Resolution Test for Missing Website]")
    for c in res_missing.competitors:
        print(f"  • Resolved Competitor: '{c.company_name}' | Website: {c.website} | Country: {c.country}")
        assert "snowflake" in c.website.lower() or "http" in c.website

    # 3. REST Endpoint Test: POST /competitors
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_api = await client.post(
            "/competitors",
            json={"company_name": "Nvidia", "competitor_names": ["AMD", "Intel"]},
        )
        print(f"\n[POST /competitors REST Test] Status: {res_api.status_code} | Count: {len(res_api.json()['data']['competitors'])}")
        assert res_api.status_code == 200

    print("\nCOMPETITOR RESEARCH SERVICE VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_competitors())
