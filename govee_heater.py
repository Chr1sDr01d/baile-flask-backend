# govee_heater.py

import requests
import os

govee_api_key = os.getenv('GOVEE_API_KEY')
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
