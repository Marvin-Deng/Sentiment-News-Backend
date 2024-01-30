from utils.article import ArticleUtils
from utils.stock import StockUtils
from controllers.ArticleController import ArticleController
import datetime


async def process_articles():
    date_today = datetime.date.today().strftime("%Y-%m-%d")

    tickers = StockUtils.get_all_tickers()

    for ticker in tickers:
        articles = ArticleUtils.get_articles(ticker, date_today, date_today)
        for article in articles:
            if (article['image']):
                await ArticleController.create_article(article)


async def remove_articles():
    one_week_ago = datetime.date.today() - datetime.timedelta(days=6)
    one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
    await ArticleController.remove_articles(one_week_ago_date)
