from db import get_db_connection

conn = get_db_connection()
cur = conn.cursor()

cur.execute("""
INSERT INTO admin (email, password)
VALUES (%s, %s)
ON CONFLICT (email) DO NOTHING
""", ("admin@example.com", "admin123"))

conn.commit()
cur.close()
conn.close()

print("Admin user inserted")
