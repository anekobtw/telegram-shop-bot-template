import sqlite3
import time
from datetime import datetime

con = sqlite3.connect('database.db')
cur = con.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tgid INT,
        tg_nickname TEXT,
        product TEXT,
        status INT,
        timestamp DATETIME
    )
""")


# <<< Getters >>>
def get_all(order_id: int = None, tgid: int = None) -> list:
    if order_id:
        res = cur.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        return res.fetchall()[0]
    elif tgid:
        res = cur.execute('SELECT * FROM orders WHERE tgid = ?', (tgid,))
        return res.fetchall()[0]

def get_tgid(order_id: int) -> int:
    res = cur.execute("SELECT tgid FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]

def get_tg_nickname(order_id: int) -> str:
    res = cur.execute("SELECT tg_nickname FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]

def get_product(order_id: int) -> str:
    res = cur.execute("SELECT product FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]

def get_status(order_id: int) -> int:
    res = cur.execute("SELECT status FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]

def get_timestamp(order_id: int) -> int:
    res = cur.execute("SELECT timestamp FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]


# <<< Useful functions >>>
def first_order() -> list:
    orders = cur.execute('SELECT * FROM orders').fetchall()
    for order in orders:
        if place_in_queue(order[0]) == 1:
            return get_order_info(order)
    return 'No orders yet.'

def place_in_queue(order_id: int) -> int:
    all_orders = cur.execute('SELECT order_id FROM orders WHERE status = 1').fetchall()
    my_order_status = cur.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,)).fetchone()[0]

    if my_order_status == 1:
        return all_orders.index((order_id,)) + 1

def user_latest_order_id(tgid: int) -> int:
    res = cur.execute('SELECT * FROM orders WHERE tgid=?', (tgid,))
    return int(res.fetchall()[-1][0])

def get_order_info(order: list) -> str:
    info_text = f'''Order id: {order[0]}
Telegram id: {order[1]}
Telegram nickname: {order[2]}
Product: {order[3]}
Date and time of purchase: {datetime.fromtimestamp(order[5])}

Place in queue: {place_in_queue(order[0])}
'''

    return info_text

# <<< Others >>>
def insert(tgid: int, tg_nickname: str, product: str) -> None:
    values = (tgid, tg_nickname, product, 0, round(time.time() + 14400))
    cur.execute("INSERT INTO orders(tgid, tg_nickname, product, status, timestamp) VALUES (?, ?, ?, ?, ?)", values)
    con.commit()

def delete(order_id: int) -> None:
    cur.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
    con.commit()
