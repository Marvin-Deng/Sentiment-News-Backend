"""
Module with logging utility functions.
"""

import logging
import traceback

logging.basicConfig(filename="error.log", level=logging.ERROR)


def log_error(error: str, message: str, return_obj: dict, status: int):
    """
    Logger for errors.
    """
    error_message = f"{message}: {error}"
    logging.error(error_message)
    logging.error(traceback.format_exc())
    return error_message, return_obj, status
