from db import get_db_connection

conn = get_db_connection()
print("✅ Database connected successfully")
conn.close()
