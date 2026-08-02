"""
Structured Logger Setup.
"""

import logging
import sys
from backend.config.settings import settings


def setup_logger() -> logging.Logger:
    """Configures application logger."""
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    logger_inst = logging.getLogger(settings.APP_NAME)
    logger_inst.setLevel(log_level)
    return logger_inst


logger = setup_logger()
