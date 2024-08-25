"""
Module with logging utility functions.
"""

import logging
import traceback

logging.basicConfig(filename="error.log", level=logging.INFO)

logger = logging.getLogger(__name__)


def log_exception_error(error: Exception, message: str, data: list, status: int):
    """
    Logger for errors.
    """
    error_message = f"message={message}, error={error}, status={status}"
    logger.error(error_message)
    logger.error(traceback.format_exc())
    return error_message, data, status
