from flask import Flask, request, jsonify, Blueprint, g
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
from mysql.connector import Error
import os
from auth import auth_bp  # Import the auth_bp Blueprint from auth.py
from newclass import get_db_connection, create_class_db  # Import the required functions
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(auth_bp, url_prefix='/auth')

# Database connection configuration using environment variables
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT'),  # Include the port from the .env file
    'database': os.getenv('DB_NAME')
}


# Route to add money for a child
@app.route('/<class_name>/add-money', methods=['POST'])
def add_money(class_name):
    try:
        # Retrieve the connection to the correct database from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        data = request.json
        print("Received data:", data)  # Debugging print statement
        child_id = data.get('child_id')
        amount = data.get('amount')
        child_name = get_child_name_by_id(child_id)
        # Ensure child_id and amount are provided
        if not child_id or not amount:
            return jsonify({'error': 'Add meg mindkét paramétert'}), 400

        # Use the existing database connection to insert the transaction
        cursor = db.cursor()

        # Insert the transaction into the database
        query = "INSERT INTO transactions (child_id, amount, type) VALUES (%s, %s, 'add')"
        cursor.execute(query, (child_id, amount))
        db.commit()

        cursor.close()
        message = f"{amount} Befizetés könyvelve {child_name} tanulónak"
        return jsonify({'message': message}), 200 

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

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

        # Use the child_id for "Kivét"
        child_id_of_kivet = 1  # Use the actual child_id of "Kivét"

        # Use the existing database connection to insert the transaction
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



# Route to get account movements
@app.route('/<class_name>/account-movements', methods=['GET'])
def account_movements(class_name):
    try:
        # Retrieve the database connection for the current class from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500

        # Use the existing database connection to fetch account movements
        cursor = db.cursor(dictionary=True)

        # Fetch all transactions with child names
        query = """
        SELECT transactions.id, transactions.amount, transactions.reason, transactions.type, transactions.created_at, 
               children.name AS child_name
        FROM transactions
        LEFT JOIN children ON transactions.child_id = children.id
        ORDER BY transactions.created_at DESC
        """
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()

        return jsonify(result), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

@app.route('/<class_name>/children', methods=['GET'])
def get_children(class_name):
    try:
        print(f"Fetching children for class: {class_name}")
        db = getattr(g, 'db', None)
        if db is None:
            print("Database connection failed")
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = db.cursor(dictionary=True)

        query = "SELECT id, name, isDeleted FROM children"
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        print("Fetched children:", result)

        return jsonify(result), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

# Route to add a new child
@app.route('/<class_name>/children', methods=['POST'])
def add_child(class_name):
    try:
        data = request.json
        child_name = data.get('name')

        if not child_name:
            return jsonify({'error': 'Adj nevet'}), 400

        # Retrieve the database connection for the current class from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500

        # Use the existing database connection to insert a new child
        cursor = db.cursor()

        # Insert the new child into the database
        query = "INSERT INTO children (name) VALUES (%s)"
        cursor.execute(query, (child_name,))
        db.commit()

        # Get the ID of the newly inserted child
        new_child_id = cursor.lastrowid

        cursor.close()

        # Return the newly created child's ID and name
        return jsonify({'id': new_child_id, 'name': child_name}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# Route to modify an existing child's name
@app.route('/<class_name>/children/<int:child_id>', methods=['PUT'])
def modify_child(class_name, child_id):
    try:
        data = request.json
        new_name = data.get('name')

        if not new_name:
            return jsonify({'error': 'Adj nevet'}), 400

        # Retrieve the database connection for the current class from Flask's global object
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500

        # Use the existing database connection to update the child's name
        cursor = db.cursor()

        # Update the child's name in the database
        query = "UPDATE children SET name = %s WHERE id = %s"
        cursor.execute(query, (new_name, child_id))
        db.commit()

        cursor.close()

        return jsonify({'message': 'Gyermek neve sikeresen frissítve'}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

@app.route('/<class_name>/children/<int:child_id>', methods=['DELETE'])
def delete_child(class_name, child_id):
    try:
        # Connect to the database dynamically using the class name
        db = getattr(g, 'db', None)
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = db.cursor()

        # Perform a soft delete by setting the isDeleted flag to TRUE
        query = "UPDATE children SET isDeleted = 1 WHERE id = %s"
        cursor.execute(query, (child_id,))
        db.commit()

        cursor.close()

        return jsonify({'message': 'Név sikeresen törölve a listából'}), 200

    except Exception as e:
        print("Error:", str(e))
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

@app.route('/<class_name>/student/<int:student_id>/account-movements', methods=['GET'])
def get_student_account_movements(class_name, student_id):
    db = get_db_connection(class_name)
    cursor = db.cursor(dictionary=True)
    
    query = "SELECT * FROM transactions WHERE child_id = %s"
    cursor.execute(query, (student_id,))
    result = cursor.fetchall()

    cursor.close()
    return jsonify(result), 200

@app.before_request
def before_request():
    path_parts = request.path.split('/')
    if len(path_parts) > 1:
        class_name = path_parts[1]  # Extract the class name from the path
        g.db = get_db_connection(class_name)

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

# Endpoint to create a new class
@app.route('/create-class', methods=['POST'])
def create_class():
    data = request.get_json()
    class_name = data.get('class_name')

    if not class_name:
        return jsonify({'error': 'Class name is required'}), 400

    result = create_class_db(class_name)  # Use the function from newclass.py

    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
