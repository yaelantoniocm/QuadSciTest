import psycopg2
from psycopg2 import sql
from dotenv import load_dotenv
import os
import config

from helpers.logger import logger

# Load environment variables from the .env file
load_dotenv()

# Settings for connecting to PostgreSQL
postgres_user = os.getenv('POSTGRES_USER')
postgres_password = os.getenv('POSTGRES_PASSWORD')
postgres_host = os.getenv('POSTGRES_HOST')
postgres_port = os.getenv('POSTGRES_PORT')

# Settings for the new database and user
new_db_name = os.getenv('DATABASE_NAME')
new_user = os.getenv('NEW_USER')
new_password = os.getenv('NEW_PASSWORD')


def check_database_exists(cursor, db_name):
    """
    Function to check if the database already exists.
    Args:
        cursor (cursor object): Cursor object for executing SQL query.
        db_name (str): Name of the database to verify.
    Returns:
        bool: True if the database exists, False otherwise.
    """
    cursor.execute("SELECT 1 FROM pg_database WHERE datname=%s", (db_name,))
    return cursor.fetchone() is not None

def check_user_exists(cursor, user_name):
    """
    Function to check if the user already exists.
    Args:
        cursor (cursor object): Cursor object for executing SQL query.
        user_name (str): Name of the user to check it
    Returns:
        bool: True if the user exists, False otherwise.
    """
    cursor.execute("SELECT 1 FROM pg_roles WHERE rolname=%s", (user_name,))
    return cursor.fetchone() is not None

def create_database_and_user():
    """
    Create the data base and the user if they doesn't exists.      
    Connect to PostgresSQL
    By default "dbname='postgres'" is a PostgreSQL database which usually always exists. 
    This database is used to perform administrative operations such as creating other databases and users
    Also help to check if a user or database already exists.
    Content: 
    dbname -> Connect to the default database 'postgres'
    user -> Administrative user
    password -> Administrative user password
    host -> PostgreSQL Host
    port -> PostgreSQL port
        """
        
    connection = None
    try:
        connection = psycopg2.connect(
        dbname ='postgres',
        user = postgres_user,
        password = postgres_password,
        host = postgres_host,
        port = postgres_port
        )
        
        # Enable autocommit to execute commands immediately
        connection.autocommit = True 
        cursor = connection.cursor()
        
        # We check if the database already exists
        if check_database_exists(cursor, new_db_name):
            logger.info(f"The database '{new_db_name}' already exists")
        else:
            # We create the database
            cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier(new_db_name)))
            logger.info(f"Database '{new_db_name}' created successfully.")
        if check_user_exists(cursor, new_user):
            logger.info(f"The user '{new_user}' already exists.")
        else:
            # We create the user and grant privileges
            cursor.execute(sql.SQL("CREATE USER {} WITH PASSWORD %s").format(sql.Identifier(new_user)), [new_password])
            cursor.execute(sql.SQL("GRANT ALL PRIVILEGES ON DATABASE {} TO {}").format(sql.Identifier(new_db_name), sql.Identifier(new_user)))
            logger.info(f"User '{new_user}' successfully created and granted privileges in the '{new_db_name}' database.")
    except Exception as e:
            logger.critical(f"Error creating database or user: {e}")
    finally:
        # We close the connection
        if connection:
            cursor.close()
            connection.close()

if __name__ == '__main__':
    create_database_and_user()