import re

with open('app1.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace basic %s
content = content.replace("WHERE email=%s", "WHERE email=?")
content = content.replace("WHERE email = %s", "WHERE email = ?")
content = content.replace("VALUES (%s)", "VALUES (?)")
content = content.replace("WHERE id=%s", "WHERE id=?")
content = content.replace("VALUES (%s, %s, %s, %s, %s)", "VALUES (?, ?, ?, ?, ?)")
content = content.replace("VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", "VALUES (?, ?, ?, ?, ?, ?, ?, ?)")
content = content.replace("date >= %s", "date >= ?")

# Replace postgres specific ON CONFLICT DO NOTHING
content = content.replace("INSERT INTO allowed_emails", "INSERT OR IGNORE INTO allowed_emails")
content = content.replace("ON CONFLICT DO NOTHING", "")

with open('app1.py', 'w', encoding='utf-8') as f:
    f.write(content)
