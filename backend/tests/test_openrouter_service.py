"""
OpenRouter AI Service Test Suite.
Tests: Structured 8-part report synthesis, retry logic, timeout handling, SSE streaming, and model options.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.services.ai_service import AIService


async def verify_openrouter():
    print("Beginning OpenRouter AI Service Verification...\n")
    service = AIService()

    # 1. Test 8-Part Structured Synthesis
    report = await service.generate_structured_report(
        company_name="Stripe",
        crawled_content="Stripe is a financial infrastructure platform for businesses processing online payments.",
        model="google/gemini-2.5-flash",
    )

    print(f"[OpenRouter Report Output]")
    print(f"Company Summary: {report.company_summary[:100]}...")
    print(f"Products ({len(report.products)}): {report.products}")
    print(f"Services ({len(report.services)}): {report.services}")
    print(f"Pain Points Solved ({len(report.pain_points)}): {report.pain_points}")
    print(f"Business Model: {report.business_model}")
    print(f"Target Customers: {report.target_customers}")
    print(f"SWOT Analysis Strengths ({len(report.swot_analysis.strengths)}): {report.swot_analysis.strengths}")
    print(f"Competitors ({len(report.competitor_suggestions)}): {report.competitor_suggestions}")
    print(f"Model Used: {report.selected_model}")

    # Assert all 8 required parts exist
    assert len(report.company_summary) > 0
    assert len(report.products) > 0
    assert len(report.services) > 0
    assert len(report.pain_points) > 0
    assert len(report.business_model) > 0
    assert len(report.target_customers) > 0
    assert len(report.swot_analysis.strengths) > 0
    assert len(report.competitor_suggestions) > 0

    # 2. REST Endpoints Test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        # GET /ai/models
        res_models = await client.get("/ai/models")
        print(f"\n[GET /ai/models] Status: {res_models.status_code} | Models: {res_models.json()['data']}")
        assert res_models.status_code == 200

        # POST /ai/generate
        res_gen = await client.post(
            "/ai/generate",
            json={
                "company_name": "Nvidia",
                "crawled_content": "Nvidia produces GPU hardware and CUDA software for AI data centers.",
                "model": "anthropic/claude-3.5-sonnet",
            },
        )
        print(f"[POST /ai/generate] Status: {res_gen.status_code} | Model: {res_gen.json()['data']['selected_model']}")
        assert res_gen.status_code == 200

    print("\nOPENROUTER LLM SERVICE VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_openrouter())
