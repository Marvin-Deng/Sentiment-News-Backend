from controllers.ticker_controller import TickerController
import datetime


async def update_tickers():
    date_today = datetime.date.today().strftime("%Y-%m-%d")
    return await TickerController.update_tickers(date_today)
