import datetime

from utils.article_utils import ArticleUtils
from utils.logging_utils import LoggingUtils
from controllers.article_controller import ArticleController
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
    one_week_ago = datetime.date.today() - datetime.timedelta(days=6)
    one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
    return await ArticleController.remove_articles(one_week_ago_date)
