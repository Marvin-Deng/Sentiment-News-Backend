import finnhub
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

from .date_utils import DateUtils
from gemini.gemini_model import gemini_analyze_sentiment

load_dotenv()


class ArticleUtils:

    @staticmethod
    def get_articles(ticker, date_from, date_to):
        try:
            finnhub_client = finnhub.Client(api_key=os.getenv("FINNHUB_API_KEY"))
            return finnhub_client.company_news(ticker, _from=date_from, to=date_to)

        except Exception:
            return None

    @staticmethod
    def extract_text(article_url):
        try:
            base_url = "https://text-extract7.p.rapidapi.com/"

            querystring = {"url": article_url}

            headers = {
                "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
                "X-RapidAPI-Host": "text-extract7.p.rapidapi.com"
            }

            response = requests.get(
                base_url, headers=headers, params=querystring)
            json_data = response.json()
            return json_data.get('raw_text')

        except Exception:
            return None

    @staticmethod
    def get_sentiment(text):
        try:
            url = "https://sentiment-analysis9.p.rapidapi.com/sentiment"

            payload = [
                {
                    "id": "1",
                    "language": "en",
                    "text": text
                }
            ]
            headers = {
                "content-type": "application/json",
                "Accept": "application/json",
                "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
                "X-RapidAPI-Host": "sentiment-analysis9.p.rapidapi.com"
            }

            response = requests.post(url, json=payload, headers=headers)
            return response.json()

        except Exception:
            return None

    @staticmethod
    def api_extract_sentiment(sentiment_json):
        sentiment = "Neutral"
        try:
            predictions = sentiment_json[0].get('predictions')
            prediction = predictions[0].get('prediction')
            probability = predictions[0].get('probability')

            if probability is not None and probability < 0.6:
                sentiment = "Neutral"
            else:
                sentiment = prediction

        except (KeyError, IndexError):
            sentiment = "Neutral"

        return sentiment

    @staticmethod
    def api_evaluate_sentiment(title, summary):

        summary_json = ArticleUtils.get_sentiment(summary)
        if (summary_json):
            return ArticleUtils.api_extract_sentiment(summary_json)

        sentiment_json = ArticleUtils.get_sentiment(title)
        if (sentiment_json):
            return ArticleUtils.api_extract_sentiment(sentiment_json)

        return "Neutral"

    @staticmethod
    def evaluate_sentiment(title, summary):
        sentiment = gemini_analyze_sentiment(f"{title}: {summary}") or ArticleUtils.api_evaluate_sentiment(title, summary)
        return sentiment.title()

    @staticmethod
    def get_article_info(article):
        id = article['id']
        title = article['headline']
        publication_datetime = DateUtils.convert_unix_to_utc(article['datetime'])
        parsed_datetime = datetime.fromisoformat(publication_datetime)
        image_url = article['image']
        url = article['url']
        summary = article['summary']
        ticker = article['related']
        sentiment = ArticleUtils.evaluate_sentiment(title, summary)

        article_info = {
            "id": id,
            "title": title,
            "publication_datetime": parsed_datetime,
            "image_url": image_url,
            "url": url,
            "summary": summary,
            "ticker": ticker,
            "sentiment": sentiment
        }

        return article_info
