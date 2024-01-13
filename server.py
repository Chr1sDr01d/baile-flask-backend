
from flask import Flask, jsonify, request, send_from_directory # pip install Flask
import subprocess # Built-in module
import os # Built-in module
from dotenv import load_dotenv # pip install python-dotenv
from flask_cors import CORS # pip install flask-cors
from blink_cam import login_to_blink, verify_pin_with_blink  # Importing functions from blink-cam.py
from samsung_tv import get_power_state, send_command  # Importing functions from samsung-tv.py
from govee_lights import get_govee_status, send_govee_command # Importing functions from govee-lights.py
from govee_heater import get_govee_heater_devices, control_govee_heater # Importing functions from govee-heater.py
app = Flask(__name__, static_folder='../baile-react-frontend/dist')
CORS(app)

#---------------------------------------------#
#  Load Environment Variables from .env file
#---------------------------------------------#

load_dotenv()

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

def check_env_variables():
    required_env_variables = [
        'FLOOR_LAMP_MAC',
        'LIGHTBARS_MAC',
        'TV_MAC',
        'GOVEE_API_KEY',
        'SMART_THINGS_API_KEY',
        'SAMSUNG_DEVICE_ID',
        'BLINK_USERNAME',
        'BLINK_PASSWORD',
        'BLINK_ACCOUNT_ID',
        'BLINK_USER_ID',
        'BLINK_CLIENT_ID'
        # Add other required environment variables here...
    ]

    for env_var in required_env_variables:
        if env_var not in os.environ:
            return False
    return True
#---------------------------------------------#
#  Blink Camera API
#---------------------------------------------#

@app.route('/blink/login', methods=['POST'])
def blink_login():
    if not check_env_variables():
        return jsonify({'error': 'Failed to load required environment variables'}), 500

    unique_id = request.json.get('unique_id', 'default_unique_id')
    reauth = request.json.get('reauth', 'false')
    response, success = login_to_blink(os.getenv('BLINK_USERNAME'), os.getenv('BLINK_PASSWORD'), unique_id, reauth)
    return jsonify(response), 200 if success else 401

@app.route('/blink/verify-pin', methods=['POST'])
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

@app.route('/samsung-tv/power-state', methods=['GET'])
def samsung_tv_power_state():
    response, success = get_power_state()
    return jsonify(response), 200 if success else 500

@app.route('/samsung-tv/send-command', methods=['POST'])
def samsung_tv_send_command():
    command_data = request.json
    response, success = send_command(command_data)
    return jsonify(response), 200 if success else 500

#---------------------------------------------#
# Govee Heater Devices API
#---------------------------------------------#

@app.route('/govee-heater/devices', methods=['GET'])
def govee_heater_get_devices():
    response, success = get_govee_heater_devices()
    return jsonify(response), 200 if success else 500

@app.route('/govee-heater/control', methods=['PUT'])
def govee_heater_control_device():
    device = request.json.get('device')
    model = request.json.get('model')
    cmd = request.json.get('cmd')
    response, success = control_govee_heater(device, model, cmd)
    return jsonify(response), 200 if success else 500

# Add other routes as needed...

if __name__ == '__main__':
    app.run(debug=True)
