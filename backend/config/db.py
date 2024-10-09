import os
from mysql.connector import connect, Error
from dotenv import load_dotenv
import bcrypt

load_dotenv()

# Database configuration
db_config_base = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT')
}

db_config_default = {
    **db_config_base,
    'database': os.getenv('DB_NAME')
}

def get_db_connection(db_name=None):
    try:
        # Use the main database (db_config_default) if no specific db_name is provided
        config = db_config_default if db_name is None else {**db_config_base, 'database': db_name}
        connection = connect(**config)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise Exception(f"Database connection failed: {e}")

def create_database(subdomain):
    db_name = f"{subdomain}_db"
    try:
        connection = get_db_connection()  # Connect to MySQL server without specifying the database
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        connection.commit()
    except Error as e:
        print(f"Error creating database '{db_name}': {e}")
        raise Exception(f"Database creation failed: {e}")
    finally:
        connection.close()  # Always close the connection after use
    return db_name

def initialize_main_database(connection):
    try:
        with connection.cursor() as cursor:
            # Create the class_admins table in the main database if it doesn't exist
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS class_admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                class_name VARCHAR(255) NOT NULL UNIQUE,
                admin_email VARCHAR(255) NOT NULL,
                pin_code VARCHAR(255) NOT NULL  -- Adjusted size for hashed PIN
            );
            """)
        connection.commit()
        print("Main database initialized successfully.")
    except Error as e:
        print(f"Error initializing main database: {e}")
        raise Exception(f"Main database initialization failed: {e}")

def initialize_database(connection):
    try:
        with connection.cursor() as cursor:
            # SQL to create the children table in the class-specific database
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS children (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url_name VARCHAR(255) NOT NULL,
                email VARCHAR(255),
                isDeleted BOOLEAN DEFAULT FALSE
            );
            """)

            # SQL to create the transactions table in the class-specific database
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                child_id INT NOT NULL,
                amount DECIMAL(10, 2) NOT NULL,
                reason VARCHAR(255),
                type ENUM('add', 'take') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (child_id) REFERENCES children(id)
            );
            """)

            # Insert the "Kivét" child record
            cursor.execute("""
            INSERT IGNORE INTO children (id, name, url_name, email, isDeleted)
            VALUES (1, 'Kivét', 'kivet', NULL, FALSE);
            """)

        # Commit the transaction to ensure tables are created
        connection.commit()
        print("Class-specific database initialized successfully.")

    except Error as e:
        print(f"Error initializing class database: {e}")
        raise Exception(f"Class database initialization failed: {e}")

    finally:
        connection.close()  # Always close the connection after initialization

def hash_pin(pin_code):
    # Generate salt and hash the pin
    salt = bcrypt.gensalt()
    hashed_pin = bcrypt.hashpw(pin_code.encode('utf-8'), salt)
    return hashed_pin.decode('utf-8')

def check_pin(pin_code, hashed_pin):
    # Check if the provided pin matches the hashed pin
    return bcrypt.checkpw(pin_code.encode('utf-8'), hashed_pin.encode('utf-8'))
