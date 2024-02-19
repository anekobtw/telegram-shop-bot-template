import sqlite3
import time
from datetime import datetime

import config

# Connect to the database
con = sqlite3.connect('database.db')
cur = con.cursor()

# Create the 'orders' table if it doesn't exist
cur.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        tgid INT,
        tg_nickname TEXT,
        order_type TEXT,
        timestamp DATETIME
    )
""")

# Getters
def get_tgid(order_id: int) -> int:
    res = cur.execute("SELECT tgid FROM orders WHERE order_id=?", (order_id,))
    return res.fetchone()[0]

def get_first_order() -> list:
    orders = cur.execute('SELECT * FROM orders').fetchall()
    for order in orders:
        if get_place_in_queue(order[0]) == 1:
            return get_order_info(order)
    return 'Заказов нет.'

def get_order_by_order_id(order_id: int) -> list:
    res = cur.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
    return res.fetchall()[0]

def get_place_in_queue(order_id: int) -> int:
    premium_orders = cur.execute('SELECT order_id FROM orders WHERE status = 1 AND is_premium = 1').fetchall()
    not_premium_orders = cur.execute('SELECT order_id FROM orders WHERE status = 1 AND is_premium = 0').fetchall()

    all_orders = premium_orders + not_premium_orders

    my_order_status = cur.execute('SELECT status FROM orders WHERE order_id = ?', (order_id,)).fetchone()[0]

    if my_order_status == 1:
        return all_orders.index((order_id,)) + 1

def get_user_latest_order_id(tgid: int) -> int:
    res = cur.execute('SELECT * FROM orders WHERE tgid=?', (tgid,))
    return int(res.fetchall()[-1][0])

def get_user_orders(tgid: int) -> list:
    res = cur.execute('SELECT * FROM orders WHERE tgid = ?', (tgid,))
    return res.fetchall()

def get_order_info(order: list) -> str:
    info_text = f'''
Никнейм в ютубе: {order[2]}
Никнейм в телеграме: {order[3]}

Товар: {order[4]}
ТЗ:
{order[5]}

Айди заказа: {order[0]}
Дата и время покупки (мск): {datetime.fromtimestamp(order[6])}

Турбо режим: {variables.tf_states[order[7]]}
'''
    
    return info_text

# Others
def insert(tgid: int, yt_nickname: str, tg_nickname: str, order_type: str, TA: str, is_turbo: bool) -> None:
    cur.execute("""
        INSERT INTO orders(tgid, yt_nickname, tg_nickname, order_type, TA, timestamp, is_turbo)  -- Change field name here
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (tgid, yt_nickname, tg_nickname, order_type, TA, round(time.time() + 14400), is_turbo))
    con.commit()

def delete(order_id: int) -> None:
    cur.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
    con.commit()
