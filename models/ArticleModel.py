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
    async def get_paged_articles(cls, page, search_query, tickers, sentiment, price_action):
        filtered_articles = []
        keywords_set = cls.split_and_clean_string(search_query)
        tickers_set = set(ticker.lower() for ticker in tickers)
        page_size = 10
        cursor = 0

        while len(filtered_articles) < page_size:
            article = await cls.get_next_article(cursor)

            if not article:
                break

            ticker_obj = await article.ticker.first()
            ticker_string = ticker_obj.ticker.lower() if ticker_obj else ""
            cursor += 1
            if (keywords_set and not cls.is_match_search_query(article, ticker_string, keywords_set) or
                tickers_set and ticker_string not in tickers_set or
                sentiment and article.sentiment.lower() != sentiment.lower()):
                continue

            filtered_articles.append(article)

        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return filtered_articles[start_index:end_index]

    @staticmethod
    def is_match_search_query(article, ticker_string, keywords_set):
        if ticker_string in keywords_set:
            return True

        title_words = ArticleModel.split_and_clean_string(article.title)
        return any(word in keywords_set for word in title_words)

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
