"""
Functions for retrieving info from third-party stock APIs.
"""

import json
import requests

from constants.env_consts import TINNGO_API_KEY


def get_eod_data(ticker: str, start_date: str, end_date: str) -> json:
    """
    Retrieves end-of-day stock price data for a given ticker and date range.
    """
    try:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices"
        params = {"startDate": start_date, "endDate": end_date, "token": TINNGO_API_KEY}
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        return response.json() if response.ok else None

    except Exception:
        return None
