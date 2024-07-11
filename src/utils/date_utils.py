"""
Module with date utility functions.
"""

from datetime import datetime


def convert_unix_to_utc(unix: int) -> str:
    """
    Converts a UNIX timestamp to a UTC datetime string.
    """
    utc_datetime = datetime.utcfromtimestamp(unix)
    return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
