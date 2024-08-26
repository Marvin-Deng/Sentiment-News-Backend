"""
Functions for retrieving info from third-party stock APIs.
"""

import requests

from config.env import TINNGO_API_KEY
from utils.logging_utils import logger, log_exception_error


def get_eod_data_tinngo(ticker: str, start_date: str, end_date: str) -> dict:
    """
    Retrieves end-of-day stock price data from Tinngo for a given ticker and date range.
    """
    try:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices"
        params = {"startDate": start_date, "endDate": end_date, "token": TINNGO_API_KEY}
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, params=params, headers=headers, timeout=10)
        if not response.ok:
            raise Exception(f"HTTP Error {response.status_code}: {response.text}")
        return "SUCCESS", response.json(), 200

    except Exception as e:
        message = f"Error when getting EOD data from Tinngo ticker={ticker}, start_date={start_date}, end_date={end_date}: {e}"
        return log_exception_error(e, message, {}, 500)
