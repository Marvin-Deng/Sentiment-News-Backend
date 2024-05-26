import requests
from datetime import timedelta, time

from constants.env_consts import TINNGO_API_KEY


class StockUtils:

    @staticmethod
    def get_eod_data(ticker, start_date, end_date):
        try:
            url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={TINNGO_API_KEY}"
            headers = {"Content-Type": "application/json"}
            response = requests.get(url, headers=headers)
            return response.json()

        except Exception:
            return None

    @staticmethod
    def get_market_date(article_datetime):
        published_date = article_datetime.date()

        if published_date.weekday() >= 5 or (
            published_date.weekday() == 4
            and StockUtils.after_market_closed(article_datetime)
        ):
            return StockUtils.get_next_monday(published_date)
        elif StockUtils.after_market_closed(article_datetime):
            return published_date + timedelta(days=1)
        return published_date

    @staticmethod
    def after_market_closed(article_datetime):
        return article_datetime.time() >= time(21, 0)

    @staticmethod
    def get_next_monday(date):
        return date + timedelta(days=(7 - date.weekday()) % 7)

    @staticmethod
    def get_stock_info(ticker, date):
        eod_data = StockUtils.get_eod_data(ticker, date, date)
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
            stock_info.update(
                {
                    "open_price": eod_data[0].get("open", 0),
                    "high_price": eod_data[0].get("high", 0),
                    "low_price": eod_data[0].get("low", 0),
                    "close_price": eod_data[0].get("close", 0),
                    "volume": eod_data[0].get("volume", 0),
                    "adj_open": eod_data[0].get("adjOpen", 0),
                    "adj_high": eod_data[0].get("adjHigh", 0),
                    "adj_low": eod_data[0].get("adjLow", 0),
                    "adj_close": eod_data[0].get("adjClose", 0),
                    "adj_volume": eod_data[0].get("adjVolume", 0),
                    "div_cash": eod_data[0].get("divCash", 0),
                    "split_factor": eod_data[0].get("splitFactor", 0),
                }
            )

        return stock_info
