import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.connection = sqlite3.connect(
            r"C:\Users\tttko\prometeusProject" + r"\become_qa_auto.db"
        )
        self.cursor = self.connection.cursor()

    def test_connection(self):
        sqlite_select_Query = "SELECT sqlite_version();"
        self.cursor.execute(sqlite_select_Query)
        record = self.cursor.fetchall()
        print(f"Connected successfully. SQLite Database Version is: {record}")

    def get_all_users(self):
        query = "SELECT name, address, city FROM customers"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def get_user_address_by_name(self, name):
        query = f"SELECT address, city, postalCode, country FROM customers WHERE name='{name}'"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def update_product_qnt_by_id(self, product_id, qnt):
        query = f"UPDATE products SET quantity = {qnt} WHERE id = {product_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def select_product_qnt_by_id(self, product_id):
        query = f"SELECT quantity FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def insert_product(self, product_id, name, description, qnt):
        query = f"INSERT OR REPLACE INTO products (id, name, description, quantity) \
            VALUES({product_id}, '{name}', '{description}', {qnt})"
        self.cursor.execute(query)
        self.connection.commit()

    def delete_product_by_id(self, product_id):
        query = f"DELETE FROM products WHERE id = {product_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def get_detailed_orders(self):
        query = "SELECT orders.id, customers.name, products.name, \
            products.description, orders.order_date \
            FROM orders \
            JOIN customers ON orders.customer_id = customers.id \
            JOIN products ON orders.product_id = products.id"
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        return record

    def insert_customer(self, name, address, city, postalCode, country):
        query = f"INSERT OR REPLACE INTO customers (name, address, city, postalCode, country)\
            VALUES('{name}', '{address}', '{city}', {postalCode}, '{country}')"
        self.cursor.execute(query)
        self.connection.commit()

    def delete_user_by_name(self, name):
        query = f"DELETE FROM customers WHERE name = '{name}'"
        self.cursor.execute(query)
        self.connection.commit()

    def select_user_by_name(self, name):
        query = f"SELECT * FROM customers WHERE name ='{name}'"
        self.cursor.execute(query)
        record = self.cursor.fetchone()
        return record

    def get_all_orders(self):
        query = "SELECT * FROM orders"
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def create_order(self, customer_id, product_id):
        date = datetime.now()
        order_date = date.strftime("%H:%M:%S")
        query = f"INSERT INTO orders (customer_id, product_id, order_date) \
            VALUES ({customer_id}, {product_id}, '{order_date}')"

        self.cursor.execute(query)
        self.connection.commit()

    def delete_order_by_id(self, order_id):
        query = f"DELETE FROM orders WHERE id = {order_id}"
        self.cursor.execute(query)
        self.connection.commit()

    def insert_user_with_invalid_name(self, name):
        try:
            query = f"INSERT INTO customers (name) \
                VALUES ({name})"
            self.cursor.execute(query)
            self.connection.commit()

        except sqlite3.ProgrammingError as e:
            pass

    def get_order_by_id(self, id):
        query = f"SELECT * FROM orders WHERE id = {id}"
        self.cursor.execute(query)
        return self.cursor.fetchone()

    def get_last_inserted_order(self):
        query = "SELECT * FROM orders ORDER BY id DESC LIMIT 1"
        self.cursor.execute(query)
        last_inserted_record = self.cursor.fetchone()
        return last_inserted_record

    def insert_order_with_invalid_data(self, customer_id, product_id):
        try:
            self.create_order(customer_id, product_id)
        except sqlite3.OperationalError as e:
            pass
