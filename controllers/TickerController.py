from models.TickerModel import TickerModel
from utils.stock import StockUtils
import logging
import traceback

logging.basicConfig(filename='error.log', level=logging.ERROR)


class TickerController:

    @staticmethod
    async def create_ticker(ticker, publication_datetime):
        market_date = StockUtils.get_market_date(
            publication_datetime).strftime("%Y-%m-%d")

        existing_ticker = await TickerModel.filter(ticker=ticker, market_date=market_date)

        if existing_ticker:
            return "Ticker already exists", existing_ticker[0], 409

        try:
            open_price, close_price = StockUtils.get_open_close(
                ticker, market_date)
            new_ticker = TickerModel(
                ticker=ticker,
                market_date=market_date,
                open_price=open_price,
                close_price=close_price
            )
            await new_ticker.save()

        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            return "Internal Server Error Creating Tickers", None, 500

        return "Created New Ticker", new_ticker, 201

    @staticmethod
    async def update_tickers(date_str):
        try:
            tickers = await TickerModel.filter(market_date=date_str)
            for ticker_model in tickers:
                open_price, close_price = StockUtils.get_open_close(
                    ticker_model.ticker, date_str)
                ticker_model.open_price = open_price
                ticker_model.close_price = close_price
                await ticker_model.save()

            return "Updated tickers", tickers, 200

        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            return "Internal Server Error Updating Tickers", None, 500
