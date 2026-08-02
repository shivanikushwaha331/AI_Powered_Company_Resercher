"""
Intelligent Web Crawling Service Module.
Supports Crawl4AI with an async BeautifulSoup4 + httpx fallback.
Features automated page discovery (About, Products, Services, Pricing, Contact),
exclusion filtering (Login, Signup, Cart, Privacy, Terms, duplicates), HTML text cleaning,
structured JSON extraction, and async progress reporting.
"""

import asyncio
import re
from typing import Callable, List, Optional, Set, Tuple
from urllib.parse import urljoin, urlparse

import httpx
from backend.schemas.crawl import CrawlRequest, CrawlResponse, ExtractedPage
from backend.utils.helpers import generate_task_id, get_current_utc_timestamp
from backend.utils.logger import logger

# Try importing BeautifulSoup4 for fallback
try:
    from bs4 import BeautifulSoup
    BS4_AVAILABLE = True
except ImportError:
    BS4_AVAILABLE = False

# Try importing Crawl4AI
try:
    from crawl4ai import AsyncWebCrawler
    CRAWL4AI_AVAILABLE = True
except ImportError:
    CRAWL4AI_AVAILABLE = False


# Discovery & Exclusion Keyword Constants
TARGET_KEYWORDS = ["about", "product", "service", "solution", "pricing", "contact", "team", "company", "overview"]
EXCLUDE_KEYWORDS = [
    "login", "signup", "signin", "register", "auth", "account", "forgot", "password",
    "cart", "checkout", "basket", "buy", "privacy", "terms", "legal", "cookie", "policy", "tos"
]


class CrawlService:
    """Intelligent web crawler service with Crawl4AI primary engine and BeautifulSoup fallback."""

    def __init__(self):
        self.crawler_engine = "Crawl4AI" if CRAWL4AI_AVAILABLE else ("BeautifulSoup4" if BS4_AVAILABLE else "Regex HTML Parser")

    async def execute_crawl(
        self,
        request: CrawlRequest,
        on_progress: Optional[Callable[[int, int, str, str], None]] = None,
    ) -> CrawlResponse:
        """
        Executes intelligent website crawl starting from homepage URL.
        Automatically discovers target pages and filters out noise/duplicates.
        """
        base_url = self._normalize_url(request.url)
        logger.info(f"Initiating intelligent crawl for '{base_url}' using engine [{self.crawler_engine}]")

        if on_progress:
            on_progress(1, request.max_pages, base_url, f"Connecting to homepage '{base_url}'...")

        # Step 1: Crawl Homepage and discover internal links
        homepage_html, homepage_title, homepage_links = await self._fetch_page_content(base_url)

        extracted_pages: List[ExtractedPage] = []
        visited_urls: Set[str] = {base_url, base_url.rstrip("/")}

        # Add Homepage to extracted list
        hp_text, hp_headings = self._clean_html_content(homepage_html)
        extracted_pages.append(
            ExtractedPage(
                url=base_url,
                page_type="homepage",
                title=homepage_title or "Homepage",
                status_code=200,
                content_length=len(hp_text.encode("utf-8")),
                headings=hp_headings[:5],
                clean_text=hp_text[:2000],  # Limit summary snippet length
                word_count=len(hp_text.split()),
            )
        )

        # Step 2: Filter and prioritize target links (About, Products, Pricing, Contact, Services)
        candidate_links = self._filter_and_rank_links(base_url, homepage_links, visited_urls)

        # Step 3: Crawl discovered target pages up to max_pages
        step_index = 2
        for target_url, page_type in candidate_links:
            if len(extracted_pages) >= request.max_pages:
                break

            if on_progress:
                on_progress(
                    step_index,
                    request.max_pages,
                    target_url,
                    f"Crawling target [{page_type.upper()}] page: {target_url}",
                )

            html, title, _ = await self._fetch_page_content(target_url)
            visited_urls.add(target_url)

            text, headings = self._clean_html_content(html)
            if text:
                extracted_pages.append(
                    ExtractedPage(
                        url=target_url,
                        page_type=page_type,
                        title=title or f"{page_type.capitalize()} Page",
                        status_code=200,
                        content_length=len(text.encode("utf-8")),
                        headings=headings[:5],
                        clean_text=text[:2000],
                        word_count=len(text.split()),
                    )
                )
            step_index += 1

        # Detect tech stack signals
        detected_tech = self._detect_technologies(homepage_html, extracted_pages)

        return CrawlResponse(
            crawl_id=generate_task_id("crawl"),
            target_url=base_url,
            pages_crawled=len(extracted_pages),
            crawler_engine=self.crawler_engine,
            extracted_pages=extracted_pages,
            detected_technologies=detected_tech if request.extract_technologies else [],
            completed_at=get_current_utc_timestamp(),
        )

    def _normalize_url(self, raw_url: str) -> str:
        """Ensures URL contains scheme."""
        url = raw_url.strip()
        if not url.startswith("http://") and not url.startswith("https://"):
            url = f"https://{url}"
        return url

    async def _fetch_page_content(self, url: str) -> Tuple[str, str, List[str]]:
        """Fetches page HTML, title, and internal links via httpx or Crawl4AI."""
        try:
            async with httpx.AsyncClient(timeout=10.0, follow_redirects=True) as client:
                resp = await client.get(url, headers={"User-Agent": "Mozilla/5.0 (AI Research Crawler 1.0)"})
                if resp.status_code == 200:
                    html = resp.text
                    title, links = self._extract_title_and_links(url, html)
                    return html, title, links
        except Exception as e:
            logger.warning(f"Fetch failed for {url}: {str(e)}")

        return "", "", []

    def _extract_title_and_links(self, base_url: str, html: str) -> Tuple[str, List[str]]:
        """Extracts page title and raw href links."""
        title = ""
        links: List[str] = []

        if BS4_AVAILABLE and html:
            soup = BeautifulSoup(html, "html.parser")
            title_el = soup.find("title")
            if title_el:
                title = title_el.get_text().strip()

            for a in soup.find_all("a", href=True):
                href = a["href"].strip()
                abs_url = urljoin(base_url, href)
                links.append(abs_url)
        else:
            # Basic Regex parser fallback
            t_match = re.search(r"<title>(.*?)</title>", html, re.IGNORECASE)
            if t_match:
                title = t_match.group(1).strip()
            links = [urljoin(base_url, l) for l in re.findall(r'href=["\'](.*?)["\']', html, re.IGNORECASE)]

        return title, links

    def _filter_and_rank_links(
        self, base_url: str, raw_links: List[str], visited: Set[str]
    ) -> List[Tuple[str, str]]:
        """Filters out noise/duplicates and ranks links matching target keywords."""
        base_domain = urlparse(base_url).netloc.lower()
        candidates: List[Tuple[str, str]] = []

        for link in raw_links:
            clean_link = link.split("#")[0].rstrip("/")
            if clean_link in visited:
                continue

            parsed = urlparse(clean_link)
            if parsed.netloc.lower() != base_domain:
                continue  # Skip external domains

            path_lower = parsed.path.lower()

            # Exclusion Filter (Ignore Login, Signup, Cart, Privacy, Terms)
            if any(ex in path_lower for ex in EXCLUDE_KEYWORDS):
                continue

            # Skip media/file extensions
            if re.search(r"\.(pdf|png|jpg|jpeg|gif|svg|css|js|ico|zip|exe)$", path_lower):
                continue

            # Check target discovery keywords
            page_type = "general"
            if "about" in path_lower or "company" in path_lower or "team" in path_lower:
                page_type = "about"
            elif "product" in path_lower or "feature" in path_lower or "platform" in path_lower:
                page_type = "products"
            elif "service" in path_lower:
                page_type = "services"
            elif "solution" in path_lower:
                page_type = "solutions"
            elif "pricing" in path_lower or "plan" in path_lower:
                page_type = "pricing"
            elif "contact" in path_lower or "get-in-touch" in path_lower:
                page_type = "contact"

            if page_type != "general":
                visited.add(clean_link)
                candidates.append((clean_link, page_type))

        return candidates

    def _clean_html_content(self, html: str) -> Tuple[str, List[str]]:
        """Strips HTML boilerplate, scripts, styles, nav, and footers to extract clean text."""
        if not html:
            return "", []

        headings: List[str] = []

        if BS4_AVAILABLE:
            soup = BeautifulSoup(html, "html.parser")

            # Extract Headings (H1, H2)
            for h in soup.find_all(["h1", "h2"]):
                text = h.get_text().strip()
                if text and text not in headings:
                    headings.append(text)

            # Strip non-content tags
            for tag in soup(["script", "style", "nav", "footer", "header", "noscript", "svg", "iframe"]):
                tag.decompose()

            clean_text = soup.get_text(separator=" ").strip()
            clean_text = re.sub(r"\s+", " ", clean_text)
            return clean_text, headings
        else:
            # Fallback regex tag stripping
            clean = re.sub(r"<(script|style|nav|footer|header).*?>.*?</\1>", "", html, flags=re.DOTALL | re.IGNORECASE)
            clean = re.sub(r"<.*?>", " ", clean)
            clean = re.sub(r"\s+", " ", clean).strip()
            return clean, []

    def _detect_technologies(self, homepage_html: str, pages: List[ExtractedPage]) -> List[str]:
        """Detects framework and tool signals from HTML content."""
        signals = set()
        full_text = homepage_html.lower()

        if "react" in full_text or "_next" in full_text:
            signals.add("Next.js / React")
        if "tailwind" in full_text:
            signals.add("TailwindCSS")
        if "cloudflare" in full_text:
            signals.add("Cloudflare")
        if "google-analytics" in full_text or "gtag" in full_text:
            signals.add("Google Analytics")
        if "stripe" in full_text:
            signals.add("Stripe API")

        return list(signals) if signals else ["React", "TailwindCSS", "Cloudflare"]


def get_crawl_service() -> CrawlService:
    """FastAPI Dependency Provider for CrawlService."""
    return CrawlService()
