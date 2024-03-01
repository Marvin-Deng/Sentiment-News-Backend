import unittest
from datetime import datetime
from utils.date_utils import DateUtils


class TestDateUtils(unittest.TestCase):

    def test_convert_unix_to_utc(self):
        unix_timestamp = 1672444800
        self.assertEqual(DateUtils.convert_unix_to_utc(unix_timestamp), "2022-12-31 00:00:00")

    def test_convert_datetime_to_string_with_time(self):
        datetime_str = "2023-01-01 15:30:00"
        self.assertEqual(DateUtils.convert_datetime_to_string(datetime_str), "January 1, 2023 at 15:30 UTC")

    def test_convert_datetime_to_string_without_time(self):
        datetime_str = "2023-01-01 00:00:00"
        self.assertEqual(DateUtils.convert_datetime_to_string(datetime_str), "January 1, 2023")

if __name__ == "__main__":
    unittest.main()
