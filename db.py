import sqlite3

def get_db_connection():
    conn = sqlite3.connect('database.sqlite')
    # Optional: return rows as dicts or tuples. 
    # psycopg2 returns tuples by default, sqlite3 returns tuples by default too.
    return conn
