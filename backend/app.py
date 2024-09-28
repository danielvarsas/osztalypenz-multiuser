from flask import Flask, request, jsonify, Blueprint, g
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
from mysql.connector import Error
import os
import unidecode

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Base configuration for MySQL connection (without a specific database)
db_config_base = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# Default database config (e.g., for global queries or operations not tied to a specific class)
db_config_default = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),
    'database': os.getenv('DB_NAME')  # Default database
}

# SQL statements to create tables
CREATE_CHILDREN_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url_name VARCHAR(255) NOT NULL,
    email VARCHAR(255),
    isDeleted BOOLEAN DEFAULT FALSE
);
"""

CREATE_TRANSACTIONS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    child_id INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    reason VARCHAR(255),
    type ENUM('add', 'take') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (child_id) REFERENCES children(id)
);
"""

CREATE_CLASS_ADMINS_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS class_admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    class_name VARCHAR(255) NOT NULL UNIQUE,
    admin_email VARCHAR(255) NOT NULL,
    pin_code VARCHAR(10) NOT NULL
);
"""

# Functions for DB management
def get_db_connection(subdomain, create_if_not_exists=True):
    db_name = f"{subdomain}_db"

    try:
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()

        if create_if_not_exists:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
            connection.database = db_name
            initialize_database(connection)

        cursor.close()
        connection.close()

        connection = mysql.connector.connect(database=db_name, **db_config_base)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None
        
def initialize_main_database():
    try:
        connection = mysql.connector.connect(**db_config_default)  # Connect to the main database
        cursor = connection.cursor()
        cursor.execute(CREATE_CLASS_ADMINS_TABLE_SQL)
        connection.commit()
        cursor.close()
        connection.close()
    except Error as e:
        print(f"Error initializing the main database: {e}")

def initialize_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_CHILDREN_TABLE_SQL)
        cursor.execute(CREATE_TRANSACTIONS_TABLE_SQL)
        cursor.execute(CREATE_CLASS_ADMINS_TABLE_SQL)  # Add this table creation
        connection.commit()
        cursor.close()
    except Error as e:
        print(f"Error initializing the database: {e}")

@app.before_request
def before_request():
    # Safely check if the route has 'class_name' in the view arguments
    if request.view_args and 'class_name' in request.view_args:
        class_name = request.view_args.get('class_name')
        db = get_db_connection(class_name, create_if_not_exists=False)
        if db:
            g.db = db
        else:
            return jsonify({'error': 'Database connection failed'}), 500
    else:
        # If no class_name, use the default global connection for general operations
        try:
            g.db = mysql.connector.connect(**db_config_default)
        except mysql.connector.Error as err:
            return jsonify({'error': 'Main database connection failed'}), 500


# Endpoint to create a new class with PIN and Admin Email
@app.route('/api/create-class', methods=['POST'])
def create_class():
    data = request.get_json()
    class_name = data.get('class_name')
    admin_email = data.get('admin_email')
    pin_code = data.get('pin_code')

    if not class_name or not admin_email or not pin_code:
        return jsonify({'error': 'Class name, email, and PIN are required'}), 400

    try:
        # Step 1: Connect to the main database and check if the class already exists
        connection = mysql.connector.connect(**db_config_default)
        cursor = connection.cursor()

        cursor.execute("SELECT class_name FROM class_admins WHERE class_name = %s", (class_name,))
        existing_class = cursor.fetchone()

        if existing_class:
            return jsonify({'error': 'Class name already exists'}), 400

        # Step 2: Create the new class database
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()
        db_name = f"{class_name.lower()}_db"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.close()
        connection.close()

        # Step 3: Initialize the new class database
        connection = mysql.connector.connect(database=db_name, **db_config_base)
        initialize_database(connection)

        # Step 4: Insert class admin info into class_admins table
        cursor = connection.cursor()
        cursor.execute("INSERT INTO class_admins (class_name, admin_email, pin_code) VALUES (%s, %s, %s)", (class_name, admin_email, pin_code))
        connection.commit()

        # Step 5: Insert the "kivét" child only if it doesn't exist
        cursor.execute("SELECT id FROM children WHERE id = 1")
        kivet_child = cursor.fetchone()

        if not kivet_child:
            cursor.execute("INSERT INTO children (id, name, url_name) VALUES (1, 'kivét', 'kivet')")
            connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': f"Class '{class_name}' created successfully!"}), 201

    except Error as e:
        return jsonify({'error': f"Failed to create class: {e}"}), 500



# Route to modify admin email and/or PIN for a class
@app.route('/api/update-class-admin', methods=['PUT'])
def update_class_admin():
    data = request.get_json()
    class_name = data.get('class_name')
    new_email = data.get('admin_email')

    if not class_name or not new_email:
        return jsonify({'error': 'Class name and new admin email are required'}), 400

    try:
        # Connect to the main database
        connection = mysql.connector.connect(**db_config_default)
        cursor = connection.cursor()

        # Update the admin email for the specified class
        cursor.execute("UPDATE class_admins SET admin_email = %s WHERE class_name = %s", (new_email, class_name))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': f"Admin email for class '{class_name}' updated successfully!"}), 200

    except Error as e:
        print(f"Error updating admin email: {e}")
        return jsonify({'error': f"Failed to update admin email: {e}"}), 500



# Get classes including admin email
@app.route('/api/classes', methods=['GET'])
def get_classes():
    try:
        connection = mysql.connector.connect(**db_config_default)
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT class_name, admin_email FROM class_admins;")
        result = cursor.fetchall()
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get account movements
@app.route('/<class_name>/account-movements', methods=['GET'])
def account_movements(class_name):
    try:
        db = getattr(g, 'db', None)
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT transactions.id, transactions.amount, transactions.reason, transactions.type, transactions.created_at, 
                   children.name AS child_name
            FROM transactions
            LEFT JOIN children ON transactions.child_id = children.id
            ORDER BY transactions.created_at DESC
        """)
        result = cursor.fetchall()
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to get children
@app.route('/<class_name>/children', methods=['GET'])
def get_children(class_name):
    try:
        db = getattr(g, 'db', None)
        cursor = db.cursor(dictionary=True)
        
        # Fetching the 'id', 'name', 'email', and 'isDeleted' fields
        cursor.execute("SELECT id, name, email, isDeleted FROM children")
        result = cursor.fetchall()
        cursor.close()

        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Add child with email
@app.route('/<class_name>/children', methods=['POST'])
def add_child(class_name):
    try:
        data = request.json
        child_name = data.get('name')
        email = data.get('email')  # Capture email from the request

        url_name = unidecode.unidecode(child_name.lower()).replace(' ', '-')
        db = getattr(g, 'db', None)
        cursor = db.cursor()

        # Insert the new child with name and email
        cursor.execute("INSERT INTO children (name, url_name, email) VALUES (%s, %s, %s)", (child_name, url_name, email))
        db.commit()
        cursor.close()

        return jsonify({'id': cursor.lastrowid, 'name': child_name, 'url_name': url_name, 'email': email}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Modify child with email
@app.route('/<class_name>/children/<int:child_id>', methods=['PUT'])
def modify_child(class_name, child_id):
    try:
        data = request.json
        new_name = data.get('name')
        email = data.get('email')  # Capture email for modification

        db = getattr(g, 'db', None)
        cursor = db.cursor()

        # Update the child's name and email
        cursor.execute("UPDATE children SET name = %s, email = %s WHERE id = %s", (new_name, email, child_id))
        db.commit()
        cursor.close()

        return jsonify({'message': 'Child updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a child
@app.route('/<class_name>/children/<int:child_id>', methods=['DELETE'])
def delete_child(class_name, child_id):
    try:
        db = getattr(g, 'db', None)
        cursor = db.cursor()
        cursor.execute("UPDATE children SET isDeleted = 1 WHERE id = %s", (child_id,))
        db.commit()
        cursor.close()
        return jsonify({'message': 'Child deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Get student's account movements
@app.route('/<class_name>/<url_name>/account-movements', methods=['GET'])
def get_student_account_movements(class_name, url_name):
    try:
        db = getattr(g, 'db', None)
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id FROM children WHERE url_name = %s", (url_name,))
        student = cursor.fetchone()
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        student_id = student['id']
        cursor.execute("""
            SELECT transactions.id, transactions.amount, transactions.reason, transactions.type, transactions.created_at 
            FROM transactions
            WHERE transactions.child_id = %s
            ORDER BY transactions.created_at DESC
        """, (student_id,))
        movements = cursor.fetchall()
        cursor.close()
        return jsonify(movements), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to delete a class
@app.route('/delete-class/<class_name>', methods=['DELETE'])
def delete_class_database(class_name):
    try:
        db_name = f"{class_name}_db"
        db = getattr(g, 'db', None)
        cursor = db.cursor()
        cursor.execute(f"DROP DATABASE IF EXISTS `{db_name}`;")
        db.commit()
        cursor.close()
        return jsonify({'message': f"Class '{class_name}' deleted successfully!"}), 200
    except Exception as e:
        return jsonify({'error': f"Failed to delete class '{class_name}' database."}), 500

# Route to add money for a child
@app.route('/<class_name>/add-money', methods=['POST'])
def add_money(class_name):
    try:
        # Retrieve the connection to the correct database from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            print("Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500
        
        data = request.json
        print("Received data:", data)  # Debugging print statement
        child_id = data.get('child_id')
        amount = data.get('amount')

        # Ensure child_id and amount are provided
        if not child_id or not amount:
            print("Missing child_id or amount")
            return jsonify({'error': 'Both child ID and amount are required'}), 400

        # Fetch the child's name by ID for logging purposes
        child_name = get_child_name_by_id(child_id)
        print(f"Child Name: {child_name}")

        # Ensure the child exists
        if child_name == 'Unknown':
            print(f"Child with ID {child_id} not found.")
            return jsonify({'error': 'Child not found'}), 404

        # Use the existing database connection to insert the transaction
        cursor = db.cursor()

        # Insert the transaction into the database
        query = "INSERT INTO transactions (child_id, amount, type) VALUES (%s, %s, 'add')"
        cursor.execute(query, (child_id, amount))
        db.commit()

        cursor.close()
        message = f"{amount} Befizetés könyvelve {child_name} tanulónak"
        print(f"Transaction successful: {message}")
        return jsonify({'message': message}), 200 

    except Exception as e:
        print("Error in add_money:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

# Function to get child's name by ID
def get_child_name_by_id(child_id):
    try:
        # Retrieve the database connection for the current class from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            print("Database connection failed.")
            return 'Unknown'

        # Use the existing database connection to fetch the child's name
        cursor = db.cursor(dictionary=True)

        # Query to fetch the child's name by ID
        query = "SELECT name FROM children WHERE id = %s"
        cursor.execute(query, (child_id,))
        result = cursor.fetchone()

        # Return the child's name if found, otherwise return 'Unknown'
        return result['name'] if result else 'Unknown'

    except Exception as e:
        print(f"Error while connecting to MySQL: {e}")
        return 'Unknown'

    finally:
        if db and cursor:
            cursor.close()

# Route to take money
@app.route('/<class_name>/take-money', methods=['POST'])
def take_money(class_name):
    try:
        # Retrieve the database connection for the current class from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500

        data = request.json
        print("Received data:", data)  # Debugging print statement
        amount = data.get('amount')
        reason = data.get('reason')

        # Ensure amount and reason are provided
        if not amount or not reason:
            return jsonify({'error': 'Összeget és okot is adj'}), 400

        # Use the child_id for "Kivét" (always ID 1)
        child_id_of_kivet = 1

        # Insert the transaction into the database
        cursor = db.cursor()
        query = "INSERT INTO transactions (child_id, amount, reason, type) VALUES (%s, %s, %s, 'take')"
        cursor.execute(query, (child_id_of_kivet, amount, reason))
        db.commit()

        cursor.close()

        message = f"{amount} Kivétel iktatva, {reason} céllal."
        return jsonify({'message': message}), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

