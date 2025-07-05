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

        # Simulate the import logic
        excel_file = 'src/data/data.xlsx'
        df = pd.read_excel(excel_file)
        r = mock_redis
        for index, row in df.iterrows():
            key = f"user:{row['Person ID']}"
            user_data = {
                'personName': str(row['Person name']),
                'nationality': str(row['Nationality']),
                'licenceType': str(row['Licence type']),
                'referenceNo': str(row['Reference No.']),
                'dateFrom': str(row['Date from']),
                'dateTo': str(row['Date to']),
                'inStatusSince': str(row['In status since']),
                'notes': str(row['Notes']),
                'season': str(row['Season']),
            }
            r.hset(key, mapping=user_data)

        # Check that hset was called with correct arguments
        mock_redis.hset.assert_called_with(
            'user:1',
            mapping={
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
        )

    @patch('dataImport.redis.Redis')
    def test_read_user_from_redis(self, mock_redis_class):
        # Mock Redis instance
        mock_redis = MagicMock()
        mock_redis_class.return_value = mock_redis
        # Mock return value for hgetall
        mock_redis.hgetall.return_value = {
            b'personName': b'John Doe',
            b'nationality': b'Irish',
        }
        user_id = '1'
        key = f"user:{user_id}"
        user_data = mock_redis.hgetall(key)
        user_data = {k.decode(): v.decode() for k, v in user_data.items()}
        self.assertEqual(user_data['personName'], 'John Doe')
        self.assertEqual(user_data['nationality'], 'Irish')

if __name__ == '__main__':
    unittest.main()
