import sqlite3

conn = sqlite3.connect('flight.db')  # 替换为你的 DB_PATH
cursor = conn.cursor()

# 添加 pid 字段，如果已经存在则忽略
try:
    cursor.execute("ALTER TABLE routes ADD COLUMN pid TEXT")
except sqlite3.OperationalError:
    print("字段 pid 已存在")

conn.commit()
conn.close()

