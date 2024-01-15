import os
import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from app import app

class GoveeHeaterStateTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.device = '60:74:F4:6E:B7:C4'
        self.model = 'H7130'

    @patch.dict(os.environ, {'GOVEE_API_KEY': 'your_mocked_api_key'})
    @patch('requests.post')
    def test_get_govee_heater_state_success(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {
            'data': {
                'powerState': 'on'
            }
        }

        response = self.app.get('/api/govee-heater-state?device=device_id&model=model_id')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['powerState'], 'on')

    @patch.dict(os.environ, {'GOVEE_API_KEY': 'your_mocked_api_key'})
    @patch('requests.post')
    def test_get_govee_heater_state_failure(self, mock_post):
        mock_post.return_value.status_code = 500
        mock_post.return_value.json.return_value = {
            'error': 'Failed to fetch Govee heater state'
        }

        response = self.app.get('/api/govee-heater-state?device=device_id&model=model_id')
        data = response.get_json()

        self.assertEqual(response.status_code, 500)
        self.assertEqual(data['error'], 'Failed to fetch Govee heater state')

if __name__ == '__main__':
    unittest.main()
