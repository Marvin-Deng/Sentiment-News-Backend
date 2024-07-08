"""
Module with stock utility functions for parsing stock info and calculating market date.
"""

from datetime import datetime, date, timedelta, time

from services import stock_services


def get_stock_info(ticker: str, date_str: str) -> dict:
    """
    Parses the end of day data retuned by Tinngo API.
    """
    eod_data = stock_services.get_eod_data(
        ticker=ticker, start_date=date_str, end_date=date_str
    )

    stock_info = {
        "open_price": None,
        "high_price": None,
        "low_price": None,
        "close_price": None,
        "volume": None,
        "adj_open": None,
        "adj_high": None,
        "adj_low": None,
        "adj_close": None,
        "adj_volume": None,
        "div_cash": None,
        "split_factor": None,
    }

    if (
        eod_data
        and isinstance(eod_data, list)
        and len(eod_data) > 0
        and isinstance(eod_data[0], dict)
    ):
        keys_mapping = {
            "open_price": "open",
            "high_price": "high",
            "low_price": "low",
            "close_price": "close",
            "volume": "volume",
            "adj_open": "adjOpen",
            "adj_high": "adjHigh",
            "adj_low": "adjLow",
            "adj_close": "adjClose",
            "adj_volume": "adjVolume",
            "div_cash": "divCash",
            "split_factor": "splitFactor",
        }

        for key, eod_key in keys_mapping.items():
            stock_info[key] = eod_data[0].get(eod_key, None)

    return stock_info


def get_market_date(article_datetime: datetime) -> date:
    """
    Returns the next market open date after the article publication datetime.
    """
    published_date = article_datetime.date()
    if published_date.weekday() >= 5 or (
        published_date.weekday() == 4 and _after_market_closed(article_datetime)
    ):
        return _get_next_monday(published_date)

    if _after_market_closed(article_datetime):
        return published_date + timedelta(days=1)

    return published_date


def _after_market_closed(article_datetime: datetime) -> bool:
    """
    Returns if the provided datetime occurs after market close.
    """
    return article_datetime.time() >= time(21, 0)


def _get_next_monday(date_obj: datetime) -> datetime:
    """
    Returns the next Monday from a datetime.
    """
    return date_obj + timedelta(days=(7 - date_obj.weekday()) % 7)
