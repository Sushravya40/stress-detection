import os
import psycopg2
from werkzeug.security import generate_password_hash

DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    print("No DATABASE_URL found. Skipping database initialization.")
else:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    # 1. Create admin table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );
    """)

    # 2. Create allowed_emails table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS allowed_emails (
        id SERIAL PRIMARY KEY,
        email TEXT UNIQUE NOT NULL
    );
    """)

    # 3. Create users table
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

    # 4. Create stress_prediction table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS stress_prediction (
        id SERIAL PRIMARY KEY,
        email TEXT,
        heart_rate FLOAT,
        skin_conductivity FLOAT,
        hours_worked FLOAT,
        emails_sent FLOAT,
        meetings_attended FLOAT,
        prediction FLOAT,
        date DATE
    );
    """)

    # 5. Insert default admin with properly HASHED password
    hashed_admin_pwd = generate_password_hash("admin123")
    cur.execute("""
    INSERT INTO admin (email, password)
    VALUES (%s, %s)
    ON CONFLICT (email) DO NOTHING
    """, ("admin@example.com", hashed_admin_pwd))

    # Commit and close
    conn.commit()
    cur.close()
    conn.close()

    print("Database initialized successfully!")
