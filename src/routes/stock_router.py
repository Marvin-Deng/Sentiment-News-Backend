"""
Router for handling stock-related endpoints.
"""

from fastapi import APIRouter, Query

from views import stock_view
from models.response import EodResponse, CronResponse, TickerResponse

router = APIRouter()


@router.get("/tinngo_eod", response_model=EodResponse)
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
):
    """
    Route for retrieving EOD stock data from Tinngo.
    """
    return stock_view.get_eod_data(ticker, start_date, end_date)


@router.patch("/tickers", response_model=CronResponse)
async def update_recent_tickers():
    """
    Route for ticker price update cron job.
    """
    return await stock_view.update_tickers()


@router.get("/tickers", response_model=TickerResponse)
def get_tickers():
    """
    Route for retrieving a list of ticker options.
    """
    return stock_view.get_ticker_list()
