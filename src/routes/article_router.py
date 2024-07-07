from fastapi import APIRouter, Query
from fastapi.responses import JSONResponse

from models.response_model import ResponseModel
from views.article_view import ArticleView
from constants.sentiment import SENTIMENT

router = APIRouter()


@router.get("/news", response_model=ResponseModel)
async def get_news(
    page: int = Query(..., description="Page number", ge=0),
    search_query: str = Query(..., description="Search query"),
    tickers: str = Query(..., description="String of tickers"),
    sentiment: str = Query(..., description="Sentiment"),
    price_action: str = Query(..., description="Price action"),
    end_date: str = Query(..., description="Ending date of the filter"),
):
    return await ArticleView.get_articles(
        page=page,
        search_query=search_query,
        tickers=tickers,
        sentiment=sentiment,
        price_action=price_action,
        end_date=end_date,
    )


@router.get("/sentiments")
def get_sentiments():
    return JSONResponse(content=SENTIMENT)


@router.get("/process")
async def process_recent_articles():
    return await ArticleView.process_articles()


@router.get("/remove")
async def delete_old_articles():
    return await ArticleView.remove_articles()
