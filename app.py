
from flask import Flask, jsonify, make_response, request, send_from_directory # pip install Flask
import subprocess # Built-in module
import os # Built-in module
from dotenv import load_dotenv # pip install python-dotenv
import requests # pip install flask-cors
from blink_cam import login_to_blink, verify_pin_with_blink  # Importing functions from blink-cam.py
from samsung_tv import get_power_state, send_command  # Importing functions from samsung-tv.py
from govee_lights import get_govee_status, send_govee_command # Importing functions from govee-lights.py
from govee_heater import get_govee_heater_devices, control_govee_heater # Importing functions from govee-heater.py
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from flask_cors import CORS, cross_origin

app = Flask(__name__, static_folder='../baile-react-frontend/dist')
#---------------------------------------------#
#  Configure Logging
#---------------------------------------------#

# Configure logging
logging.basicConfig(level=logging.INFO)
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)

#---------------------------------------------#
#  CORS CORS CORS
#---------------------------------------------#
CORS(app, resources={r"/*": {"origins": "*"}})
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

#---------------------------------------------#
#  Testing Route
#---------------------------------------------#

@app.route('/test', methods=['GET', 'OPTIONS'])
def test_route():
    return jsonify({"message": "Test successful"})


#---------------------------------------------#
#  Load Environment Variables from .env file
#---------------------------------------------#

load_dotenv()

#---------------------------------------------#
#  Check for Environment Variables from .env file
#---------------------------------------------#

# Check for required environment variables
def check_env_variables():
    required_env_variables = [
        'FLOOR_LAMP_MAC', 'LIGHTBARS_MAC', 'TV_MAC', 'GOVEE_API_KEY',
        'SMART_THINGS_API_KEY', 'SAMSUNG_DEVICE_ID', 'BLINK_USERNAME',
        'BLINK_PASSWORD', 'BLINK_ACCOUNT_ID', 'BLINK_USER_ID', 'BLINK_CLIENT_ID'
    ]
    return all(env_var in os.environ for env_var in required_env_variables)

#---------------------------------------------#
# Root Route
#---------------------------------------------#

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    if not check_env_variables():
        return jsonify({'error': 'Failed to load required environment variables'}), 500
    return send_from_directory(app.static_folder, 'index.html')
def index():
    if not check_env_variables():
        return jsonify({'error': 'Failed to load required environment variables'}), 500
    return send_from_directory(app.static_folder, 'index.html')

#---------------------------------------------#
#  Blink Camera API
#---------------------------------------------#

@app.route('/blink/login', methods=['GET', 'OPTIONS'])
@cross_origin()  # Ad
def blink_login():
    if not check_env_variables():
        return jsonify({'error': 'Failed to load required environment variables'}), 500

    unique_id = request.json.get('unique_id', 'default_unique_id')
    reauth = request.json.get('reauth', 'false')
    response, success = login_to_blink(os.getenv('BLINK_USERNAME'), os.getenv('BLINK_PASSWORD'), unique_id, reauth)
    return jsonify(response), 200 if success else 401

@app.route('/blink/verify-pin', methods=['GET', 'OPTIONS'])
@cross_origin()  # Ad
def blink_verify_pin():
    if not check_env_variables():
        return jsonify({'error': 'Failed to load required environment variables'}), 500

    account_id = request.json.get('account_id')
    client_id = request.json.get('client_id')
    pin = request.json.get('pin')
    auth_token = request.json.get('auth_token')
    response, success = verify_pin_with_blink(account_id, client_id, pin, auth_token)
    return jsonify(response), 200 if success else 401

#---------------------------------------------#
#  Samsung TV Widget API
#---------------------------------------------#

@app.route('/samsung-tv/power-state', methods=['GET', 'OPTIONS'])
def samsung_tv_power_state():
    if request.method == "OPTIONS":  # CORS preflight
        return _build_cors_preflight_response()
    elif request.method == "GET":  # The actual request
        power_state_response, success = get_power_state()
        if success:
            response = jsonify(power_state_response)
            return _corsify_actual_response(response)
        else:
            return jsonify(power_state_response), 500


@app.route('/samsung-tv/send-command', methods=['POST', 'OPTIONS'])
def samsung_tv_send_command():
    if request.method == "OPTIONS":
        return _build_cors_preflight_response()
    elif request.method == "POST":
        command_data = request.json
        success_response, success = send_command(command_data)
        if success:
            return _corsify_actual_response(jsonify(success_response))
        else:
            return jsonify(success_response), 500
        
@app.route('/samsung-tv/play', methods=['POST'])
def samsung_tv_play():
    # Logic to send play command
    
    command_data = {"component": "main", "capability": "mediaPlayback", "command": "play"}
    success_response, success = send_command(command_data)
    return jsonify(success_response), 200 if success else 500

@app.route('/samsung-tv/pause', methods=['POST'])
def samsung_tv_pause():
    # Logic to send pause command
    command_data = {"component": "main", "capability": "mediaPlayback", "command": "pause"}
    success_response, success = send_command(command_data)
    return jsonify(success_response), 200 if success else 500

@app.route('/samsung-tv/launch-app', methods=['POST'])
def samsung_tv_launch_app():
    app_id = request.json.get('appId')
    command_data = {"component": "main", "capability": "custom.launchapp", "command": "launchApp", "arguments": [app_id]}
    success_response, success = send_command(command_data)
    return jsonify(success_response), 200 if success else 500




#---------------------------------------------#
# Govee Heater Devices API
#---------------------------------------------#

@app.route('/govee-heater/devices', methods=['GET', 'OPTIONS'])
@cross_origin()  # Ad
def govee_heater_get_devices():
    response, success = get_govee_heater_devices()
    return jsonify(response), 200 if success else 500

@app.route('/govee-heater/control', methods=['GET', 'OPTIONS'])
@cross_origin()  # Ad
def govee_heater_control_device():
    device = request.json.get('device')
    model = request.json.get('model')
    cmd = request.json.get('cmd')
    response, success = control_govee_heater(device, model, cmd)
    return jsonify(response), 200 if success else 500

# Create a new route to get the Govee heater state
@app.route('/api/govee-heater-status', methods=['GET'])
@cross_origin()  # Add this decorator to enable CORS support for the route
def get_govee_heater_status():
    device = request.args.get('device')
    model = request.args.get('model')
    
    # Fetch the Govee API key from environment variables
    govee_api_key = os.getenv('GOVEE_API_KEY')
    
    if not govee_api_key:
        return jsonify({'error': 'Govee API key is not available in environment variables'}), 500
    
    # Use the Govee API to send a command to get the state
    govee_url = f'https://developer-api.govee.com/v1/appliance/control'
    
    headers = {
        'Govee-API-Key': govee_api_key
    }
    
    # Define the command to get the power state
    command = {
        'device': device,
        'model': model,
        'cmd': 'turn',
        'value': 'query'  # This value queries the current state
    }
    
    try:
        response = requests.post(govee_url, json=command, headers=headers)
        if response.status_code == 200:
            # expect response to be like:
#             {
#     "data": {
#         "devices": [
#             {
#                 "device": "1D:C0:60:74:F4:6E:B7:C4",
#                 "model": "H7130",
#                 "deviceName": "Black Smart Heater",
#                 "controllable": true,
#                 "retrievable": false,
#                 "properties": {
#                     "mode": {
#                         "options": [
#                             {
#                                 "name": "Low",
#                                 "value": "1"
#                             },
#                             {
#                                 "name": "Medium",
#                                 "value": "2"
#                             },
#                             {
#                                 "name": "High",
#                                 "value": "3"
#                             }
#                         ]
#                     }
#                 },
#                 "supportCmds": [
#                     "turn",
#                     "mode"
#                 ]
#             },
#             {
#                 "device": "1D:C8:60:74:F4:58:56:42",
#                 "model": "H7130",
#                 "deviceName": "White Smart Heater",
#                 "controllable": true,
#                 "retrievable": false,
#                 "properties": {
#                     "mode": {
#                         "options": [
#                             {
#                                 "name": "Low",
#                                 "value": "1"
#                             },
#                             {
#                                 "name": "Medium",
#                                 "value": "2"
#                             },
#                             {
#                                 "name": "High",
#                                 "value": "3"
#                             }
#                         ]
#                     }
#                 },
#                 "supportCmds": [
#                     "turn",
#                     "mode"
#                 ]
#             }
#         ]
#     },
#     "message": "Success",
#     "code": 200
# }
            logging.info(f'Response: {response.json()}')
            data = response.json().get('data', {})
            power_state = data.get('powerState', 'off')
            logging.info(f'Power state: {power_state}')
            # You can add more properties if needed
            return jsonify({'powerState': power_state})
        else:
            return jsonify({'error': 'Failed to fetch Govee heater state'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add other routes as needed...

if __name__ == '__main__':
    handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)
    app.run(debug=True, port=5001)