"""
Module for querying and updating ticker table.
"""

import datetime

from models.ticker import TickerModel
from utils import logging_utils, stock_utils


async def create_ticker(ticker: str, publication_datetime: datetime) -> TickerModel:
    """
    Create a new ticker entry if it doesn't already exist.
    """
    market_date = stock_utils.get_market_date(publication_datetime).strftime("%Y-%m-%d")
    existing_ticker = await TickerModel.filter(ticker=ticker, market_date=market_date)
    if existing_ticker:
        return "Ticker already exists", existing_ticker[0], 409

    try:
        stock_info = stock_utils.get_stock_info(ticker=ticker, date_str=market_date)
        new_ticker = TickerModel(ticker=ticker, market_date=market_date, **stock_info)
        await new_ticker.save()
        return "Created new ticker", new_ticker, 201

    except Exception as e:
        error_message = "Error occured in controllers.create_ticker"
        return logging_utils.log_error(e, error_message, None, 500)


async def update_tickers(date_str: str) -> list:
    """
    Update price action for tickers on a specific date.
    """
    try:
        tickers = await TickerModel.filter(market_date=date_str, open_price=None)
        updated_tickers = []
        for ticker_model in tickers:
            stock_info = stock_utils.get_stock_info(
                ticker=ticker_model.ticker, date_str=date_str
            )
            if not stock_info.get("open_price"):
                continue
            for key, value in stock_info.items():
                if hasattr(ticker_model, key):
                    setattr(ticker_model, key, value)
            await ticker_model.save()
            updated_tickers.append(ticker_model.ticker)
        return "Successfully updated tickers", updated_tickers, 200

    except Exception as e:
        error_message = "Error occured in controllers.update_tickers"
        return logging_utils.log_error(e, error_message, None, 500)
