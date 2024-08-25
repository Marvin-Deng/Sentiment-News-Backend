"""
Module for querying and updating article table.
"""

from models.article import ArticleModel
from models.ticker import TickerModel
from controllers import ticker_controller
from utils import article_utils
from utils.logging_utils import logger, log_exception_error


async def create_article(article: dict) -> str:
    """
    Adds a new article to the article table.
    """
    existing_article = await ArticleModel.filter(article_id=article["id"]).first()
    if existing_article:
        logger.warning(
            f"Creation failed, article already exists: {existing_article.article_id}"
        )
        return

    try:
        article_data = article_utils.get_article_info(article)
        ticker_object = await ticker_controller.create_ticker(
            article_data["ticker"], article_data["publication_datetime"]
        )

        new_article = ArticleModel(
            article_id=article_data["id"],
            title=article_data["title"],
            image_url=article_data["image_url"],
            article_url=article_data["url"],
            summary=article_data["summary"],
            ticker=ticker_object,
            publication_datetime=article_data["publication_datetime"],
            sentiment=article_data["sentiment"],
        )
        await new_article.save()
        logger.info(f"New article created: {new_article.article_id}")
        return new_article.title

    except Exception as e:
        error_message = "Error occured in article_controller.create_article"
        log_exception_error(e, error_message, None, 500)


async def fetch_articles(search_params: dict) -> list:
    """
    Fetch articles based on search parameters.
    """
    try:
        response = await ArticleModel.get_paged_articles(search_params)
        return "Successfully queried articles", response, 200

    except Exception as e:
        error_message = "Error occured in article_controller.fetch_articles"
        return log_exception_error(e, error_message, [], 500)


async def remove_articles(one_week_ago_date: str) -> list:
    """
    Remove articles from a week ago.
    """
    try:
        tickers = await TickerModel.filter(market_date=one_week_ago_date)
        for ticker in tickers:
            await ArticleModel.filter(ticker=ticker).delete()
            await ticker.delete()
        return "Successfully removed articles from last week", tickers, 200

    except Exception as e:
        error_message = "Error occurred in article_controller.remove_articles"
        return log_exception_error(e, error_message, None, 500)
