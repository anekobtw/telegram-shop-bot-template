import sqlite3
import time
from datetime import datetime


class Order:
    def __init__(self, order_id, tgid, tg_nickname, product, is_open, timestamp) -> None:
        """Initialize an order object with provided attributes"""
        self.order_id = order_id
        self.tgid = tgid
        self.tg_nickname = tg_nickname
        self.product = product
        self.is_open = is_open
        self.timestamp = timestamp

    @property
    def formatted_timestamp(self) -> str:
        """Return the timestamp in a formatted string (YYYY-MM-DD HH:MM:SS)"""
        return datetime.fromtimestamp(self.timestamp).strftime("%Y-%m-%d %H:%M:%S")

    def all_data(self) -> str:
        return f"""Order ID: {self.order_id}
Telegram ID: {self.tgid}
Telegram Nickname: {self.tg_nickname}
Product: {self.product}
Date and Time of Purchase: {self.formatted_timestamp}

"""


class OrderManager:
    DATABASE_FILE = "database.db"
    TIMEZONE_OFFSET = 0  # Assuming offset in seconds

    def __init__(self) -> None:
        self.connection = sqlite3.connect(self.DATABASE_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tgid INT,
            tg_nickname TEXT,
            product TEXT,
            is_open INTEGER,
            timestamp DATETIME
        )
        """
        )
        self.connection.commit()

    def get_active_orders(self) -> list:
        """Retrieve all orders that are not completed from the database"""
        self.cursor.execute("SELECT * FROM orders WHERE is_open = 1")
        return self.cursor.fetchall()

    def get_user_orders(self, tgid: int) -> list:
        """Get the information about all user's orders"""
        self.cursor.execute("SELECT * FROM orders WHERE tgid = ?", (tgid,))
        return self.cursor.fetchall()

    def get_order(self, order_id: int) -> int:
        """Get the order info"""
        self.cursor.execute("SELECT * FROM orders WHERE order_id = ?", (order_id,))
        return self.cursor.fetchone()

    def insert_order(self, tgid: int, tg_nickname: str, product: str) -> None:
        """Insert a new order into the database with the provided details"""
        timestamp = round(time.time()) + self.TIMEZONE_OFFSET
        values = (tgid, tg_nickname, product, 1, timestamp)
        self.cursor.execute("INSERT INTO orders(tgid, tg_nickname, product, is_open, timestamp) VALUES (?, ?, ?, ?, ?)", values)
        self.connection.commit()

    def delete_order(self, order_id: int) -> None:
        """Delete the order"""
        self.cursor.execute("DELETE FROM orders WHERE order_id = ?", (order_id,))
        self.connection.commit()
