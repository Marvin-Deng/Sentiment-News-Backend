"""
Module for querying and updating article table.
"""

from models.article_model import ArticleModel
from models.ticker_model import TickerModel
from controllers import ticker_controller
from utils.article_utils import ArticleUtils
from utils.logging_utils import LoggingUtils


async def create_article(article: dict):
    """
    Adds a new article to the articles table.
    """
    existing_article = await ArticleModel.filter(article_id=article["id"])
    if existing_article:
        return "Creation failed, article already exists", existing_article[0], 409

    try:
        article_data = ArticleUtils.get_article_info(article)
        _, ticker_object, _ = await ticker_controller.create_ticker(
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
        return "Created new article", new_article, 201

    except Exception as e:
        error_message = "Error occured in article_controller.create_article"
        return LoggingUtils.log_error(e, error_message, None, 500)


async def fetch_articles(search_params: dict):
    """
    Fetch articles based on search parameters.
    """
    try:
        response = await ArticleModel.get_paged_articles(search_params)
        return "Successfully queried articles", response, 200

    except Exception as e:
        error_message = "Error occured in article_controller.fetch_articles"
        return LoggingUtils.log_error(e, error_message, [], 500)


async def remove_articles(one_week_ago_date: str):
    """
    Remove articles from a week ago.
    """
    try:
        tickers = await TickerModel.filter(market_date=one_week_ago_date)
        for ticker in tickers:
            await ArticleModel.filter(ticker=ticker).delete()
            await ticker.delete()
        return "Successfully removed articles from last week"

    except Exception as e:
        error_message = "Error occurred in article_controller.remove_articles"
        return LoggingUtils.log_error(e, error_message, None, 500)
