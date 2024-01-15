# govee_heater.py

import requests
import os
import logging
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

govee_api_key = os.getenv('GOVEE_API_KEY')
if not govee_api_key:
    raise ValueError("GOVEE_API_KEY environment variable not set")
    
logger.info(f"GOVEE_API_KEY: {govee_api_key}")
GOVEE_BASE_URL = "https://developer-api.govee.com/v1" 


def get_govee_heater_devices():
    headers = {"Govee-API-Key": govee_api_key}
    try:
        response = requests.get(f"{GOVEE_BASE_URL}/appliance/devices", headers=headers)
        return response.json(), response.status_code == 200
    except Exception as e:
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
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False
