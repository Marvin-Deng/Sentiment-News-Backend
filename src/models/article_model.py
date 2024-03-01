import re
from tortoise.models import Model
from tortoise.transactions import in_transaction
from tortoise.fields import (
    IntField, CharField, TextField, ForeignKeyField
)

from constants.sentiment import SENTIMENT_MAP


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
    async def get_paged_articles(cls, search_params):
        PAGE_SIZE = 10
        keywords_list = cls.get_list_without_symbols(search_params["search_query"])
        sentiment_array = SENTIMENT_MAP.get(search_params["sentiment"], [])
        offset = search_params['page'] * PAGE_SIZE
        return await cls.get_articles(keywords_list, search_params["tickers_list"], sentiment_array, search_params["price_action"], offset, PAGE_SIZE)

    @staticmethod
    async def get_articles(keywords, tickers_list, sentiment_array, price_action, offset, page_size):
        async with in_transaction() as connection:
            query = """
                SELECT 
                    article_model.title,
                    article_model.image_url,
                    article_model.article_url,
                    article_model.summary,
                    article_model.publication_datetime,
                    article_model.sentiment,
                    ticker_model.ticker,
                    ticker_model.market_date,
                    ticker_model.open_price,
                    ticker_model.close_price
                FROM 
                    article_model
                JOIN ticker_model ON ticker_id::INTEGER = ticker_model.id::INTEGER
                WHERE
                    ($1::text[] = '{}' OR string_to_array(LOWER(title), ' ') && $1::text[])
                    AND
                    ($2::text[] = '{}' OR ticker_model.ticker = ANY($2::text[]))
                    AND
                    ($3::text[] = '{}' OR sentiment = ANY($3::text[]))
                    AND
                    (
                        $4 = ''
                        OR
                        (
                            ticker_model.open_price IS NOT NULL AND ticker_model.close_price IS NOT NULL AND (
                                ($4 = 'Positive' AND ticker_model.open_price < close_price)
                                OR
                                ($4 = 'Negative' AND ticker_model.open_price > close_price)
                            )
                        )
                        OR
                        (
                            (ticker_model.open_price IS NULL OR ticker_model.close_price IS NULL) AND $4 = 'NA'
                        )
                    )
                OFFSET $5
                LIMIT $6;
            """
            params = (keywords, tickers_list, sentiment_array, price_action, offset, page_size)
            return await connection.execute_query_dict(query, params)

    @staticmethod
    def get_list_without_symbols(input_string):
        words = input_string.split()
        processed_words = [re.sub(r'\W+', '', word.lower()) for word in words]
        return processed_words
