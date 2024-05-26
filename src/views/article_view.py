import datetime

from controllers.article_controller import ArticleController
from models.response_model import ResponseModel


class ArticleView:

    @staticmethod
    async def get_articles(
        page, search_query, tickers, sentiment, price_action, end_date
    ):
        ticker_list = tickers.split(",") if len(tickers) != 0 else []
        if len(end_date) == 0:
            end_date = datetime.date.today().strftime("%Y-%m-%d")
        search_params = {
            "page": page,
            "search_query": search_query,
            "ticker_list": ticker_list,
            "sentiment": sentiment,
            "price_action": price_action,
            "end_date": end_date,
        }
        message, response, status = await ArticleController.fetch_articles(
            search_params
        )
        return ResponseModel(message=message, articles=response, code=status)
