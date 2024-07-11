import unittest
from datetime import datetime
import pytz
from src.utils import stock_utils, date_utils


class TestStockUtilsAfterMarketClose(unittest.TestCase):
    def test_market_open(self):
        mock_datetime = datetime(2024, 7, 3, 20, 0, tzinfo=pytz.utc)
        self.assertFalse(stock_utils._after_market_closed(mock_datetime))

    def test_market_closed_after_10_utc(self):
        mock_datetime = datetime(2023, 1, 1, 22, 0, tzinfo=pytz.utc)
        self.assertTrue(stock_utils._after_market_closed(mock_datetime))


class TestStockUtilsNextMarketDate(unittest.TestCase):


    def test_next_market_date_on_weekday_before_market_close_is_same_day(self):
        article_datetime = datetime(2024, 7, 8, 15, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2024, 7, 8).date())

    def test_next_market_date_on_weekday_after_market_close_is_next_day(self):
        article_datetime = datetime(2024, 7, 8, 22, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2024, 7, 9).date())

    def test_next_market_date_on_saturday_is_monday(self):
        article_datetime = datetime(2023, 1, 7, 10, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 9).date())

    def test_next_market_date_on_friday_before_market_close_is_friday(self):
        article_datetime = datetime(2023, 1, 5, 15, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 5).date())

    def test_next_market_date_on_friday_after_market_close_is_monday(self):
        article_datetime = datetime(2023, 1, 6, 22, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 9).date())

    def test_next_market_date_on_market_holiday_is_day_after(self):
        article_datetime = datetime(2023, 1, 1, 10, 0)
        result_date = stock_utils.get_market_date(article_datetime)
        self.assertEqual(result_date, datetime(2023, 1, 2).date())


class TestDateUtilsConvertUnixToUtc(unittest.TestCase):

    def test_convert_unix_to_utc_with_system_timezone(self):
        unix_timestamp = 1672444800
        expected_utc_datetime = "2022-12-31 00:00:00"
        self.assertEqual(
            date_utils.convert_unix_to_utc(unix_timestamp), expected_utc_datetime
        )

    def test_convert_unix_to_utc_epoch_start(self):
        unix_timestamp = 0
        expected_utc_datetime = "1970-01-01 00:00:00"
        self.assertEqual(
            date_utils.convert_unix_to_utc(unix_timestamp), expected_utc_datetime
        )

    def test_convert_unix_to_utc_invalid_none_timestamp(self):
        invalid_unix_timestamp = None
        with self.assertRaises(TypeError):
            date_utils.convert_unix_to_utc(invalid_unix_timestamp)


if __name__ == "__main__":
    unittest.main()
