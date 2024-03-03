from models.ticker_model import TickerModel
from utils.stock_utils import StockUtils
import logging
import traceback

logging.basicConfig(filename='error.log', level=logging.ERROR)


class TickerController:

    @staticmethod
    async def create_ticker(ticker, publication_datetime):
        market_date = StockUtils.get_market_date(publication_datetime).strftime("%Y-%m-%d")

        existing_ticker = await TickerModel.filter(ticker=ticker, market_date=market_date)

        if existing_ticker:
            return "Ticker already exists", existing_ticker[0], 409

        try:
            stock_info = StockUtils.get_stock_info(ticker, market_date)
            new_ticker = TickerModel(
                ticker=ticker,
                market_date=market_date,
                **stock_info
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
            print(date_str)
            tickers = await TickerModel.filter(market_date=date_str)
            for ticker_model in tickers:
                stock_info = StockUtils.get_stock_info(ticker_model.ticker, date_str)
                if stock_info.get("open_price") == None:
                    continue
                ticker_model.ticker = stock_info.get("ticker")
                ticker_model.market_date = stock_info.get("market_date")
                for key, value in stock_info.items():
                    if hasattr(ticker_model, key):
                        setattr(ticker_model, key, value)
                await ticker_model.save()

            return "Successfully updated tickers", tickers, 200

        except Exception as e:
            logging.error(f"Exception: {e}")
            logging.error(traceback.format_exc())
            return f"Error occured when updating tickers: {e}", None, 500
