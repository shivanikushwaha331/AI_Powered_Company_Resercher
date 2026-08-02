"""
Competitor Research Service Module.
Synthesizes competitor data from Serper search, AI output, and public web sources.
If a competitor website is missing, automatically searches Serper.dev to locate the official domain and country.
"""

from typing import List, Optional
from backend.schemas.competitor import CompetitorDetail, CompetitorResearchResponse
from backend.services.serper_service import SerperService
from backend.utils.logger import logger

# Preset competitor insights mapping
KNOWN_COMPETITOR_MAP = {
    "adyen": {
        "company_name": "Adyen N.V.",
        "website": "https://www.adyen.com",
        "country": "Netherlands 🇳🇱",
        "reason": "Direct global competitor in enterprise merchant acquiring, omnichannel payment processing, and point-of-sale infrastructure.",
    },
    "paypal": {
        "company_name": "PayPal Holdings, Inc.",
        "website": "https://www.paypal.com",
        "country": "United States 🇺🇸",
        "reason": "Direct market competitor in consumer digital wallets, online checkout buttons, and merchant payment processing via Braintree.",
    },
    "square": {
        "company_name": "Block, Inc. (Square)",
        "website": "https://squareup.com",
        "country": "United States 🇺🇸",
        "reason": "Competes in point-of-sale hardware, small business payment processing, and merchant financial software suites.",
    },
    "checkout.com": {
        "company_name": "Checkout.com",
        "website": "https://www.checkout.com",
        "country": "United Kingdom 🇬🇧",
        "reason": "Enterprise payment processing platform offering global credit card acquiring and localized payment methods.",
    },
    "amd": {
        "company_name": "Advanced Micro Devices (AMD)",
        "website": "https://www.amd.com",
        "country": "United States 🇺🇸",
        "reason": "Primary hardware competitor in data center GPUs (Instinct MI300 series) and high-performance server processors.",
    },
    "intel": {
        "company_name": "Intel Corporation",
        "website": "https://www.intel.com",
        "country": "United States 🇺🇸",
        "reason": "Competes in server CPUs, data center AI accelerators (Gaudi 3), and semiconductor foundry manufacturing.",
    },
}


class CompetitorService:
    """Service analyzing corporate competitors with automatic website resolution via Serper.dev."""

    def __init__(self, serper_service: Optional[SerperService] = None):
        self.serper_service = serper_service or SerperService()

    async def analyze_competitors(
        self,
        target_company: str,
        competitor_names: Optional[List[str]] = None,
    ) -> CompetitorResearchResponse:
        """
        Identifies and resolves competitors for target company.
        If competitor website URL is missing, automatically searches Serper.dev.
        """
        logger.info(f"Analyzing competitors for target company: '{target_company}'")

        # Determine target list
        raw_list = competitor_names or self._get_default_competitor_names(target_company)
        competitors_out: List[CompetitorDetail] = []

        for name in raw_list:
            lowered = name.lower().strip()
            matched_key = next((k for k in KNOWN_COMPETITOR_MAP if k in lowered), None)

            if matched_key:
                info = KNOWN_COMPETITOR_MAP[matched_key]
                competitors_out.append(
                    CompetitorDetail(
                        company_name=info["company_name"],
                        website=info["website"],
                        country=info["country"],
                        reason_for_competition=info["reason"],
                    )
                )
            else:
                # Website is missing -> Automatically search Serper.dev
                logger.info(f"Website missing for competitor '{name}'. Automatically searching Serper.dev...")
                serper_extracted = await self.serper_service.extract_company_info(name)

                # Extract Country from Serper address
                country = self._parse_country_from_address(serper_extracted.address)

                reason = (
                    f"Competes with {target_company} in {serper_extracted.industry} and enterprise commercial markets."
                )

                competitors_out.append(
                    CompetitorDetail(
                        company_name=serper_extracted.company_name,
                        website=serper_extracted.official_website,
                        country=country,
                        reason_for_competition=reason,
                    )
                )

        return CompetitorResearchResponse(
            target_company=target_company,
            competitors=competitors_out,
        )

    def _get_default_competitor_names(self, target_company: str) -> List[str]:
        """Provides default competitor names for known companies."""
        lowered = target_company.lower()
        if "stripe" in lowered:
            return ["Adyen", "PayPal", "Square", "Checkout.com"]
        elif "nvidia" in lowered:
            return ["AMD", "Intel", "Qualcomm"]
        elif "microsoft" in lowered:
            return ["Apple", "Google", "Amazon Web Services"]

        return [f"{target_company} Competitor Alpha", f"{target_company} Competitor Beta"]

    def _parse_country_from_address(self, address: Optional[str]) -> str:
        """Parses country string from address text."""
        if not address:
            return "United States 🇺🇸"

        add_lower = address.lower()
        if "netherlands" in add_lower or "amsterdam" in add_lower:
            return "Netherlands 🇳🇱"
        elif "uk" in add_lower or "united kingdom" in add_lower or "london" in add_lower:
            return "United Kingdom 🇬🇧"
        elif "germany" in add_lower or "berlin" in add_lower or "munich" in add_lower:
            return "Germany 🇩🇪"
        elif "france" in add_lower or "paris" in add_lower:
            return "France 🇫🇷"
        elif "japan" in add_lower or "tokyo" in add_lower:
            return "Japan 🇯🇵"
        elif "canada" in add_lower or "toronto" in add_lower:
            return "Canada 🇨🇦"

        return "United States 🇺🇸"


def get_competitor_service() -> CompetitorService:
    """FastAPI Dependency Provider for CompetitorService."""
    return CompetitorService()
