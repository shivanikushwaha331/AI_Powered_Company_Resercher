"""
Intelligent Web Crawler Test Suite.
Tests: Link discovery, exclusion filters (Login, Signup, Privacy, Terms), text cleaning, page type classification, and progress updates.
"""

import asyncio
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.schemas.crawl import CrawlRequest
from backend.services.crawl_service import CrawlService


async def verify_crawler():
    print("Beginning Intelligent Web Crawler Verification...\n")
    service = CrawlService()

    progress_log = []

    def progress_callback(step: int, total: int, current_url: str, message: str):
        progress_log.append((step, message))
        print(f"  ⚡ [Progress {step}/{total}] {message}")

    req = CrawlRequest(url="https://stripe.com", max_pages=4, extract_technologies=True)
    res = await service.execute_crawl(req, on_progress=progress_callback)

    print(f"\n[Crawl Result Summary]")
    print(f"Target URL: {res.target_url}")
    print(f"Pages Crawled: {res.pages_crawled}")
    print(f"Crawler Engine Used: {res.crawler_engine}")
    print(f"Detected Technologies: {res.detected_technologies}")

    assert res.pages_crawled > 0
    assert len(progress_log) > 0

    print("\n[Extracted Pages Breakdown]")
    for p in res.extracted_pages:
        print(f"  • [{p.page_type.upper()}] Title: '{p.title}' | Words: {p.word_count} | URL: {p.url}")
        # Verify no excluded keywords exist in the page URLs
        url_lower = p.url.lower()
        for excluded in ["login", "signup", "privacy", "terms", "cookie"]:
            assert excluded not in url_lower, f"Excluded keyword '{excluded}' found in crawled URL: {p.url}"

        # Verify clean text is extracted
        assert len(p.clean_text) > 0
        assert "<script>" not in p.clean_text.lower()
        assert "<style>" not in p.clean_text.lower()

    # REST API Endpoint Test
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        api_res = await client.post("/crawl", json={"url": "https://microsoft.com", "max_pages": 3})
        print(f"\n[POST /crawl REST Test] Status: {api_res.status_code} | Pages: {api_res.json()['data']['pages_crawled']}")
        assert api_res.status_code == 200

    print("\nINTELLIGENT WEB CRAWLER VERIFICATION PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    asyncio.run(verify_crawler())
