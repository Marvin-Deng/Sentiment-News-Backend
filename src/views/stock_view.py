"""
Functions for processing requests and responses related to stocks.
"""

import datetime

from services import stock_services
from controllers import ticker_controller
from constants.stock import TICKERS


def get_eod_data(ticker: str, start_date: str, end_date: str) -> list:
    """
    Retrieves end-of-day stock price data for a given ticker and date range.
    """
    return stock_services.get_eod_data(ticker, start_date, end_date)


async def update_tickers() -> str:
    """
    Cron job for updating price action for each stock daily.
    """
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    return await ticker_controller.update_tickers(date_today)


def get_ticker_list() -> list:
    """
    Retrieves a list of tickers.
    """
    return TICKERS
