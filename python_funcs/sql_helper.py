import sqlite3

def get_db_connection(db_name):
    conn = sqlite3.connect(f'dbs/{db_name}.db')
    conn.row_factory = sqlite3.Row
    return conn