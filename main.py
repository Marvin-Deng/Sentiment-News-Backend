from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, Query
from typing import List
import os

from services.ArticleService import process_articles, remove_articles
from services.TickerService import update_tickers
from views.ArticleView import ArticleView
from utils.stock import StockUtils
from models.ResponseModel import ResponseModel
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
    await process_articles_job()
    schedule_background_tasks()


@app.get('/api/articles', response_model=ResponseModel)
async def get_articles(
    cursor: int = Query(..., description="Page number", ge=0),
    search_query: str = Query(..., description="Search query"),
    tickers: str = Query(..., description="String of tickers"),
    sentiment: str = Query(..., description="Sentiment"),
    price_action: str = Query(..., description="Price action"),
    start_date: str = Query(..., description="Starting date of the filter"),
    end_date: str = Query(..., description="Ending date of the filter"),
):
    return await ArticleView.get_articles(
        cursor=cursor,
        search_query=search_query,
        tickers=tickers,
        sentiment=sentiment,
        price_action=price_action,
        start_date=start_date,
        end_date=end_date
    )


@app.get('/api/tickers')
def get_tickers() -> List[str]:
    return StockUtils.get_all_tickers()


def schedule_background_tasks():
    scheduler = AsyncIOScheduler()
    # scheduler.add_job(process_articles_job, 'cron', hour=14, minute=0)
    # scheduler.add_job(update_tickers_job, 'cron', hour=14, minute=30)
    # scheduler.add_job(remove_articles_job, 'cron', hour=5, minute=0)
    scheduler.start()


async def process_articles_job():
    await process_articles()


async def update_tickers_job():
    await update_tickers()


async def remove_articles_job():
    await remove_articles()
