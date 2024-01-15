# govee_heater.py

import requests
import os
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

govee_api_key = os.getenv('GOVEE_API_KEY')
logger.info(f"GOVEE_API_KEY: {govee_api_key}")
if not govee_api_key:
    logger.error(f"GOVEE_API_KEY environment variable not set")
    raise ValueError("GOVEE_API_KEY environment variable not set")
    
GOVEE_BASE_URL = "https://developer-api.govee.com/v1" 


def get_govee_heater_devices():
    headers = {"Govee-API-Key": govee_api_key}
    try:
        response = requests.get(f"{GOVEE_BASE_URL}/appliance/devices", headers=headers)
        if response.status_code == 200:
            return response.json(), True
        else:
            logger.error(f"Failed to get devices: {response.text}")
            return {"error": "Failed to get devices"}, False
    except Exception as e:
        logger.error(f"Exception in get_govee_heater_devices: {str(e)}")
        return {"error": str(e)}, False

def control_govee_heater(device, model, cmd):
    headers = {"Govee-API-Key": govee_api_key}
    payload = {
        "device": device,
        "model": model,
        "cmd": cmd
        }
    try:
        response = requests.put(f"{GOVEE_BASE_URL}/appliance/devices/control", json=payload, headers=headers)
        if response.status_code == 200:
            return response.json(), True
        else:
            logger.error(f"Failed to control device: {response.text}")
            return {"error": "Failed to control device"}, False
    except Exception as e:
        logger.error(f"Exception in control_govee_heater: {str(e)}")
        return {"error": str(e)}, False
