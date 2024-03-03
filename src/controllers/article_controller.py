import logging
import traceback

from models.article_model import ArticleModel
from models.ticker_model import TickerModel
from utils.date_utils import DateUtils
from controllers.ticker_controller import TickerController
from utils.article_utils import ArticleUtils

logging.basicConfig(filename='error.log', level=logging.ERROR)


class ArticleController:

    @staticmethod
    async def create_article(article):
        existing_article = await ArticleModel.filter(article_id=article['id'])

        if existing_article:
            return "Duplicated Article", existing_article[0], 409

        try:
            article_data = ArticleUtils.get_article_info(article)
            _, ticker_object, _ = await TickerController.create_ticker(article_data['ticker'], article_data['publication_datetime'])

            new_article = ArticleModel(
                article_id=article_data['id'],
                title=article_data['title'],
                image_url=article_data['image_url'],
                article_url=article_data['url'],
                summary=article_data['summary'],
                ticker=ticker_object,
                publication_datetime=article_data['publication_datetime'],
                sentiment=article_data['sentiment']
            )
            await new_article.save()

        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            return "Internal Server Error Creating Articles", None, 500

        return "Created New Article", new_article, 201

    @staticmethod
    async def fetch_articles(search_params):
        try:
            response = await ArticleModel.get_paged_articles(search_params)
            return "Successfully queried articles", response, 200

        except Exception as e:
            error_message = f"Internal Service Error: {e}"
            logging.error(error_message)
            logging.error(traceback.format_exc())
            return error_message, [], 500

    @staticmethod
    async def remove_articles(one_week_ago_date):
        tickers = await TickerModel.filter(market_date=one_week_ago_date)

        for ticker in tickers:
            await ArticleModel.filter(ticker=ticker).delete()
            await ticker.delete()
