import sqlite3
import json
import os

# 原文件保留用于密码
PASSWORD_FILE = "passwords.json"
DB_PATH = "flight.db"

# ✅ 初始化密码 JSON 文件（保留）
if not os.path.exists(PASSWORD_FILE):
    with open(PASSWORD_FILE, 'w', encoding='utf-8') as f:
        json.dump({
            "admin": {"zyy": "123456"},
            "operator": {"wby": "12345678"}
        }, f, ensure_ascii=False)

# ✅ 初始化数据库（只初始化结构）
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            model TEXT,
            id TEXT PRIMARY KEY,
            departure TEXT,
            booked INTEGER,
            available INTEGER
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS routes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fid TEXT,
            name TEXT,
            pid TEXT,
            seat TEXT,
            status TEXT,
            FOREIGN KEY(fid) REFERENCES flights(id)
        )
    ''')

    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# 获取数据库连接
def get_connection():
    return sqlite3.connect(DB_PATH)

# 获取所有航班信息
def get_flights():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT id, model, departure, booked, available FROM flights")
    rows = cursor.fetchall()
    print(rows)  # ✅ 检查后台是否真的读出了内容
    result = {fid: {"model": model, "departure": departure, "booked": b, "available": a}
              for fid, model, departure, b, a in rows}
    conn.close()
    return result


# 获取所有航线信息
def get_routes():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fid, name, pid, seat, status FROM routes")
    routes = {}
    for fid, name, pid, seat, status in cursor.fetchall():
        routes.setdefault(fid, []).append({
            "name": name,
            "id": pid,
            "seat": seat,
            "status": status
        })
    conn.close()
    return routes


# 更新航班信息
def update_flight(fid, flight_data):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO flights (id, model, departure, booked, available)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            model=excluded.model,
            departure=excluded.departure,
            booked=excluded.booked,
            available=excluded.available
    ''', (fid, flight_data["model"], flight_data["departure"],
          flight_data["booked"], flight_data["available"]))
    conn.commit()
    conn.close()


# 保存航线信息
def save_routes(routes):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM routes")
    for fid in routes:
        for r in routes[fid]:
            cursor.execute(
                "INSERT INTO routes (fid, name, pid, seat, status) VALUES (?, ?, ?, ?, ?)",
                (fid, r["name"], r.get("id", ""), r.get("seat", ""), r.get("status", "预订"))
            )
    conn.commit()
    conn.close()



