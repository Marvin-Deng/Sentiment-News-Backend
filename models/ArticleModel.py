from tortoise.models import Model
from tortoise.fields import (
    IntField, CharField, TextField, ForeignKeyField, CharEnumField
)
from enum import Enum
import re


class SentimentEnum(str, Enum):
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'


class ArticleModel(Model):
    id = IntField(pk=True, generated=True)
    article_id = IntField()
    title = TextField()
    image_url = TextField(null=True)
    article_url = TextField()
    summary = TextField()
    publication_datetime = CharField(max_length=100)
    ticker = ForeignKeyField('models.TickerModel')
    sentiment = CharEnumField(SentimentEnum, max_length=10)

    class Meta:
        table = "article_model"

    @classmethod
    async def get_paged_articles(cls, cursor, search_query, tickers_set, sentiment, price_action):
        PAGE_SIZE = 10
        filtered_articles = []
        keywords_set = cls.split_and_clean_string(search_query)

        while len(filtered_articles) < PAGE_SIZE:
            article = await cls.get_next_article(cursor)

            if not article:
                break

            ticker_obj = await article.ticker.first()
            ticker_string = ticker_obj.ticker.lower() if ticker_obj else ""
            open_price, close_price = ticker_obj.open_price, ticker_obj.close_price
            cursor += 1

            if (not cls.is_match_search_query(article.title, ticker_string, keywords_set) or
                    not cls.is_match_tickers(tickers_set, ticker_string) or
                    not cls.is_match_sentiment(sentiment, article.sentiment) or
                    not cls.is_match_price_action(price_action, open_price, close_price)):
                continue

            filtered_articles.append(article)

        return filtered_articles, cursor

    @staticmethod
    def is_match_search_query(title, ticker_string, keywords_set):
        if not keywords_set or ticker_string in keywords_set:
            return True

        title_words = ArticleModel.split_and_clean_string(title)
        return any(word in keywords_set for word in title_words)

    @staticmethod
    def is_match_tickers(tickers_set, ticker_string):
        return not tickers_set or ticker_string in tickers_set

    @staticmethod
    def is_match_sentiment(sentiment, article_sentiment):
        return not sentiment or article_sentiment.lower() == sentiment.lower()

    @staticmethod
    def is_match_price_action(price_action, open_price, close_price):
        return (not price_action or
                (price_action == "Positive" and open_price < close_price) or
                (price_action == "Negative" and open_price > close_price) or
                (price_action == "NA" and open_price is None and close_price is None))

    @staticmethod
    async def get_next_article(cursor):
        if cursor is None:
            cursor = 0

        next_article = await ArticleModel.all().offset(cursor).limit(1).first()
        return next_article

    @staticmethod
    def split_and_clean_string(input_string):
        pattern = re.compile(r'[^A-Za-z0-9_]')
        cleaned_query = re.sub(pattern, '', input_string).lower()
        words_array = re.findall(r'\b\w+\b', cleaned_query)
        return set(words_array)
