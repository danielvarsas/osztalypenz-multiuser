from flask import Blueprint, jsonify, request, g
from config.db import get_db_connection

transactions_bp = Blueprint('transactions', __name__)

@transactions_bp.route('/<class_name>/add-money', methods=['POST'])
def add_money(class_name):
    data = request.json
    child_id = data.get('child_id')
    amount = data.get('amount')

    if not child_id or not amount:
        return jsonify({'error': 'Both child ID and amount are required'}), 400

    connection = get_db_connection(f"{class_name.lower()}_db")

    if connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO transactions (child_id, amount, type) VALUES (%s, %s, 'add')", (child_id, amount))
        connection.commit()
        cursor.close()
        connection.close()
        return jsonify({'message': 'Tranzakció rögzítve'}), 200
    else:
        return jsonify({'error': 'Failed to connect to database'}), 500
        
@transactions_bp.route('/<class_name>/take-money', methods=['POST'])
def take_money(class_name):
    try:
        # Get the database connection for the specific class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

        data = request.json
        amount = data.get('amount')
        reason = data.get('reason')

        # Ensure that amount and reason are provided
        if not amount or not reason:
            return jsonify({'error': 'Összeg és ok is kell.'}), 400

        # Use the child_id for "Kivét" (you mentioned this is always ID 1 for the "kivét" child)
        child_id_of_kivet = 1

        cursor = connection.cursor()

        # Insert the transaction into the database
        query = "INSERT INTO transactions (child_id, amount, reason, type) VALUES (%s, %s, %s, 'take')"
        cursor.execute(query, (child_id_of_kivet, amount, reason))
        connection.commit()

        cursor.close()
        connection.close()

        # Return a success message
        message = f"{amount} összeg kivételre került, {reason} céllal."
        return jsonify({'message': message}), 200

    except Exception as e:
        print("Error:", str(e))  # Print the error to the console for debugging
        return jsonify({'error': str(e)}), 500

        
@transactions_bp.route('/<class_name>/account-movements', methods=['GET'])
def account_movements(class_name):
    try:
        # Get the database connection for the specific class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

        cursor = connection.cursor(dictionary=True)

        # Query to fetch account movements (transactions) along with the child names
        cursor.execute("""
            SELECT transactions.id, transactions.amount, transactions.reason, transactions.type, transactions.created_at, 
                   children.name AS child_name
            FROM transactions
            LEFT JOIN children ON transactions.child_id = children.id
            ORDER BY transactions.created_at DESC
        """)
        
        # Fetch all the results
        result = cursor.fetchall()
        
        cursor.close()
        connection.close()

        # Return the fetched account movements
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@transactions_bp.route('/<class_name>/<child_name>/account-movements', methods=['GET'])
def get_child_account_movements(class_name, child_name):
    try:
        # Connect to the class-specific database
        connection = get_db_connection(f"{class_name.lower()}_db")
        cursor = connection.cursor(dictionary=True)

        # Fetch the child ID based on the provided child name (url_name)
        cursor.execute("SELECT id FROM children WHERE url_name = %s LIMIT 1", (child_name,))
        child = cursor.fetchone()

        if not child:
            return jsonify({'error': 'Child not found'}), 404

        # Fetch all transactions for the specific child
        cursor.execute("SELECT * FROM transactions WHERE child_id = %s", (child['id'],))
        transactions = cursor.fetchall()

        cursor.close()
        connection.close()

        # Return the list of transactions
        return jsonify(transactions), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500        


