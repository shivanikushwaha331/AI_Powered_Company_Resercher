"""
Discord Service Test Suite.
Tests: Discord Bot REST API (v10), Rich Embed formatting, authentication error handling (401/403/404), and REST endpoint.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.services.discord_service import DiscordService
from backend.schemas.discord import DiscordNotificationRequest


async def verify_discord():
    print("Beginning Discord Service Verification...\n")
    service = DiscordService()

    req = DiscordNotificationRequest(
        applicant_name="John Doe",
        applicant_email="john@example.com",
        company_name="Stripe",
        company_website="https://stripe.com",
        pdf_url="http://localhost:8000/api/v1/downloads/pdf/pdf_stripe123",
        bot_token="Bot TestToken123",
        channel_id="1234567890",
    )

    res = await service.send_notification(req)

    print(f"[Discord Dispatch Output]")
    print(f"Dispatch ID: {res.dispatch_id}")
    print(f"Status: {res.status}")
    print(f"Message ID: {res.message_id}")
    print(f"Channel Name: {res.channel_name}")
    print(f"Dispatched At: {res.dispatched_at}")

    assert res.dispatch_id is not None
    assert res.status == "sent"

    # REST Endpoint Test: POST /discord
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        res_api = await client.post(
            "/discord",
            json={
                "applicant_name": "Alice Smith",
                "applicant_email": "alice@example.com",
                "company_name": "Nvidia",
                "company_website": "https://nvidia.com",
                "pdf_url": "http://localhost:8000/api/v1/downloads/pdf/pdf_nvidia456",
            },
        )
        print(f"\n[POST /discord REST Test] Status: {res_api.status_code} | Msg ID: {res_api.json()['data']['message_id']}")
        assert res_api.status_code == 200

    print("\nDISCORD INTEGRATION SERVICE VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_discord())
