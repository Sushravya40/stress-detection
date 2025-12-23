from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS allowed_emails (
    id SERIAL PRIMARY KEY,
    email TEXT UNIQUE NOT NULL
);
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT,
    email TEXT UNIQUE,
    password TEXT
);
""")

conn.commit()
cur.close()
conn.close()

print("Tables created")
