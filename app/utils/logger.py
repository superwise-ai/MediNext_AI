"""
Global Logging Configuration for EHR Demo Portal

This module provides centralized logging configuration that can be used
across all components of the EHR portal application.
"""

import logging
import sys
from datetime import datetime
import os


def setup_logger(name: str = None, level: str = "INFO") -> logging.Logger:
    """
    Set up and configure a logger with consistent formatting and handlers.

    Args:
        name (str): Logger name (usually __name__ from the calling module)
        level (str): Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)

    Returns:
        logging.Logger: Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name or __name__)
    logger.setLevel(getattr(logging, level.upper()))

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(getattr(logging, level.upper()))

    # Create file handler for persistent logs
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_filename = f"{log_dir}/ehr_portal_{datetime.now().strftime('%Y%m%d')}.log"
    file_handler = logging.FileHandler(log_filename, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)  # File handler captures all levels

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Add formatter to handlers
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a configured logger instance.

    Args:
        name (str): Logger name (usually __name__ from the calling module)

    Returns:
        logging.Logger: Configured logger instance
    """
    return setup_logger(name)


# Global logger for the application
app_logger = get_logger("ehr_portal")

# Log application startup
app_logger.info("🚀 EHR Portal Application Starting")
app_logger.info("📊 Logging system initialized")
