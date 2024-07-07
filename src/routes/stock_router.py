from fastapi import APIRouter, Query

import views.stock_view as stock_view
from services.stock_services import get_eod_data

router = APIRouter()


@router.get("/update")
async def update_recent_tickers():
    return await stock_view.update_tickers()


@router.get("/tinngo_stock_prices")
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
):
    return get_eod_data(ticker, start_date, end_date)


@router.get("/tickers")
def get_tickers():
    return stock_view.get_ticker_list()
