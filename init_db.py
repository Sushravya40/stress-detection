import sqlite3
from werkzeug.security import generate_password_hash

conn = sqlite3.connect('database.sqlite')
cur = conn.cursor()

# 1. Create admin table
cur.execute("""
CREATE TABLE IF NOT EXISTS admin (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);
""")

# 2. Create allowed_emails table
cur.execute("""
CREATE TABLE IF NOT EXISTS allowed_emails (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL
);
""")

# 3. Create users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    id INTEGER PRIMARY KEY AUTOINCREMENT,
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
INSERT OR IGNORE INTO admin (email, password)
VALUES (?, ?)
""", ("admin@example.com", hashed_admin_pwd))

# Commit and close
conn.commit()
cur.close()
conn.close()

print("SQLite Database initialized successfully!")
