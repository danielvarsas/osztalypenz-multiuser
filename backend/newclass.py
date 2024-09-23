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


# SQL statements to create tables
CREATE_CHILDREN_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS children (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    url_name VARCHAR(255) NOT NULL,  -- Column for URL-friendly name
    isDeleted BOOLEAN DEFAULT FALSE  -- Column to mark soft deletion
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

# SQL statements to insert mock data
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
    # Dynamically construct the database name using the subdomain
    db_name = f"{subdomain}_db"  # Properly format the database name

    try:
        # Connect to the MySQL server without specifying a database
        connection = mysql.connector.connect(**db_config_base)
        cursor = connection.cursor()

        # Safely create the database using backticks to avoid SQL syntax errors
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        
        # Set the connection to use the newly created or existing database
        connection.database = db_name

        # Close the initial connection and cursor
        cursor.close()
        connection.close()

        # Reconnect to the MySQL server with the specified database
        connection = mysql.connector.connect(database=db_name, **db_config_base)

        # Initialize the database if required
        if create_if_not_exists:
            initialize_database(connection, add_mock_data=False)  # Do not add mock data on regular connection
        
        return connection

    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def initialize_database(connection, add_mock_data=True):
    """
    Initializes the database with the required tables.
    Optionally adds mock data only if add_mock_data is True.
    """
    try:
        cursor = connection.cursor()
        # Create tables
        cursor.execute(CREATE_CHILDREN_TABLE_SQL)
        cursor.execute(CREATE_TRANSACTIONS_TABLE_SQL)
        
        # Only insert mock data if add_mock_data is True
        if add_mock_data:
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
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        cursor.close()
        connection.close()

        # Initialize the new database with tables and mock data
        connection = mysql.connector.connect(database=db_name, **db_config_base)
        initialize_database(connection, add_mock_data=True)  # Only add mock data during class creation
        connection.close()

        return {'success': True, 'message': f"Class '{class_name}' created successfully!"}
    except Error as e:
        print(f"Error creating class database: {e}")
        return {'error': 'Failed to create class'}
