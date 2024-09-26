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

def initialize_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_CHILDREN_TABLE_SQL)
        cursor.execute(CREATE_TRANSACTIONS_TABLE_SQL)
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


# Endpoint to create a new class
@app.route('/create-class', methods=['POST'])
def create_class():
    data = request.get_json()
    class_name = data.get('class_name')

    if not class_name:
        return jsonify({'error': 'Class name is required'}), 400

    try:
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()
        db_name = f"{class_name.lower()}_db"
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.close()
        connection.close()

        connection = mysql.connector.connect(database=db_name, **db_config_base)
        initialize_database(connection)

        # Automatically insert the "kivét" child with ID 1
        cursor = connection.cursor()
        cursor.execute("INSERT INTO children (id, name, url_name) VALUES (1, 'kivét', 'kivet')")
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({'success': True, 'message': f"Class '{class_name}' created successfully!"}), 201

    except Error as e:
        return jsonify({'error': 'Failed to create class'}), 500


# Get classes
@app.route('/classes', methods=['GET'])
def get_classes():
    try:
        db = getattr(g, 'db', None)
        cursor = db.cursor()
        cursor.execute("SHOW DATABASES LIKE '%_db';")
        databases = cursor.fetchall()
        class_names = [db[0].replace('_db', '') for db in databases]
        cursor.close()
        return jsonify(class_names), 200
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
        cursor.execute("SELECT id, name, isDeleted FROM children")
        result = cursor.fetchall()
        cursor.close()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Add child
@app.route('/<class_name>/children', methods=['POST'])
def add_child(class_name):
    try:
        data = request.json
        child_name = data.get('name')
        url_name = unidecode.unidecode(child_name.lower()).replace(' ', '-')
        db = getattr(g, 'db', None)
        cursor = db.cursor()
        cursor.execute("INSERT INTO children (name, url_name) VALUES (%s, %s)", (child_name, url_name))
        db.commit()
        cursor.close()
        return jsonify({'id': cursor.lastrowid, 'name': child_name, 'url_name': url_name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to modify an existing child
@app.route('/<class_name>/children/<int:child_id>', methods=['PUT'])
def modify_child(class_name, child_id):
    try:
        data = request.json
        new_name = data.get('name')
        db = getattr(g, 'db', None)
        cursor = db.cursor()
        cursor.execute("UPDATE children SET name = %s WHERE id = %s", (new_name, child_id))
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

