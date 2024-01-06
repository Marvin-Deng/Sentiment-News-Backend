from controllers.ArticleController import ArticleController
from models.ResponseModel import ResponseModel


class ArticleView:

    @staticmethod
    async def get_articles(cursor, search_query, tickers, sentiment, price_action):

        # Set default values for the params
        cursor = cursor or 0
        search_query = search_query or ""
        sentiment = sentiment or ""
        price_action = price_action or ""

        # Convert ticker string to a set
        tickers_set = set()
        if tickers and any(tickers):
            for ticker in tickers.split(','):
                tickers_set.add(ticker.lower())

        message, response, cursor, status = await ArticleController.fetch_articles(cursor, search_query, tickers_set, sentiment, price_action)
        return ResponseModel(message=message, articles=response, cursor=cursor, code=status)
