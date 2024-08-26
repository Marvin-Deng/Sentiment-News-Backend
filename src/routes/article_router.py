"""
Router for handling article-related endpoints.
"""

from fastapi import APIRouter, Query

from views import article_view
from models.response import ArticleResponse, CronResponse, SentimentResponse

router = APIRouter()


@router.get("/news", response_model=ArticleResponse)
async def get_news(
    page: int = Query(..., description="Page number", ge=0),
    search_query: str = Query(..., description="Search query"),
    tickers: str = Query(..., description="String of tickers"),
    sentiment: str = Query(..., description="Sentiment"),
    price_action: str = Query(..., description="Price action"),
    end_date: str = Query(..., description="Ending date of the filter"),
):
    """
    Route for retrieving filtered news articles based on query parameters.
    """
    request_data = {
        "page": page,
        "search_query": search_query,
        "tickers": tickers,
        "sentiment": sentiment,
        "price_action": price_action,
        "end_date": end_date,
    }
    return await article_view.get_articles(request_data)


@router.post("/news", response_model=CronResponse)
async def ingest_recent_articles():
    """
    Route for article ingestion cron job.
    """
    return await article_view.ingest_articles()


@router.delete("/news", response_model=CronResponse)
async def delete_old_articles():
    """
    Route for article deletion cron job.
    """
    return await article_view.remove_articles()


@router.get("/sentiments", response_model=SentimentResponse)
def get_sentiments():
    """
    Route for retrieving sentiment list.
    """
    return article_view.get_sentiments()
