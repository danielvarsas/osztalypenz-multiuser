from flask import Blueprint, request, jsonify, session
from config.db import get_db_connection, check_pin  # Assuming these are in db.py

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/<class_name>/verify-pin', methods=['POST'])
def verify_pin(class_name):
    data = request.json
    pin_code = data.get('pin_code')

    if not pin_code:
        return jsonify({'error': 'PIN is required'}), 400

    try:
        # Connect to the main database (osztalypenz_db), not the class-specific database
        main_db_connection = get_db_connection()  # Connect to main database
        cursor = main_db_connection.cursor(dictionary=True)

        # Fetch the hashed PIN from the class_admins table for the specific class
        cursor.execute("SELECT pin_code FROM class_admins WHERE class_name = %s LIMIT 1", (class_name,))
        admin = cursor.fetchone()

        # Debugging: Print the admin entry retrieved from the main database
        print("admin:", admin)

        if admin and check_pin(pin_code, admin['pin_code']):
            # If the PIN matches, store the class in the session
            session['authenticated_class'] = class_name
            return jsonify({'message': 'PIN verified successfully'}), 200
        else:
            return jsonify({'error': 'Invalid PIN'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@auth_bp.route('/<class_name>/<child_name>/verify-pin', methods=['POST'])
def verify_child_pin(class_name, child_name):
    try:
        data = request.json
        pin_code = data.get('pin_code')

        if not pin_code:
            return jsonify({'error': 'PIN is required'}), 400

        # Connect to the class-specific database
        connection = get_db_connection(f"{class_name.lower()}_db")
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT pin_code FROM children WHERE url_name = %s LIMIT 1", (child_name,))
        child = cursor.fetchone()

        if child and check_pin(pin_code, child['pin_code']):
            return jsonify({'message': 'PIN verified successfully'}), 200
        else:
            return jsonify({'error': 'Invalid PIN'}), 401

    except Exception as e:
        return jsonify({'error': str(e)}), 500

