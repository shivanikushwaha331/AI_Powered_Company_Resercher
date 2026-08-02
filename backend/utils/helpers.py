"""
Utility functions for ID generation, timestamp formatting, and URL validation.
"""

import re
import uuid
from datetime import datetime, timezone

URL_REGEX = re.compile(
    r"^(https?://)?"  # http:// or https://
    r"(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|"  # domain...
    r"localhost|"  # localhost...
    r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})"  # ...or ip
    r"(?::\d+)?"  # optional port
    r"(?:/?|[/?]\S+)$",
    re.IGNORECASE,
)


def generate_task_id(prefix: str = "task") -> str:
    """Generates unique prefixed task ID."""
    return f"{prefix}_{uuid.uuid4().hex[:8]}"


def get_current_utc_timestamp() -> str:
    """Returns current ISO formatted UTC timestamp string."""
    return datetime.now(timezone.utc).isoformat()


def is_url(text: str) -> bool:
    """Checks whether a given query string is a direct website URL."""
    text_clean = text.strip().lower()
    if text_clean.startswith("http://") or text_clean.startswith("https://") or text_clean.startswith("www."):
        return True
    # Check regex for domain.tld pattern
    return bool(URL_REGEX.match(text_clean))
