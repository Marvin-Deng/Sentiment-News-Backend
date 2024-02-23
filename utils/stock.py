import requests
import pytz
from datetime import datetime, timedelta, time
from dotenv import load_dotenv
import os

load_dotenv()


class StockUtils:

    @staticmethod
    def get_eod_data(ticker, date_str):
        try:
            url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={date_str}&endDate={date_str}&token={os.getenv('TIINGO_TOKEN')}"
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.get(url, headers=headers)
            return response.json()

        except Exception:
            return None

    @staticmethod
    def get_market_date(article_datetime):
        published_date = article_datetime.date()

        if published_date.weekday() >= 5 or (published_date.weekday() == 4 and StockUtils.after_market_closed(article_datetime)):
            return StockUtils.get_next_monday(published_date)

        elif StockUtils.after_market_closed(article_datetime):
            return published_date + timedelta(days=1)

        return published_date

    @staticmethod
    def after_market_closed(article_datetime):
        et_market_close = time(16, 0)
        et_day_end = time(23, 59)

        utc_market_close = StockUtils.convert_ET_to_UTC(
            article_datetime.date(), et_market_close)
        utc_day_end = StockUtils.convert_ET_to_UTC(
            article_datetime.date(), et_day_end)
        utc_article_datetime = article_datetime.replace(tzinfo=pytz.utc)

        if utc_market_close < utc_article_datetime and utc_article_datetime <= utc_day_end:
            return True

        return False

    @staticmethod
    def convert_ET_to_UTC(date, time):
        et_datetime = datetime.combine(date, time)
        et_timezone = pytz.timezone('US/Eastern')
        utc_datetime = et_timezone.localize(et_datetime).astimezone(pytz.utc)
        return utc_datetime

    @staticmethod
    def get_next_monday(date):
        days_until_monday = (7 - date.weekday()) % 7
        next_monday = date + timedelta(days=days_until_monday)
        return next_monday

    @staticmethod
    def get_open_close(ticker, date):
        eod_data = StockUtils.get_eod_data(ticker, date)
        open_price, close_price = None, None

        if eod_data is not None and len(eod_data) > 0:
            open_price = eod_data[0]['open']
            close_price = eod_data[0]['close']
        return open_price, close_price

    @staticmethod
    def get_all_tickers():
        tickers = [
            "AAPL",
            "MSFT",
            "AMZN",
            "GOOGL",
            "TSLA",
            "JPM",
            "V",
            "FB",
            "NVDA",
            "NFLX",
            "DIS",
            "PYPL",
            "BA",
            "JNJ",
            "KO",
            "PFE",
            "AMD",
            "XOM",
            "T",
            "WMT",
        ]
        
        return tickers
