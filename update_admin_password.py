from db import get_db_connection
from werkzeug.security import generate_password_hash

conn = get_db_connection()
cur = conn.cursor()

hashed = generate_password_hash("admin123")

cur.execute(
    "UPDATE admin SET password=%s WHERE email=%s",
    (hashed, "admin@example.com")
)

conn.commit()
cur.close()
conn.close()

print("Admin password hashed")
