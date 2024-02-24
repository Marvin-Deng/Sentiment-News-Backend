from controllers.article_controller import ArticleController
from models.response_model import ResponseModel
import datetime


class ArticleView:

    @staticmethod
    async def get_articles(cursor, search_query, tickers, sentiment, price_action, start_date, end_date):

        # Set default values for the params
        cursor = cursor or 0
        search_query = search_query or ""
        sentiment = sentiment or ""
        price_action = price_action or ""
        if len(start_date) == 0 and len(end_date) == 0:
            start_date = "1970-01-01"
            end_date = datetime.date.today().strftime("%Y-%m-%d")

        # Convert ticker string to a set
        tickers_set = set()
        if tickers and any(tickers):
            for ticker in tickers.split(','):
                tickers_set.add(ticker.lower())

        message, response, cursor, status = await ArticleController.fetch_articles(cursor, search_query, tickers_set, sentiment, price_action, start_date, end_date)
        return ResponseModel(message=message, articles=response, cursor=cursor, code=status)
