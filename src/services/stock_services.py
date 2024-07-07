import finnhub
import requests

from constants.env_consts import TINNGO_API_KEY


def get_eod_data(ticker, start_date, end_date):
    try:
        url = f"https://api.tiingo.com/tiingo/daily/{ticker}/prices?startDate={start_date}&endDate={end_date}&token={TINNGO_API_KEY}"
        headers = {"Content-Type": "application/json"}
        response = requests.get(url, headers=headers)
        return response.json()

    except Exception:
        return None
