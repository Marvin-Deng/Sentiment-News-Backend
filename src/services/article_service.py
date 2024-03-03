from utils.article_utils import ArticleUtils
from utils.stock_utils import StockUtils
from controllers.article_controller import ArticleController
import datetime


async def process_articles():
    try:
        date_today = datetime.date.today().strftime("%Y-%m-%d")

        tickers = StockUtils.get_all_tickers()

        for ticker in tickers:
            articles = ArticleUtils.get_articles(ticker, date_today, date_today)
            for article in articles:
                if (article['image']):
                    await ArticleController.create_article(article)
        return "Successfully processed articles"
    except Exception as e:
        return f"An error occurred in process_articles: {e}"


async def remove_articles():
    one_week_ago = datetime.date.today() - datetime.timedelta(days=6)
    one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
    return await ArticleController.remove_articles(one_week_ago_date)
