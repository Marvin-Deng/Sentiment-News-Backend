"""
Functions for processing requests and responses related to articles.
"""

import asyncio
import datetime
from fastapi.responses import JSONResponse

from services import article_services
from controllers import article_controller
from models.response import ResponseModel
from utils import logging_utils
from constants.stock import TICKERS
from constants.sentiment import SENTIMENT


async def get_articles(request_data: dict) -> ResponseModel:
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

        message, data, status = await article_controller.fetch_articles(search_params)

    except Exception as e:
        error_message = "An error occurred in article_view.get_articles"
        message, data, status = logging_utils.log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return ResponseModel(message=message, data=data, status=status)


async def process_articles() -> ResponseModel:
    """
    Cron job for processing new articles daily.
    """
    try:
        date_today = datetime.date.today().strftime("%Y-%m-%d")
        titles = []

        async def process_ticker_articles(ticker: str) -> None:
            """
            Processes all available articles for a ticker.
            """
            articles = article_services.get_articles(ticker, date_today, date_today)

            async def add_article(article: dict) -> None:
                await article_controller.create_article(article)
                title = article.get("title", "")
                if title:
                    titles.append(title)

            tasks = [
                add_article(article) for article in articles if article.get("image", "")
            ]
            if tasks:
                await asyncio.gather(*tasks)

        tasks = [process_ticker_articles(ticker) for ticker in TICKERS]
        await asyncio.gather(*tasks)

        message, data, status = (
            "Successfully processed articles",
            titles,
            200,
        )

    except Exception as e:
        error_message = "An error occurred in article_view.process_articles"
        message, data, status = logging_utils.log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return ResponseModel(message=message, data=data, status=status)


async def remove_articles() -> ResponseModel:
    """
    Cron job for removing outdated articles every week.
    """
    try:
        one_week_ago = datetime.date.today() - datetime.timedelta(days=8)
        one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
        message, data, status = await article_controller.remove_articles(
            one_week_ago_date
        )

    except Exception as e:
        error_message = "An error occurred in article_view.remove_articles"
        message, data, status = logging_utils.log_exception_error(
            error=e, message=error_message, data=[], status=500
        )

    return ResponseModel(message=message, data=data, status=status)


def get_sentiments() -> JSONResponse:
    """
    Retrieves a sentiment json constants.
    """
    return JSONResponse(content=SENTIMENT)
