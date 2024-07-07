"""
Functions for retrieving info from third-party article APIs.
"""

import json
import finnhub
import requests

from constants.env_consts import FINNHUB_API_KEY, RAPID_API_KEY


def get_articles(ticker: str, date_from: str, date_to: str) -> list:
    """
    Retrieves company news articles from Finnhub for a given ticker and date range.
    """
    try:
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        return finnhub_client.company_news(ticker, _from=date_from, to=date_to)

    except Exception:
        return None


def get_sentiment(text: str) -> json:
    """
    Analyzes sentiment for a given text using RapidAPI's sentiment analysis API.
    """
    try:
        url = "https://sentiment-analysis9.p.rapidapi.com/sentiment"
        payload = [{"id": "1", "language": "en", "text": text}]
        headers = {
            "content-type": "application/json",
            "Accept": "application/json",
            "X-RapidAPI-Key": RAPID_API_KEY,
            "X-RapidAPI-Host": "sentiment-analysis9.p.rapidapi.com",
        }
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        return response.json()

    except Exception:
        return None
