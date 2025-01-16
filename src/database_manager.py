import sqlite3
import threading

class DatabaseManager:
    def __init__(self, db_name="usage_data.db"):
        """
        Initialize the DatabaseManager with a connection to the SQLite database.
        """
        self.lock = threading.Lock()
        self.connection = sqlite3.connect(db_name, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        """
        Create the necessary tables in the database if they do not already exist.
        """
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS usage_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            self.connection.commit()

    def insert_usage(self, file_path):
        """
        Insert a record into the usage_history table whenever a file is used.

        Parameters:
            file_path (str): The path of the file that was used.
        """
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('''
                INSERT INTO usage_history (file_path) VALUES (?)
            ''', (file_path,))
            self.connection.commit()

    def get_usage_history(self, limit=50):
        """
        Retrieve the most recent file usage history.

        Parameters:
            limit (int): The maximum number of records to retrieve.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing file paths and timestamps.
        """
        with self.lock:
            cursor = self.connection.cursor()
            cursor.execute('''
                SELECT file_path, timestamp FROM usage_history ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            return cursor.fetchall()

    def close(self):
        """
        Close the database connection.
        """
        self.connection.close()