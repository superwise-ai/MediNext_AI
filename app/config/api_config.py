"""
API Configuration for Superwise Integration

This module contains configuration settings for the Superwise API integration.
"""

import os
from typing import Optional

# Superwise API Configuration
SUPERWISE_API_URL = os.getenv("SUPERWISE_API_URL")
SUPERWISE_API_VERSION = os.getenv("SUPERWISE_API_VERSION")
SUPERWISE_APP_ID = os.getenv("SUPERWISE_APP_ID")

# API Timeout Settings
API_TIMEOUT = int(os.getenv("API_TIMEOUT", "30"))  # seconds

# Retry Settings
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", "1"))  # seconds


def get_superwise_headers() -> dict:
    """
    Get headers for Superwise API requests

    Returns:
        dict: Headers dictionary
    """
    return {
        "Content-Type": "application/json",
        # "Authorization": f"Bearer ",
        # "X-API-Version": SUPERWISE_API_VERSION,
        "User-Agent": "MediNext-AI/1.0",
    }


def validate_api_config() -> bool:
    """
    Validate that required API configuration is present

    Returns:
        bool: True if configuration is valid, False otherwise
    """
    if not SUPERWISE_API_URL:
        return False
    if not SUPERWISE_APP_ID:
        return False
    return True
