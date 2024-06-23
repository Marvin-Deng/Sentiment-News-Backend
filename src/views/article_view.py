import datetime

from controllers.article_controller import ArticleController
from models.response_model import ResponseModel
from utils.article_utils import ArticleUtils
from utils.logging_utils import LoggingUtils
from constants.stock import TICKERS


async def process_articles():
    try:
        date_today = datetime.date.today().strftime("%Y-%m-%d")

        for ticker in TICKERS:
            articles = ArticleUtils.get_articles(ticker, date_today, date_today)
            for article in articles:
                if article["image"]:
                    await ArticleController.create_article(article)
        return "Successfully processed articles"

    except Exception as e:
        error_message = "An error occurred in services.process_articles"
        return LoggingUtils.log_error(e, error_message, None, 500)


async def remove_articles():
    one_week_ago = datetime.date.today() - datetime.timedelta(days=8)
    one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
    return await ArticleController.remove_articles(one_week_ago_date)


async def get_articles(page, search_query, tickers, sentiment, price_action, end_date):
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
    message, response, status = await ArticleController.fetch_articles(search_params)
    return ResponseModel(message=message, articles=response, code=status)
