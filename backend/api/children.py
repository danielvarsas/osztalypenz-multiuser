from flask import Blueprint, jsonify, request, g
from config.db import get_db_connection, hash_pin, check_pin
import unidecode 
        
children_bp = Blueprint('children', __name__)

@children_bp.route('/<class_name>/children', methods=['GET'])
def get_children(class_name):
    try:
        # Get the database connection for the specific class
        connection = get_db_connection(f"{class_name.lower()}_db")
        
        if connection:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT id, name, email, isDeleted FROM children WHERE isDeleted = FALSE;")
            result = cursor.fetchall()
            cursor.close()
            connection.close()
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@children_bp.route('/<class_name>/children', methods=['POST'])
def add_child(class_name):
    try:
        data = request.json
        child_name = data.get('name')
        email = data.get('email')
        pin_code = data.get('pin_code')

        if not child_name or not email or not pin_code:
            return jsonify({'error': 'Tanuló neve, email címe, és PIN kódja is kelletik :)'}), 400

        # Hash the pin code before storing it
        hashed_pin = hash_pin(pin_code)

        # Generate URL-friendly name
        url_name = unidecode.unidecode(child_name.lower()).replace(' ', '-')

        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

        cursor = connection.cursor()

        # Insert the new child into the children table, including hashed pin_code
        cursor.execute("INSERT INTO children (name, url_name, email, pin_code) VALUES (%s, %s, %s, %s)", 
                       (child_name, url_name, email, hashed_pin))
        connection.commit()

        # Get the last inserted child's ID for response
        child_id = cursor.lastrowid

        cursor.close()
        connection.close()

        # Return the inserted child's data, including ID, name, and email
        return jsonify({'id': child_id, 'name': child_name, 'url_name': url_name, 'email': email}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500



@children_bp.route('/<class_name>/children/<int:child_id>', methods=['PUT'])
def modify_child(class_name, child_id):
    try:
        data = request.json
        new_name = data.get('name')
        new_email = data.get('email')

        # Input validation
        if not new_name or not new_email:
            return jsonify({'error': 'Kell a név és az email cím is.'}), 400

        # Generate URL-friendly name (for url_name)
        url_name = unidecode.unidecode(new_name.lower()).replace(' ', '-')

        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database, Valami nem ok, szólj Daninak, javítson meg.'}), 500

        cursor = connection.cursor()

        # Update the child's name, url_name, and email in the database
        query = "UPDATE children SET name = %s, url_name = %s, email = %s WHERE id = %s"
        cursor.execute(query, (new_name, url_name, new_email, child_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Tanuló adatai frissítve.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@children_bp.route('/<class_name>/children/<child_id>/account-movements', methods=['GET'])
def get_child_account_movements(class_name, child_id):
    # Check if the child has been authenticated
    if not session.get(f'authenticated_child_{child_id}'):
        return jsonify({'error': 'Ajjaj, nem jó a PIN. Próbáld újra.'}), 403

    try:
        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

        cursor = connection.cursor(dictionary=True)

        # Fetch the account movements for the given child
        cursor.execute("SELECT * FROM transactions WHERE child_id = %s", (child_id,))
        movements = cursor.fetchall()

        cursor.close()
        connection.close()

        return jsonify(movements), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
        
@children_bp.route('/<class_name>/children/<int:child_id>', methods=['DELETE'])
def delete_child(class_name, child_id):
    try:
        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database. Valami nem ok, szólj Daninak, javítson meg.'}), 500

        cursor = connection.cursor()

        # Set isDeleted to TRUE for the given child
        query = "UPDATE children SET isDeleted = TRUE WHERE id = %s"
        cursor.execute(query, (child_id,))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Tanuló sikeresen törölve.'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

