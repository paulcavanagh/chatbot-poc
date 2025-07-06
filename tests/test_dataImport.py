import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
import sys
import os

# Import the dataImport module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/utils')))
from src.utils import dataImport

class TestDataImport(unittest.TestCase):

    @patch('dataImport.pd.read_excel')
    @patch('dataImport.redis.Redis')
    def test_import_data_to_redis(self, mock_redis_class, mock_read_excel):
        # Mock DataFrame
        data = {
            'Person ID': [1],
            'Person name': ['John Doe'],
            'Nationality': ['Irish'],
            'Licence type': ['A'],
            'Reference No.': ['REF123'],
            'Date from': ['2024-01-01'],
            'Date to': ['2024-12-31'],
            'In status since': ['2023-01-01'],
            'Notes': ['Test note'],
            'Season': ['2024/2025'],
        }
        df = pd.DataFrame(data)
        mock_read_excel.return_value = df

        # Mock Redis instance
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis

        # Call the actual function
        dataImport.import_data_to_redis()

        # Check that set was called with correct arguments
        expected_key = 'user:1'
        expected_user_data = {
            'personName': 'John Doe',
            'nationality': 'Irish',
            'licenceType': 'A',
            'referenceNo': 'REF123',
            'dateFrom': '2024-01-01',
            'dateTo': '2024-12-31',
            'inStatusSince': '2023-01-01',
            'notes': 'Test note',
            'season': '2024/2025',
        }
        import json
        mock_redis.set.assert_called_with(expected_key, json.dumps(expected_user_data))


    @patch('dataImport.redis.Redis')
    def test_read_user_from_redis(self, mock_redis_class):
        # Mock Redis instance
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        # Mock return value for get (JSON-encoded bytes)
        import json
        expected_dict = {'personName': 'John Doe', 'nationality': 'Irish'}
        mock_redis.get.return_value = json.dumps(expected_dict).encode()
        user_id = '1'
        result = dataImport.get_user_from_redis(mock_redis, user_id)
        self.assertEqual(result['personName'], 'John Doe')
        self.assertEqual(result['nationality'], 'Irish')

if __name__ == '__main__':
    unittest.main()
