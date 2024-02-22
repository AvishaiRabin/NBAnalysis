import sqlite3
import os
def establish_connection(db_path):
    """Establishes a connection to the SQLite database."""
    return sqlite3.connect(db_path)

def execute_sql_script(connection, script_path):
    """Executes an SQL script on the given database connection."""
    with open(script_path) as f:
        connection.executescript(f.read())

def commit_and_close_connection(connection):
    """Commits changes and closes the database connection."""
    connection.commit()
    connection.close()

def get_db_connection(db_name):
    """Establishes a connection to the SQLite database and configures it."""
    # Get the current directory of the script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    # Construct the path to the database file dynamically
    db_path = os.path.join(current_dir, '..', 'dbs', f'{db_name}.db')

    # Establishing connection
    connection = establish_connection(db_path)

    # Configuring connection
    connection.row_factory = sqlite3.Row

    return connection

