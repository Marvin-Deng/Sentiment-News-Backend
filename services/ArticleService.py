from utils.article import ArticleUtils
from controllers.ArticleController import ArticleController
import datetime


async def process_articles():
    date_today = datetime.date.today().strftime("%Y-%m-%d")

    tickers = [
        "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "JPM", "V", "FB", "NVDA", "NFLX",
        "DIS", "PYPL", "BA", "JNJ", "KO", "PFE", "AMD", "XOM", "T", "WMT"
    ]

    for ticker in tickers:
        articles = ArticleUtils.get_articles(ticker, date_today, date_today)
        for article in articles:
            if (article['image']):
                await ArticleController.create_article(article)


async def remove_articles():
    one_week_ago = datetime.date.today() - datetime.timedelta(days=6)
    one_week_ago_date = one_week_ago.strftime("%Y-%m-%d")
    await ArticleController.remove_articles(one_week_ago_date)
