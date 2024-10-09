from flask import Blueprint, jsonify, request, session
from config.db import get_db_connection, create_database, initialize_database, hash_pin, check_pin

classes_bp = Blueprint('classes', __name__)

import bcrypt

def hash_pin(pin_code):
    # Generate salt and hash the pin
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(pin_code.encode('utf-8'), salt)
    return hashed_pin.decode('utf-8')

@classes_bp.route('/create-class', methods=['POST'])
def create_class():
    data = request.json
    class_name = data.get('class_name')
    admin_email = data.get('admin_email')
    pin_code = data.get('pin_code')

    if not class_name or not admin_email or not pin_code:
        return jsonify({'error': 'Class name, email, and PIN are required'}), 400

    try:
        # Step 1: Hash the PIN before storing it
        hashed_pin = hash_pin(pin_code)

        # Step 2: Create the new class-specific database
        db_name = f"{class_name.lower()}_db"
        create_database(class_name)  # Create the new class-specific database

        # Step 3: Connect to the new class-specific database
        class_db_connection = get_db_connection(db_name)  # Connect to the new class-specific DB

        # Step 4: Initialize the new class database (create children, transactions, etc.)
        initialize_database(class_db_connection)  # Initialize the tables in the new class-specific DB

        # Step 5: Insert the "Kivét" child into the new class's children table
        cursor = class_db_connection.cursor()
        cursor.execute("""
            INSERT INTO children (id, name, url_name, email, isDeleted)
            VALUES (1, 'Kivét', 'kivet', NULL, FALSE)
        """)
        class_db_connection.commit()

        # Step 6: Insert class info into the `class_admins` table in the main database (osztalypenz_db)
        main_db_connection = get_db_connection()  # Connect to the main DB
        main_cursor = main_db_connection.cursor()

        main_cursor.execute("INSERT INTO class_admins (class_name, admin_email, pin_code) VALUES (%s, %s, %s)", 
                            (class_name, admin_email, hashed_pin))
        main_db_connection.commit()

        # Close all connections
        cursor.close()
        class_db_connection.close()
        main_cursor.close()
        main_db_connection.close()

        return jsonify({'message': f"Class '{class_name}' created successfully!"}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500




@classes_bp.route('/classes', methods=['GET'])
def get_classes():
    try:
        # Connect to the main database (where class_admins is stored)
        connection = get_db_connection()  # Ensure this uses db_config_default, which includes the main database
        if not connection:
            return jsonify({'error': 'Failed to connect to main database'}), 500

        cursor = connection.cursor(dictionary=True)

        # Query to fetch all classes and their admin emails from class_admins table in the main database
        cursor.execute("SELECT class_name, admin_email FROM class_admins;")
        classes = cursor.fetchall()

        cursor.close()
        connection.close()

        # Return the list of classes with admin emails
        return jsonify(classes), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

        
@classes_bp.route('/classes/<class_name>', methods=['GET'])
def check_class_exists(class_name):
    try:
        print(f"API called with class_name: {class_name}", flush=True)  # Added to confirm the route is triggered
        # Query the class_admins table to check if the class exists
        connection = get_db_connection()
        cursor = connection.cursor()

        # Check if the class exists in class_admins
        cursor.execute("SELECT class_name FROM class_admins WHERE class_name = %s", (class_name,))
        existing_class = cursor.fetchone()
        
        print(f"Class query result: {existing_class}")
        
        cursor.close()
        connection.close()

        # If class exists, return 200 with a message
        if existing_class:
            return jsonify({'message': 'Class exists'}), 200
            print('exists')
        else:
            # If class does not exist, return 404
            return jsonify({'error': 'Class not found'}), 404
            print('Class doesnt exists')

    except Exception as e:
        print(f"Error: {e}", flush=True)  # Ensure any exception is printed
        return jsonify({'error': str(e)}), 500


@classes_bp.route('/<class_name>/dashboard', methods=['GET'])
def class_dashboard(class_name):
    # Check if the class admin has been authenticated
    if session.get('authenticated_class') != class_name:
        return jsonify({'error': 'Unauthorized access, please provide valid PIN'}), 403

    # If authenticated, return the dashboard
    return jsonify({'message': f'Welcome to {class_name} dashboard!'}), 200