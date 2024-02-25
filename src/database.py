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
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')


class OrderManager:
    DATABASE_FILE = 'database.db'
    TIMEZONE_OFFSET = 0  # Assuming offset in seconds

    def __init__(self) -> None:
        """Initialize the OrderManager instance by connecting to the database and creating a cursor"""
        self.connection = sqlite3.connect(self.DATABASE_FILE)
        self.cursor = self.connection.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            tgid INT,
            tg_nickname TEXT,
            product TEXT,
            is_open INTEGER,
            timestamp DATETIME
        )
        """)
        self.connection.commit()

    def get_active_orders(self) -> list:
        """Retrieve all active orders (orders that are not completed) from the database"""
        self.cursor.execute('SELECT * FROM orders WHERE is_open = 1')
        return self.cursor.fetchall()

    def get_order_by_id(self, order_id: int) -> list:
        """Get the information about exact order by knowing only its ID"""
        self.cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        return self.cursor.fetchone()

    def insert_order(self, tgid: int, tg_nickname: str, product: str) -> None:
        """Insert a new order into the database with the provided details and mark it as open"""
        timestamp = round(time.time()) + self.TIMEZONE_OFFSET
        values = (tgid, tg_nickname, product, 1, timestamp)
        self.cursor.execute("INSERT INTO orders(tgid, tg_nickname, product, is_open, timestamp) VALUES (?, ?, ?, ?, ?)", values)
        self.connection.commit()

    def delete_order(self, order_id: int) -> None:
        """Delete the order"""
        self.cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
        self.connection.commit()

    def close_connection(self) -> None:
        self.connection.close()


if __name__ == '__main__':
    # Example usage:
    order_manager = OrderManager()

    # Generating 10 random orders
    import random
    for i in range(10):
        order_manager.insert_order(random.randint(10000, 99999), 'anekobtw', 'design')

    # Getting data about all of them and writing it down in all_orders.txt
    all_orders_data = order_manager.get_active_orders()

    for order_data in all_orders_data:
        order_obj = Order(*order_data)
        with open('all_orders.txt', 'a') as f:
            f.write(f"""Order ID: {order_obj.order_id}
Telegram ID: {order_obj.tgid}
Telegram Nickname: {order_obj.tg_nickname}
Product: {order_obj.product}
Date and Time of Purchase: {order_obj.formatted_timestamp}

""")

    order_manager.close_connection()
