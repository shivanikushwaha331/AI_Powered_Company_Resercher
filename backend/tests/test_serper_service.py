"""
Serper.dev Integration Verification Test Suite.
Tests: Microsoft, Tesla, Stripe, and Direct URL skipping.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.services.serper_service import SerperService


async def verify_serper():
    print("Beginning Serper.dev Integration Verification...\n")
    service = SerperService()

    # 1. Company Name Query: Microsoft
    r_msft = await service.extract_company_info("Microsoft")
    print(f"[Microsoft] Company: '{r_msft.company_name}' | Website: {r_msft.official_website} | Phone: {r_msft.phone} | Address: {r_msft.address} | Industry: {r_msft.industry}")
    assert "Microsoft" in r_msft.company_name
    assert "microsoft.com" in r_msft.official_website
    assert r_msft.is_direct_url is False

    # 2. Company Name Query: Tesla
    r_tesla = await service.extract_company_info("Tesla")
    print(f"[Tesla] Company: '{r_tesla.company_name}' | Website: {r_tesla.official_website} | Phone: {r_tesla.phone} | Address: {r_tesla.address} | Industry: {r_tesla.industry}")
    assert "Tesla" in r_tesla.company_name
    assert "tesla.com" in r_tesla.official_website
    assert r_tesla.is_direct_url is False

    # 3. Company Name Query: Stripe
    r_stripe = await service.extract_company_info("Stripe")
    print(f"[Stripe] Company: '{r_stripe.company_name}' | Website: {r_stripe.official_website} | Phone: {r_stripe.phone} | Address: {r_stripe.address} | Industry: {r_stripe.industry}")
    assert "Stripe" in r_stripe.company_name
    assert "stripe.com" in r_stripe.official_website
    assert r_stripe.is_direct_url is False

    # 4. Direct URL Input: https://stripe.com (Skipping Serper search)
    r_url = await service.extract_company_info("https://stripe.com")
    print(f"[Direct URL] Company: '{r_url.company_name}' | Website: {r_url.official_website} | Is Direct URL: {r_url.is_direct_url}")
    assert r_url.is_direct_url is True
    assert r_url.official_website == "https://stripe.com"

    # 5. REST Endpoint Verification: POST /serper/search
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res = await client.post("/serper/search", json={"query": "Microsoft"})
        print(f"\n[POST /serper/search] Status: {res.status_code} | Payload: {res.json()['data']['company_name']}")
        assert res.status_code == 200

    print("\nSERPER.DEV INTEGRATION VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_serper())
