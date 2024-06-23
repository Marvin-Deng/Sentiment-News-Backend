from datetime import datetime

from .date_utils import DateUtils
from gemini.gemini_model import gemini_analyze_sentiment
from services.article_services import get_sentiment

class ArticleUtils:

    @staticmethod
    def _api_extract_sentiment(sentiment_json):
        sentiment = "Neutral"
        try:
            predictions = sentiment_json[0].get("predictions")
            prediction = predictions[0].get("prediction")
            probability = predictions[0].get("probability")

            if probability is not None and probability < 0.6:
                sentiment = "Neutral"
            else:
                sentiment = prediction

        except (KeyError, IndexError):
            sentiment = "Neutral"

        return sentiment

    @staticmethod
    def _api_evaluate_sentiment(title, summary):

        summary_json = get_sentiment(summary)
        if summary_json:
            return ArticleUtils._api_extract_sentiment(summary_json)

        sentiment_json = get_sentiment(title)
        if sentiment_json:
            return ArticleUtils._api_extract_sentiment(sentiment_json)

        return "Neutral"

    @staticmethod
    def _evaluate_sentiment(title, summary):
        sentiment = gemini_analyze_sentiment(
            f"{title}: {summary}"
        ) or ArticleUtils._api_evaluate_sentiment(title, summary)
        return sentiment.title()

    @staticmethod
    def get_article_info(article):
        id = article["id"]
        title = article["headline"]
        publication_datetime = DateUtils.convert_unix_to_utc(article["datetime"])
        parsed_datetime = datetime.fromisoformat(publication_datetime)
        image_url = article["image"]
        url = article["url"]
        summary = article["summary"]
        ticker = article["related"]
        sentiment = ArticleUtils._evaluate_sentiment(title, summary)

        article_info = {
            "id": id,
            "title": title,
            "publication_datetime": parsed_datetime,
            "image_url": image_url,
            "url": url,
            "summary": summary,
            "ticker": ticker,
            "sentiment": sentiment,
        }

        return article_info
