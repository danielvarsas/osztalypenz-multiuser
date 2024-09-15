from flask import Flask, request, jsonify, Blueprint
import mysql.connector
from flask_cors import CORS
from dotenv import load_dotenv
from mysql.connector import Error
import os
from auth import auth_bp  # Import the auth_bp Blueprint from auth.py
from newclass import get_db_connection, create_class_db  # Import the required functions

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
@app.route('/add-money', methods=['POST'])
def add_money():
    try:
        data = request.json
        print("Received data:", data)  # Debugging print statement
        child_id = data.get('child_id')
        amount = data.get('amount')
        child_name = get_child_name_by_id(child_id)
        # Ensure child_id and amount are provided
        if not child_id or not amount:
            return jsonify({'error': 'Add meg mindkét paramétert'}), 400

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert the transaction into the database
        query = "INSERT INTO transactions (child_id, amount, type) VALUES (%s, %s, 'add')"
        cursor.execute(query, (child_id, amount))
        connection.commit()

        cursor.close()
        connection.close()
        message = f"{amount} Befizetés könyvelve {child_name} tanulónak"
        return jsonify({'message': message}), 200 

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

# Route to take money
@app.route('/take-money', methods=['POST'])
def take_money():
    try:
        data = request.json
        print("Received data:", data)  # Debugging print statement
        amount = data.get('amount')
        reason = data.get('reason')

        # Ensure amount and reason are provided
        if not amount or not reason:
            return jsonify({'error': 'Összeget és okot is adj'}), 400

        # Use the child_id for "Kivét"
        child_id_of_kivet = 1  # Replace with the actual child_id of "Kivét"

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert the transaction into the database with the specific child_id
        query = "INSERT INTO transactions (child_id, amount, reason, type) VALUES (%s, %s, %s, 'take')"
        cursor.execute(query, (child_id_of_kivet, amount, reason))
        connection.commit()

        cursor.close()
        connection.close()

        message = f"{amount} Kivétel iktatva, {reason} céllal."
        return jsonify({'message': message}), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

# Route to get account movements
@app.route('/account-movements', methods=['GET'])
def account_movements():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

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
        connection.close()

        return jsonify(result), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

@app.route('/children', methods=['GET'])
def get_children():
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Fetch all children
        query = "SELECT id, name FROM children"
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(result), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console
        return jsonify({'error': str(e)}), 500

# Route to add a new child
@app.route('/children', methods=['POST'])
def add_child():
    try:
        data = request.json
        child_name = data.get('name')

        if not child_name:
            return jsonify({'error': 'Adj nevet'}), 400

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Insert the new child into the database
        query = "INSERT INTO children (name) VALUES (%s)"
        cursor.execute(query, (child_name,))
        connection.commit()

        # Get the ID of the newly inserted child
        new_child_id = cursor.lastrowid

        cursor.close()
        connection.close()

        # Return the newly created child's ID and name
        return jsonify({'id': new_child_id, 'name': child_name}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# Route to modify an existing child's name
@app.route('/children/<int:child_id>', methods=['PUT'])
def modify_child(child_id):
    try:
        data = request.json
        new_name = data.get('name')

        if not new_name:
            return jsonify({'error': 'Adj nevet'}), 400

        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Update the child's name in the database
        query = "UPDATE children SET name = %s WHERE id = %s"
        cursor.execute(query, (new_name, child_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Gyermek neve sikeresen frissítve'}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# Route to delete a child
@app.route('/children/<int:child_id>', methods=['DELETE'])
def delete_child(child_id):
    try:
        # Connect to the database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Delete the child from the database
        query = "DELETE FROM children WHERE id = %s"
        cursor.execute(query, (child_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Név sikeresen törölve a listából'}), 200

    except Exception as e:
        print("Error:", str(e))
        return jsonify({'error': str(e)}), 500

# Function to get child's name by ID
def get_child_name_by_id(child_id):
    try:
        # Establish the database connection
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        # Query to fetch the child's name by ID
        query = "SELECT name FROM children WHERE id = %s"
        cursor.execute(query, (child_id,))
        result = cursor.fetchone()

        # Return the child's name if found, otherwise return 'Unknown'
        return result['name'] if result else 'Unknown'

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return 'Unknown'
    
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

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
    app.run(debug=True)
