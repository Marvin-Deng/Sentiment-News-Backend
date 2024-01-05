from controllers.ArticleController import ArticleController
from models.ResponseModel import ResponseModel


class ArticleView:

    @staticmethod
    async def get_articles(cursor, search_query, tickers, sentiment, price_action):
        cursor = cursor or 0
        search_query = search_query or ""
        tickers_set = set(ticker.lower() for ticker in tickers.split(
            ',')) if tickers and any(tickers) else set()
        sentiment = sentiment or ""
        price_action = price_action or ""
        message, response, cursor, status = await ArticleController.fetch_articles(cursor, search_query, tickers_set, sentiment, price_action)
        return ResponseModel(message=message, articles=response, cursor=cursor, code=status)
