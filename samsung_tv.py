# samsung-tv.py

import requests
import os
import logging
from dotenv import load_dotenv

# Samsung SmartThings API configuration
# Get API key from environment variables .env file
logging.basicConfig(level=logging.INFO)
logging.info("Starting Samsung SmartThings API")
logging.info("Loading environment variables from .env file")

load_dotenv()

samsungSmartThingsAPIKey = os.getenv('SMART_THINGS_API_KEY')
samsungDeviceID = os.getenv('SAMSUNG_DEVICE_ID')

logging.info("Environment variables loaded")
logging.info(f"samsungSmartThingsAPIKey: {samsungSmartThingsAPIKey}")

smartthings_base_url = 'https://api.smartthings.com/v1'

def get_power_state():
    headers = {'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
    url = f'{smartthings_base_url}/devices/{samsungDeviceID}/components/main/capabilities/switch/status'

    logging.info(f"Sending request to URL: {url}")
    logging.info(f"Headers: {headers}")

    try:
        response = requests.get(url, headers=headers)
        logging.info(f"Response status code: {response.status_code}")
        logging.info(f"Response headers: {response.headers}")

        if response.status_code == 200:
            power_state = response.json()['switch']['value']
            return {'power': power_state}, True
        else:
            logging.error(f"Failed to get power state: {response.content}")
            return {'error': 'Failed to get power state'}, False
    except Exception as e:
        logging.exception("Exception occurred while getting power state")
        return {'error': str(e)}, False

def send_command(command_data):
    try:
        # Format the command data as per SmartThings API requirements
        payload = {
            "commands": [{
                "component": command_data.get("component", "main"),
                "capability": command_data["capability"],
                "command": command_data["command"],
                "arguments": command_data.get("arguments", [])
            }]
        }
        response = requests.post(
            f'{smartthings_base_url}/devices/{samsungDeviceID}/commands',
            json=payload,
            headers={'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
        )

        if response.status_code in [200, 202]:
            return {'message': 'Command successful'}, True
        else:
            logging.error(f"Failed to send command: {response.content}")
            return {'error': 'Failed to send command'}, False
    except Exception as e:
        logging.exception("Exception occurred while sending command")
        return {'error': str(e)}, False

    
# def send_command(command_data):
#     headers = {'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
#     url = f'{smartthings_base_url}/devices/{samsungDeviceID}/commands'

#     logging.info(f"Sending request to URL: {url}")
#     logging.info(f"Headers: {headers}")
#     logging.info(f"Command data: {command_data}")

#     try:
#         response = requests.post(url, json={'commands': [command_data]}, headers=headers)
#         logging.info(f"Response status code: {response.status_code}")
#         logging.info(f"Response headers: {response.headers}")

#         if response.status_code == 200:
#             return {'message': 'Command successful'}, True
#         else:
#             logging.error(f"Failed to send command: {response.content}")
#             return {'error': 'Failed to send command'}, False
#     except Exception as e:
#         logging.exception("Exception occurred while sending command")
#         return {'error': str(e)}, False
    
# def send_command(command_data):
#     try:
#         # Format the command data as per SmartThings API requirements
#         payload = {
#             "commands": [{
#                 "component": command_data.get("component", "main"),
#                 "capability": command_data["capability"],
#                 "command": command_data["command"],
#                 "arguments": command_data.get("arguments", [])
#                 }]
#         }
#         response = requests.post(
#         f'{smartthings_base_url}/devices/{samsungDeviceID}/commands',
#         json=payload,
#         headers={'Authorization': f'Bearer {samsungSmartThingsAPIKey}'}
#     )

#         if response.status_code == 200 or response.status_code == 202:
#             return {'message': 'Command successful'}, True
#         else:
#             logging.error(f"Failed to send command: {response.content}")
#             return {'error': 'Failed to send command'}, False
#     except Exception as e:
#         logging.exception("Exception occurred while sending command")
#         return {'error': str(e)}, False