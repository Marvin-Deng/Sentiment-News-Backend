import unittest
from datetime import datetime
import pytz
from src.utils import stock_utils, date_utils


class TestStockUtils(unittest.TestCase):

    def test_market_open(self):
        mock_datetime = datetime(2023, 1, 1, 20, 0, tzinfo=pytz.utc)
        self.assertFalse(stock_utils._after_market_closed(mock_datetime))

    def test_market_closed(self):
        # Testing 10:00 PM UTC, after market close
        mock_datetime = datetime(2023, 1, 1, 22, 0, tzinfo=pytz.utc)
        self.assertTrue(stock_utils._after_market_closed(mock_datetime))

    def test_get_market_date(self):
        article_datetime = datetime(2023, 1, 1, 10, 0)  # A Sunday
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 2).date())


class TestDateUtils(unittest.TestCase):

    def test_convert_unix_to_utc(self):
        unix_timestamp = 1672444800
        self.assertEqual(
            date_utils.convert_unix_to_utc(unix_timestamp), "2022-12-31 00:00:00"
        )


if __name__ == "__main__":
    unittest.main()
