from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT,
    age INT,
    mob TEXT
);
""")

conn.commit()
cur.close()
conn.close()

print("users table created successfully")
