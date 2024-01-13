# govee_lights.py

import requests
import os

# Base URL for the Govee API
govee_base_url = 'https://developer-api.govee.com/v1'
# API key from environment variable
govee_api_key = os.getenv('goveeApiKey')

def get_govee_status(device_mac, device_model):
    try:
        response = requests.get(f'{govee_base_url}/devices/state', params={
            'device': device_mac,
            'model': device_model
        }, headers={
            'Content-Type': 'application/json',
            'Govee-API-Key': govee_api_key
        })

        if response.status_code == 200:
            data = response.json()
            device_data = next((device for device in data['data']['devices'] if device['device'] == device_mac), None)
            if device_data:
                return device_data['properties'], True
            else:
                return 'Device not found', False
        else:
            return 'Failed to get Govee light status', False
    except Exception as e:
        return str(e), False

def send_govee_command(device_mac, device_model, cmd):
    try:
        response = requests.put(f'{govee_base_url}/devices/control', json={
            'device': device_mac,
            'model': device_model,
            'cmd': cmd
        }, headers={
            'Content-Type': 'application/json',
            'Govee-API-Key': govee_api_key
        })

        if response.status_code == 200:
            return 'Command successful', True
        else:
            return 'Failed to send command', False
    except Exception as e:
        return str(e), False
