from controllers.ArticleController import ArticleController
from models.ResponseModel import ResponseModel

class ArticleView:

    @staticmethod
    async def get_articles(page, search_query, tickers, sentiment, price_action):
        search_query = search_query or ""
        tickers = [] if not tickers or tickers == [''] else tickers
        sentiment = sentiment or ""
        price_action = price_action or ""
        message, response, status = await ArticleController.fetch_articles(1 if page <= 0 else page, search_query, tickers, sentiment, price_action)
        return ResponseModel(message=message, articles=response, code=status)