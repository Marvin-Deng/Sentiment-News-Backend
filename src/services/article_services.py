"""
Functions for retrieving info from third-party article APIs.
"""

import finnhub
import requests
import google.generativeai as genai

from constants.env_consts import FINNHUB_API_KEY, RAPID_API_KEY, GEMINI_API_KEY
from constants.sentiment import SENTIMENT_OPTIONS
from utils.logging_utils import logger

genai.configure(api_key=GEMINI_API_KEY)
MODEL = genai.GenerativeModel("gemini-pro")


def get_articles_finnhub(ticker: str, date_from: str, date_to: str) -> list:
    """
    Retrieves company news articles from Finnhub for a given ticker and date range.
    """
    try:
        finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)
        return finnhub_client.company_news(ticker, _from=date_from, to=date_to)

    except Exception as e:
        logger.error(
            f"Error when getting company news from Finnhub ticker={ticker}, date_from={date_from}, date_to={date_to}: {e}"
        )
        return []


def get_sentiment_gemini(text: str) -> str:
    """
    Analyzes the sentiment of the provided text using Gemini.
    """
    try:
        prompt = (
            f"Analyze the sentiment of the following text using only one of the following: "
            f"{SENTIMENT_OPTIONS}. {text}"
        )
        response = MODEL.generate_content(prompt)
        return response.text

    except Exception as e:
        logger.error(f"Error when getting sentiment with Gemini: {e}")
        return ""


def get_sentiment_fastapi(text: str) -> dict:
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

    except Exception as e:
        logger.error(f"Error when getting sentiment with FastAPI: {e}")
        return ""
