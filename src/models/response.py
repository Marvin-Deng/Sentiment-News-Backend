"""
Pydantic models for articles and response.
"""

from pydantic import BaseModel


class Status(BaseModel):
    rcode: int
    message: str


class Response(BaseModel):
    status: Status


class CronResponse(Response):
    num_returned: int
    processed: list


class SentimentResponse(Response):
    sentiment: dict


class TickerResponse(Response):
    tickers: list


class EodResponse(Response):
    eod_data: list


class ArticleResponse(Response):
    num_returned: int
    articles: list
