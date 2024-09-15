import mysql.connector
from mysql.connector import Error
import os

# Base configuration for MySQL connection (without database)
db_config_base = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

# SQL statements to create tables and add mock data
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);
"""

INSERT_MOCK_DATA_SQL = """
INSERT INTO children (name) VALUES
('John Doe'),
('Jane Smith'),
('Mike Johnson');
"""

def get_database_for_request(subdomain):
    db_name = f"{subdomain}_db"
    return db_name

def get_db_connection(subdomain, create_if_not_exists=True):
    db_name = get_database_for_request(subdomain)
    try:
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        connection.database = db_name
        cursor.close()
        connection.close()

        connection = mysql.connector.connect(database=db_name, **db_config_base)
        if create_if_not_exists:
            initialize_database(connection)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def initialize_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(CREATE_TABLE_SQL)
        cursor.execute(INSERT_MOCK_DATA_SQL)
        connection.commit()
        cursor.close()
        print(f"Database initialized successfully.")
    except Error as e:
        print(f"Error initializing the database: {e}")

def create_class_db(class_name):
    try:
        db_name = f"{class_name.lower()}_db"
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
        cursor.close()
        connection.close()

        # Initialize the new database with tables and mock data
        connection = mysql.connector.connect(database=db_name, **db_config_base)
        initialize_database(connection)
        connection.close()

        return {'success': True, 'message': f"Class '{class_name}' created successfully!"}
    except Error as e:
        print(f"Error creating class database: {e}")
        return {'error': 'Failed to create class'}
