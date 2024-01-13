# samsung-tv.py

import requests
import os

# Samsung SmartThings API configuration
samsungSmartThingsAPIKey = os.getenv('samsungSmartThingsAPIKey')
samsungDeviceID = os.getenv('samsungDeviceID')
smartthings_base_url = 'https://api.smartthings.com/v1'

def get_power_state():
    try:
        response = requests.get(
            f'{smartthings_base_url}/devices/{samsungDeviceID}/components/main/capabilities/switch/status',
            headers={'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
        )
        if response.status_code == 200:
            power_state = response.json()['switch']['value']
            return {'power': power_state}, True
        else:
            return {'error': 'Failed to get power state'}, False
    except Exception as e:
        return {'error': str(e)}, False

def send_command(command_data):
    try:
        response = requests.post(
            f'{smartthings_base_url}/devices/{samsungDeviceID}/commands',
            json={'commands': [command_data]},
            headers={'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
        )
        if response.status_code == 200:
            return {'message': 'Command successful'}, True
        else:
            return {'error': 'Failed to send command'}, False
    except Exception as e:
        return {'error': str(e)}, False
