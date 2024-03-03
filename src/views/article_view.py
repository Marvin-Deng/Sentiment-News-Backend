import datetime

from controllers.article_controller import ArticleController
from models.response_model import ResponseModel


class ArticleView:

    @staticmethod
    async def get_articles(page, search_query, tickers, sentiment, price_action, start_date, end_date):
        search_query = search_query or ""
        sentiment = sentiment or ""
        price_action = price_action or ""

        if len(start_date) == 0 and len(end_date) == 0:
            start_date = "1970-01-01"
            end_date = datetime.date.today().strftime("%Y-%m-%d")

        tickers_list = tickers.split(',')
        if tickers_list == ['']:
            tickers_list = []

        search_params = {
            'page': page,
            'search_query': search_query,
            'tickers_list': tickers_list,
            'sentiment': sentiment,
            'price_action': price_action,
            'start_date': start_date,
            'end_date': end_date
        }

        message, response, status = await ArticleController.fetch_articles(search_params)
        return ResponseModel(message=message, articles=response, code=status)
