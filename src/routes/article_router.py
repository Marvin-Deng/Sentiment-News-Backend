from fastapi import APIRouter, Query
from models.response_model import ResponseModel
from views.article_view import ArticleView
from fastapi.responses import JSONResponse
from constants.sentiment import SENTIMENT
from services.article_service import process_articles, remove_articles

router = APIRouter()


@router.get("/", response_model=ResponseModel)
async def get_articles(
    page: int = Query(..., description="Page number", ge=0),
    search_query: str = Query(..., description="Search query"),
    tickers: str = Query(..., description="String of tickers"),
    sentiment: str = Query(..., description="Sentiment"),
    price_action: str = Query(..., description="Price action"),
    start_date: str = Query(..., description="Starting date of the filter"),
    end_date: str = Query(..., description="Ending date of the filter"),
):
    return await ArticleView.get_articles(
        page, search_query, tickers, sentiment, price_action, start_date, end_date
    )


@router.get("/process")
async def process_recent_articles():
    return await process_articles()


@router.get("/remove")
async def delete_old_articles():
    return await remove_articles()


@router.get("/sentiments")
def get_sentiments():
    return JSONResponse(content=SENTIMENT)
