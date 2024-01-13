# blink-cam.py

import requests
import os

BLINK_API_URL = "https://rest-prod.immedia-semi.com"

def login_to_blink(username, password, unique_id, reauth):
    try:
        login_url = f"{BLINK_API_URL}/api/v5/account/login"
        payload = {
            "email": username,
            "password": password,
            "unique_id": unique_id,
            "reauth": reauth
        }
        response = requests.post(login_url, json=payload)
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False

def verify_pin_with_blink(account_id, client_id, pin, auth_token):
    try:
        verify_url = f"{BLINK_API_URL}/api/v4/account/{account_id}/client/{client_id}/pin/verify"
        headers = {"TOKEN-AUTH": auth_token}
        payload = {"pin": pin}
        response = requests.post(verify_url, headers=headers, json=payload)
        return response.json(), response.status_code == 200
    except Exception as e:
        return {"error": str(e)}, False
