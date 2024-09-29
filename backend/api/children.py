from flask import Blueprint, jsonify, request, g
from config.db import get_db_connection
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
            return jsonify({'error': 'Failed to connect to class database'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@children_bp.route('/<class_name>/children', methods=['POST'])
def add_child(class_name):
    try:
        data = request.json
        child_name = data.get('name')
        email = data.get('email') 

        if not child_name or not email:
            return jsonify({'error': 'Child name and email are required'}), 400

        # Generate URL-friendly name
        url_name = unidecode.unidecode(child_name.lower()).replace(' ', '-')

        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database'}), 500

        cursor = connection.cursor()

        # Insert the new child into the children table
        cursor.execute("INSERT INTO children (name, url_name, email) VALUES (%s, %s, %s)", 
                       (child_name, url_name, email))
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
            return jsonify({'error': 'Both name and email are required'}), 400

        # Generate URL-friendly name (for url_name)
        url_name = unidecode.unidecode(new_name.lower()).replace(' ', '-')

        # Get the database connection for the correct class
        connection = get_db_connection(f"{class_name.lower()}_db")
        if not connection:
            return jsonify({'error': 'Failed to connect to class database'}), 500

        cursor = connection.cursor()

        # Update the child's name, url_name, and email in the database
        query = "UPDATE children SET name = %s, url_name = %s, email = %s WHERE id = %s"
        cursor.execute(query, (new_name, url_name, new_email, child_id))
        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({'message': 'Child updated successfully'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
