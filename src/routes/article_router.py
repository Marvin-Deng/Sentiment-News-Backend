"""
Router for handling article-related endpoints.
"""

from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from views import article_view
from models.response import ResponseModel

router = APIRouter()


@router.get("/news", response_model=ResponseModel)
async def get_news(
    page: int = Query(..., description="Page number", ge=0),
    search_query: str = Query(..., description="Search query"),
    tickers: str = Query(..., description="String of tickers"),
    sentiment: str = Query(..., description="Sentiment"),
    price_action: str = Query(..., description="Price action"),
    end_date: str = Query(..., description="Ending date of the filter"),
) -> ResponseModel:
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


@router.get("/process")
async def process_recent_articles() -> ResponseModel:
    """
    Route for article ingestion cron job.
    """
    return await article_view.process_articles()


@router.get("/remove")
async def delete_old_articles() -> ResponseModel:
    """
    Route for article removal cron job.
    """
    return await article_view.remove_articles()


@router.get("/sentiments")
def get_sentiments() -> JSONResponse:
    """
    Route for retrieving sentiment list.
    """
    return article_view.get_sentiments()
