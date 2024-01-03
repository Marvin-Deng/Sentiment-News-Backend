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
    async def get_paged_articles(cls, page, search_query=None, tickers=None, sentiment=None):
        articles_list = await cls.all()

        filtered_articles = []

        for article in articles_list:
            if search_query and cls.is_match_search_query(article, search_query):
                if tickers and not cls.is_match_tickers(article.ticker, tickers):
                    continue
                if sentiment and article.sentiment != sentiment:
                    continue

            filtered_articles.append(article)

        page_size = 20
        start_index = (page - 1) * page_size
        end_index = start_index + page_size
        return filtered_articles[start_index:end_index]
        

    @staticmethod
    def is_match_search_query(article, keywords_set):
        title_words = re.findall(r'\b\w+\b', article.title.lower())
        for word in title_words:
            if word not in keywords_set:
                return False
        return True

    @staticmethod
    def is_match_tickers(tickers, keywords_set):
        for ticker in tickers:
            if ticker not in keywords_set:
                return False
        return True
