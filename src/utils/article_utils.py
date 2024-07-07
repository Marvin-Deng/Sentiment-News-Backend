"""
Module with article utility functions for parsing and sentiment analysis.
"""

from datetime import datetime

from utils.date_utils import convert_unix_to_utc
from gemini.gemini_model import gemini_analyze_sentiment
from services import article_services


def get_article_info(article: dict) -> dict:
    """
    Parses and analyzes the fields of a Funnhub article object.
    """
    title, summary = article["headline"], article["summary"]
    sentiment = _evaluate_sentiment(title, summary)

    article_info = {
        "id": article["id"],
        "title": title,
        "publication_datetime": datetime.fromisoformat(
            convert_unix_to_utc(article["datetime"])
        ),
        "image_url": article["image"],
        "url": article["url"],
        "summary": summary,
        "ticker": article["related"],
        "sentiment": sentiment,
    }

    return article_info


def _evaluate_sentiment(title: str, summary: str) -> str:
    """
    Evaluates the sentiment of an article using either Gemini or RapidAPI.
    """
    sentiment = gemini_analyze_sentiment(
        f"{title}: {summary}"
    ) or _api_evaluate_sentiment(title, summary)

    return sentiment.title()


def _api_evaluate_sentiment(title: str, summary: str) -> str:
    """
    Evaluates the sentiment of an article using RapidAPI.
    """
    summary_json = article_services.get_sentiment(summary)
    if summary_json:
        return _api_extract_sentiment(summary_json)

    sentiment_json = article_services.get_sentiment(title)
    if sentiment_json:
        return _api_extract_sentiment(sentiment_json)

    return "Neutral"


def _api_extract_sentiment(sentiment_json: dict) -> str:
    """
    Returns a sentiment string from the confidence returned by RapidAPI.
    """
    sentiment = "Neutral"

    try:
        predictions = sentiment_json[0].get("predictions")
        prediction = predictions[0].get("prediction")
        probability = predictions[0].get("probability")
        if probability is not None and probability < 0.6:
            sentiment = "Neutral"
        else:
            sentiment = prediction

    except KeyError:
        sentiment = "Neutral"

    return sentiment
