import re
from tortoise.models import Model
from tortoise.fields import (
    IntField, CharField, TextField, ForeignKeyField
)

from utils.date import DateUtils


class ArticleModel(Model):
    id = IntField(pk=True, generated=True)
    article_id = IntField()
    title = TextField()
    image_url = TextField(null=True)
    article_url = TextField()
    summary = TextField()
    publication_datetime = CharField(max_length=100)
    ticker = ForeignKeyField('models.TickerModel')
    sentiment = CharField(max_length=50)

    class Meta:
        table = "article_model"

    @classmethod
    async def get_paged_articles(cls, cursor, search_query, tickers_set, sentiment, price_action, start_date, end_date):
        PAGE_SIZE = 10
        filtered_articles = []
        keywords_set = set(cls.get_list_without_symbols(search_query))

        while len(filtered_articles) < PAGE_SIZE:
            cursor += 1
            article = await cls.get_next_article(cursor)

            if not article:
                return [], 0

            # Extract ticker fields for the article
            ticker_string, open_price, close_price, market_date = await cls.get_ticker_fields(article)

            if not cls.is_match_search_query(article.title, ticker_string, keywords_set):
                continue

            if not cls.is_match_tickers(tickers_set, ticker_string):
                continue

            if not cls.is_match_sentiment(sentiment, article.sentiment):
                continue

            if not cls.is_match_price_action(price_action, open_price, close_price):
                continue

            if not cls.in_date_range(market_date, start_date, end_date):
                continue

            # Add an article when it matches the search condition
            filtered_articles.append(article)

        return filtered_articles, cursor

    @staticmethod
    def is_match_search_query(title, ticker_string, keywords_set):
        if not keywords_set or ticker_string in keywords_set:
            return True

        title_words = ArticleModel.get_list_without_symbols(title)
        return any(word in keywords_set for word in title_words)

    @staticmethod
    def is_match_tickers(tickers_set, ticker_string):
        return not tickers_set or ticker_string in tickers_set

    @staticmethod
    def is_match_sentiment(sentiment, article_sentiment):
        return not sentiment or article_sentiment.lower() == sentiment.lower()

    @staticmethod
    def is_match_price_action(price_action, open_price, close_price):
        if not price_action:
            return True

        if open_price and close_price:
            return ((price_action == "Positive" and open_price < close_price) or
                    (price_action == "Negative" and open_price > close_price))

        return price_action == "NA"

    @staticmethod
    def in_date_range(market_date, start_date, end_date):
        market_date_obj = DateUtils.convert_string_to_datetime(market_date)
        start_date_obj = DateUtils.convert_string_to_datetime(start_date)
        end_date_obj = DateUtils.convert_string_to_datetime(end_date)

        return start_date_obj <= market_date_obj <= end_date_obj

    @staticmethod
    async def get_next_article(cursor):
        return await ArticleModel.filter().offset(cursor).limit(1).first()

    @staticmethod
    async def get_ticker_fields(article):
        ticker_obj = await article.ticker.first()
        ticker_string = ticker_obj.ticker.lower() if ticker_obj else ""
        open_price, close_price = ticker_obj.open_price, ticker_obj.close_price
        market_date = ticker_obj.market_date
        return ticker_string, open_price, close_price, market_date

    @staticmethod
    def get_list_without_symbols(input_string):
        words = input_string.split()
        processed_words = [re.sub(r'\W+', '', word.lower()) for word in words]
        return processed_words
