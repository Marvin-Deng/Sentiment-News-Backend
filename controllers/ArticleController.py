from models.ArticleModel import ArticleModel, SentimentEnum
from models.TickerModel import TickerModel
from controllers.TickerController import TickerController
from utils.article import ArticleUtils
import logging
import traceback

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
                sentiment=SentimentEnum[article_data['sentiment'].upper()]
            )
            await new_article.save()

        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            return "Internal Server Error Creating Articles", None, 500

        return "Created New Article", new_article, 201

    @staticmethod
    async def fetch_articles(cursor, search_query, tickers_set, sentiment, price_action):
        try:
            article_models, cursor = await ArticleModel.get_paged_articles(cursor, search_query, tickers_set, sentiment, price_action)
            articles_list = await ArticleController.convert_articles_to_json(article_models)
            return "Successfully Queried Articles", articles_list, cursor, 200

        except Exception as e:
            error_message = f"Internal Service Error: {e}"
            logging.error(error_message)
            logging.error(traceback.format_exc())
            return error_message, [], 0, 500

    @staticmethod
    async def convert_articles_to_json(articles_list):
        articles_json_list = []
        for article_obj in articles_list:
            ticker_obj = await article_obj.ticker.first()

            article = {
                'title': article_obj.title,
                'image_url': article_obj.image_url,
                'article_url': article_obj.article_url,
                'summary': article_obj.summary,
                'ticker': ticker_obj.ticker,
                'publication_datetime': ArticleUtils.convert_datetime_to_string(article_obj.publication_datetime),
                'sentiment': article_obj.sentiment.value,
                'market_date': ticker_obj.market_date,
                'open_price': ticker_obj.open_price,
                'close_price': ticker_obj.close_price
            }
            articles_json_list.append(article)

        return articles_json_list

    @staticmethod
    async def remove_articles(one_week_ago_date):
        tickers = await TickerModel.filter(market_date=one_week_ago_date)

        for ticker in tickers:
            await ArticleModel.filter(ticker=ticker).delete()
            await ticker.delete()
