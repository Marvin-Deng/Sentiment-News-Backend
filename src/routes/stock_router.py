"""
Router for handling stock-related endpoints.
"""

from fastapi import APIRouter, Query

from views import stock_view

router = APIRouter()


@router.get("/tinngo_stock_prices")
def get_tinngo_stock(
    ticker: str = Query(..., description="Ticker string"),
    start_date: str = Query(..., description="Starting date"),
    end_date: str = Query(..., description="Ending date"),
) -> dict:
    """
    Route for retrieving EOD stock data from Tinngo.
    """
    return stock_view.get_eod_data(ticker, start_date, end_date)


@router.get("/update")
async def update_recent_tickers():
    """
    Route for price action update cron job.
    """
    return await stock_view.update_tickers()


@router.get("/tickers")
def get_tickers() -> list:
    """
    Retrieves a list of available tickers.
    """
    return stock_view.get_ticker_list()
