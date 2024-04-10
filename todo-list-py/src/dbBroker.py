import sqlite3
from datetime import datetime
from item import Item
import logging

logging.basicConfig(level=logging.INFO)


class DbBroker:
    DB_URL = "todolist.db"

    @staticmethod
    def get_connection():
        try:
            connection = sqlite3.connect(DbBroker.DB_URL)
            logging.info("Successfully connected to the database.")
            return connection
        except Exception as e:
            logging.error("Error connecting to the database: %s", e)
            raise

    from datetime import datetime

    @staticmethod
    def get_all_items():
        with DbBroker.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM Item")
            rows = cursor.fetchall()

            item_list = []
            for row in rows:
                id, description, done, date_data = row
                # Check if date_data is a string and convert it to a datetime object
                if isinstance(date_data, str):
                    try:
                        # Attempt to convert the string to a datetime object
                        date = datetime.strptime(date_data, '%Y-%m-%d').date()
                    except ValueError:
                        # Handle the case where the string is not in the expected format
                        print(f"Invalid date format for item {id}: {date_data}")
                        continue  # Skip this item if the date cannot be parsed
                else:
                    # If date_data is not a string, proceed with your original logic
                    try:
                        date = datetime.fromtimestamp(date_data).date()
                    except ValueError:
                        date = datetime.fromtimestamp(date_data / 1000).date()
                item_list.append(Item(id, description, done, date))
            return item_list

    @staticmethod
    def get_item(id):
        with DbBroker.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("SELECT id, description, done, date FROM Item WHERE id = ?", (id,))
            row = cursor.fetchone()

            if row:
                id, description, done, date_data = row
                try:
                    date = datetime.fromtimestamp(date_data).date()
                except ValueError:
                    # Convert timestamp from milliseconds to seconds
                    date = datetime.fromtimestamp(date_data / 1000).date()
                return Item(id, description, done, date)
            else:
                raise Exception("No item found with ID: " + str(id))

    @staticmethod
    def add_item(item):
        with DbBroker.get_connection() as connection:
            cursor = connection.cursor()
            # Convert date to Unix timestamp
            timestamp = int(item.date.timestamp())
            cursor.execute("INSERT INTO Item (description, done, date) VALUES (?, ?, ?)",
                           (item.description, item.done, timestamp))
            connection.commit()

    @staticmethod
    def delete_item(item):
        with DbBroker.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM Item WHERE description = ?", (item.description,))
            deleted = cursor.rowcount
            connection.commit()
            if deleted > 0:
                return True
            else:
                raise Exception("No item found to delete")

    @staticmethod
    def finish_item(item):
        with DbBroker.get_connection() as connection:
            cursor = connection.cursor()
            cursor.execute("UPDATE Item SET done = 1 WHERE description = ?", (item.description,))
            connection.commit()
