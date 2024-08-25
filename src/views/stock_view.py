"""
Functions for processing requests and responses related to stocks.
"""

import datetime

from models.response import Status, EodResponse, CronResponse, TickerResponse
from services import stock_services
from controllers import ticker_controller
from constants.stock import TICKERS
from utils.logging_utils import log_exception_error


def get_eod_data(ticker: str, start_date: str, end_date: str) -> EodResponse:
    """
    Retrieves end-of-day stock price data for a given ticker and date range.
    """
    data = stock_services.get_eod_data(ticker, start_date, end_date)

    return EodResponse(
        status=Status(message="SUCCESS", rcode=200),
        num_returned=len(data),
        eod_data=data,
    )


async def update_tickers() -> CronResponse:
    """
    Cron job for updating price action for each stock daily.
    """
    try:
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        message, data, rcode = await ticker_controller.update_tickers(date_today)

    except Exception as e:
        error_message = "ERROR in stock_view.update_tickers"
        message, data, rcode = log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return CronResponse(
        status=Status(message=message, rcode=rcode),
        num_returned=len(data),
        processed=data,
    )


def get_ticker_list() -> TickerResponse:
    """
    Retrieves a list of tickers.
    """
    return TickerResponse(
        status=Status(message="SUCCESS", rcode=200),
        tickers=TICKERS,
    )
