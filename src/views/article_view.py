"""
Functions for processing requests and responses related to articles.
"""

import asyncio
import datetime

from services import article_services
from services.async_services import async_wrap_sync
from controllers import article_controller
from models.response import Status, ArticleResponse, CronResponse, SentimentResponse
from utils.logging_utils import log_exception_error
from constants.stock import TICKERS
from constants.sentiment import SENTIMENT


async def get_articles(request_data: dict) -> ArticleResponse:
    """
    Retrieves filtered news articles.
    """
    try:
        ticker_list = (
            request_data["tickers"].split(",")
            if len(request_data["tickers"]) != 0
            else []
        )
        end_date = request_data["end_date"]
        if len(end_date) == 0:
            end_date = datetime.date.today().strftime("%Y-%m-%d")

        search_params = {
            "page": request_data["page"],
            "search_query": request_data["search_query"],
            "ticker_list": ticker_list,
            "sentiment": request_data["sentiment"],
            "price_action": request_data["price_action"],
            "end_date": end_date,
        }

        message, data, rcode = await article_controller.fetch_articles(search_params)

    except Exception as e:
        error_message = "An error occurred in article_view.get_articles"
        message, data, rcode = log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return ArticleResponse(
        status=Status(message=message, rcode=rcode),
        num_returned=len(data),
        articles=data,
    )


async def process_articles() -> CronResponse:
    """
    Cron job for processing new articles daily.
    """
    try:
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        titles = []
        processed = set()

        async def process_ticker_articles(ticker: str) -> None:
            """
            Processes all available articles for a ticker.
            """
            articles = await async_wrap_sync(
                article_services.get_articles, ticker, date_today, date_today
            )

            async def add_article(article: dict) -> None:
                id = article["id"]
                if id not in processed:
                    processed.add(id)
                    title = await article_controller.create_article(article)
                    if title:
                        titles.append(title)

            tasks = [
                add_article(article) for article in articles if article.get("image", "")
            ]
            if tasks:
                await asyncio.gather(*tasks)

        tasks = [process_ticker_articles(ticker) for ticker in TICKERS]
        await asyncio.gather(*tasks)

        message, data, rcode = (
            "Successfully processed articles",
            titles,
            200,
        )

    except Exception as e:
        error_message = "An error occurred in article_view.process_articles"
        message, data, rcode = log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return CronResponse(
        status=Status(message=message, rcode=rcode),
        num_returned=len(data),
        processed=data,
    )


async def remove_articles() -> CronResponse:
    """
    Cron job for removing outdated articles every week.
    """
    try:
        one_week_ago = datetime.date.today() - datetime.timedelta(days=8)
        one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
        message, data, rcode = await article_controller.remove_articles(
            one_week_ago_date
        )

    except Exception as e:
        error_message = "ERROR in article_view.remove_articles"
        message, data, rcode = log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return CronResponse(
        status=Status(message=message, rcode=rcode),
        num_returned=len(data),
        processed=data,
    )


def get_sentiments() -> SentimentResponse:
    """
    Retrieves a sentiment json constants.
    """
    return SentimentResponse(
        status=Status(message="SUCCESS", rcode=200),
        sentiment=SENTIMENT,
    )
