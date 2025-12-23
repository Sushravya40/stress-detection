# db.py
import os
import psycopg2

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    if not DATABASE_URL:
        raise Exception("DATABASE_URL environment variable not set")
    return psycopg2.connect(DATABASE_URL)
