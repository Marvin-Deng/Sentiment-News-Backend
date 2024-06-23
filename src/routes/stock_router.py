from fastapi import APIRouter, Query

from constants.stock import TICKERS
from utils.stock_utils import StockUtils
from views.ticker_service import update_tickers

router = APIRouter()


@router.get("/update")
async def update_recent_tickers():
    return await update_tickers()


@router.get("/tinngo_stock_prices")
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
):
    return StockUtils.get_eod_data(ticker, start_date, end_date)

@router.get("/exchange")
async def get_exchange():
    return await StockUtils.get_stocks()

@router.get("/tickers")
def get_tickers():
    return TICKERS
