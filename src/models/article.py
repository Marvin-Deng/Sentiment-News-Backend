"""
Module for article table.
"""

import re
from tortoise.models import Model
from tortoise.transactions import in_transaction
from tortoise.fields import IntField, CharField, TextField, ForeignKeyField

from config.sentiment import SENTIMENT_MAP


class ArticleModel(Model):
    id = IntField(pk=True, generated=True)
    article_id = IntField()
    title = TextField()
    image_url = TextField(null=True)
    article_url = TextField()
    summary = TextField()
    publication_datetime = CharField(max_length=100)
    ticker = ForeignKeyField("models.TickerModel")
    sentiment = CharField(max_length=50)

    class Meta:
        table = "article_model"

    @classmethod
    async def get_paged_articles(cls, search_params):
        """
        Retrieves a page of articles based on search parameters.
        """
        page_size = 10
        keywords_list = cls._get_list_without_symbols(search_params["search_query"])
        sentiment_array = SENTIMENT_MAP.get(search_params["sentiment"], [])
        offset = search_params["page"] * page_size
        return await cls._get_articles(
            keywords=keywords_list,
            ticker_list=search_params["ticker_list"],
            sentiment_array=sentiment_array,
            price_action=search_params["price_action"],
            end_date=search_params["end_date"],
            offset=offset,
            page_size=page_size,
        )

    @staticmethod
    async def _get_articles(
        keywords,
        ticker_list,
        sentiment_array,
        price_action,
        end_date,
        offset,
        page_size,
    ):
        """
        Retrieves articles based on search filters.
        """
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
                    AND
                    ($5 = '' OR article_model.publication_datetime <= $5)
                ORDER BY publication_datetime DESC
                OFFSET $6
                LIMIT $7;
            """
            params = (
                keywords,
                ticker_list,
                sentiment_array,
                price_action,
                end_date,
                offset,
                page_size,
            )
            return await connection.execute_query_dict(query, params)

    @staticmethod
    def _get_list_without_symbols(input_string):
        """
        Removes symbols from a string.
        """
        words = input_string.split()
        processed_words = [re.sub(r"\W+", "", word.lower()) for word in words]
        return processed_words
