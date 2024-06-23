from fastapi import APIRouter, Query

from constants.stock import TICKERS
from views.stock_view import StockView
from services.stock_services import get_eod_data

router = APIRouter()


@router.get("/update")
async def update_recent_tickers():
    return await StockView.update_tickers()


@router.get("/tinngo_stock_prices")
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
):
    return get_eod_data(ticker, start_date, end_date)


@router.get("/tickers")
def get_tickers():
    return TICKERS
