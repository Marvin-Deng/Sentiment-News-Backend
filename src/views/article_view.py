"""
Functions for processing requests and responses related to articles.
"""

import asyncio
from datetime import datetime, timedelta

from services import article_services
from services.async_wrapper import async_wrap_sync
from controllers import article_controller, ticker_controller
from models.response import Status, ArticleResponse, CronResponse, SentimentResponse
from utils.logging_utils import log_exception_error
from config.stock import TICKERS
from config.sentiment import SENTIMENT
from utils.logging_utils import logger
from models.ticker import TickerModel


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
        search_params = {
            "page": request_data["page"],
            "search_query": request_data["search_query"],
            "ticker_list": ticker_list,
            "sentiment": request_data["sentiment"],
            "price_action": request_data["price_action"],
            "end_date": request_data["end_date"],
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


async def ingest_articles() -> CronResponse:
    """
    Cron job for processing new articles daily.
    """
    try:
        date_today = datetime.today().strftime("%Y-%m-%d")
        titles = []
        processed = set()

        async def process_ticker_articles(ticker: str) -> None:
            """
            Processes all available articles for a ticker.
            """
            articles = await async_wrap_sync(
                article_services.get_articles_finnhub, ticker, date_today, date_today
            )

            async def add_article(article: dict, ticker_object: TickerModel) -> None:
                id = article["id"]
                if id not in processed:
                    processed.add(id)
                    title = await article_controller.create_article(
                        article=article, ticker_object=ticker_object
                    )
                    if title:
                        titles.append(title)

            valid_articles = [
                article for article in articles if article.get("image", "")
            ]
            if valid_articles:
                logger.info(f"Found {len(valid_articles)} articles for {ticker}")
                ticker_object = await ticker_controller.create_ticker(
                    ticker=ticker, publication_datetime=datetime.today()
                )
                tasks = [
                    add_article(article=article, ticker_object=ticker_object)
                    for article in valid_articles
                ]
                await asyncio.gather(*tasks)

        tasks = [process_ticker_articles(ticker) for ticker in TICKERS]
        await asyncio.gather(*tasks)
        message, data, rcode = "SUCCESS", titles, 200

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
        week_ago_str = datetime.today() - timedelta(days=8)
        week_ago_date = week_ago_str.strftime("%Y-%m-%d")
        message, data, rcode = await article_controller.remove_articles(week_ago_date)

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
