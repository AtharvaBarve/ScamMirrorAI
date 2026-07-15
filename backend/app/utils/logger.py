import logging
import os
from datetime import datetime
from pathlib import Path

def setup_logging(log_level=logging.INFO, log_file=None):
    """
    Set up logging configuration for the application.

    Args:
        log_level: Logging level (default: INFO)
        log_file: Path to log file (default: logs/scam_mirror.log)
    """
    # Create logs directory if it doesn't exist
    if log_file is None:
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        log_file = log_dir / "scam_mirror.log"

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Set up root logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear any existing handlers
    logger.handlers.clear()

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Console handler (for development)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

def get_logger(name):
    """
    Get a logger instance for a specific module.

    Args:
        name: Usually __name__ of the calling module

    Returns:
        Logger instance
    """
    return logging.getLogger(name)