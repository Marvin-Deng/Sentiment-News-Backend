"""
Module with date utility functions.
"""

from datetime import datetime, timezone


def convert_unix_to_utc(unix: str) -> str:
    """
    Converts a UNIX time string to a UTC datetime string.
    """
    utc_datetime = datetime.fromtimestamp(unix, tz=timezone.utc)
    return utc_datetime.strftime("%Y-%m-%d %H:%M:%S")
