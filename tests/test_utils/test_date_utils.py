import unittest

from utils import date_utils


class TestDateUtils(unittest.TestCase):

    def test_convert_unix_to_utc(self):
        unix_timestamp = 1672444800
        self.assertEqual(
            date_utils.convert_unix_to_utc(unix_timestamp), "2022-12-31 00:00:00"
        )


if __name__ == "__main__":
    unittest.main()
