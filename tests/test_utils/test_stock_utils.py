import unittest
from unittest.mock import patch
from datetime import datetime
import pytz

from utils.stock_utils import StockUtils


class TestStockUtils(unittest.TestCase):

    def test_market_open(self):
        mock_datetime = datetime(2023, 1, 1, 20, 0, tzinfo=pytz.utc)
        self.assertFalse(StockUtils.after_market_closed(mock_datetime))

    def test_market_closed(self):
        # Testing 10:00 PM UTC, after market close
        mock_datetime = datetime(2023, 1, 1, 22, 0, tzinfo=pytz.utc)
        self.assertTrue(StockUtils.after_market_closed(mock_datetime))

    @patch("utils.stock.StockUtils.after_market_closed")
    def test_get_market_date(self, mock_after_market_closed):
        mock_after_market_closed.return_value = False
        article_datetime = datetime(2023, 1, 1, 10, 0)  # A Sunday
        result_date = StockUtils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 2).date())

    @patch("utils.stock.requests.get")
    def test_get_eod_data_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = [
            {
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
                "volume": 10000,
                "adjOpen": 100,
                "adjHigh": 110,
                "adjLow": 90,
                "adjClose": 105,
                "adjVolume": 10000,
                "divCash": 0.5,
                "splitFactor": 1,
            }
        ]
        mock_get.return_value = mock_response

        result = StockUtils.get_eod_data("AAPL", "2023-01-01", "2023-01-01")

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertDictEqual(
            result[0],
            {
                "open": 100,
                "high": 110,
                "low": 90,
                "close": 105,
                "volume": 10000,
                "adjOpen": 100,
                "adjHigh": 110,
                "adjLow": 90,
                "adjClose": 105,
                "adjVolume": 10000,
                "divCash": 0.5,
                "splitFactor": 1,
            },
        )


if __name__ == "__main__":
    unittest.main()
