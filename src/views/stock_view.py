"""
Functions for processing requests and responses related to stocks.
"""

import datetime

from controllers.ticker_controller import TickerController
from constants.stock import TICKERS


async def update_tickers() -> str:
    """
    Cron job for updating price action for each stock daily
    """
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    return await TickerController.update_tickers(date_today)


def get_ticker_list() -> list:
    """
    Retrieves a list of tickers
    """
    return TICKERS
