from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from typing import List
import os

from services.article_service import process_articles, remove_articles
from services.ticker_service import update_tickers
from views.article_view import ArticleView
from utils.stock_utils import StockUtils
from models.response_model import ResponseModel
from db import init_db


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv('CLIENT_URL'), "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():
    await init_db()


@app.get('/api/articles', response_model=ResponseModel)
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
        page=page,
        search_query=search_query,
        tickers=tickers,
        sentiment=sentiment,
        price_action=price_action,
        start_date=start_date,
        end_date=end_date
    )


@app.get('/api/article/process')
async def process_recent_articles():
    return await process_articles()


@app.get('/api/article/remove')
async def delete_old_articles():
    return await remove_articles()


@app.get('/api/stock/update')
async def update_recent_tickers():
    return await update_tickers()


@app.get('/api/stock/tinngo_stock_prices')
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
):
    return StockUtils.get_eod_data(ticker, start_date, end_date)


@app.get('/api/stock/tickers')
def get_tickers() -> List[str]:
    return StockUtils.get_all_tickers()
