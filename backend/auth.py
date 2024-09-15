from flask import Blueprint, request, jsonify
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__)  # Declare the Blueprint

# Get the correct PIN from environment variables for added security
CORRECT_PIN = os.getenv('PIN_CODE')

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.json
        pin = data.get('pin')

        if not pin:
            return jsonify({'success': False, 'message': 'PIN is required.'}), 400

        # Check if the PIN is correct
        if pin == CORRECT_PIN:
            return jsonify({'success': True, 'message': 'Login successful!'}), 200
        else:
            return jsonify({'success': False, 'message': 'Invalid PIN, please try again.'}), 401

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'success': False, 'message': 'An error occurred during login.'}), 500
