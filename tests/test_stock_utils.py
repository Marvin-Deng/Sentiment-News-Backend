import unittest
from unittest.mock import patch
from utils.stock import StockUtils


class TestStockUtils(unittest.TestCase):

    @patch('utils.stock.requests.get')
    def test_get_eod_data_success(self, mock_get):
        mock_response = unittest.mock.Mock()
        mock_response.json.return_value = [{
            'open': 100,
            'high': 110,
            'low': 90,
            'close': 105,
            'volume': 10000,
            'adjOpen': 100,
            'adjHigh': 110,
            'adjLow': 90,
            'adjClose': 105,
            'adjVolume': 10000,
            'divCash': 0.5,
            'splitFactor': 1,
        }]
        mock_get.return_value = mock_response

        result = StockUtils.get_eod_data('AAPL', '2023-01-01')

        self.assertIsNotNone(result)
        self.assertIsInstance(result, list)
        self.assertDictEqual(result[0], {
            'open': 100,
            'high': 110,
            'low': 90,
            'close': 105,
            'volume': 10000,
            'adjOpen': 100,
            'adjHigh': 110,
            'adjLow': 90,
            'adjClose': 105,
            'adjVolume': 10000,
            'divCash': 0.5,
            'splitFactor': 1,
        })


if __name__ == '__main__':
    unittest.main()
