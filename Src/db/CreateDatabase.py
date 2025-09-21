#Create DB and tables if not exists
from Src.db.Configuration import Configuration
from Src.db.Connection import Connection

class CreateDatabase:
    
    def __init__(self):
        self.db_connection = Connection.Server()
        self.create_database()
        self.create_tables()

    def create_database(self):
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {Configuration.DB_NAME}")
        except Exception as e:
            print(f"Error creating database: {e}")

    def create_tables(self):
        try:
            db_cursor = self.db_connection.cursor()
            db_cursor.execute("USE gravity_db")

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('Admin', 'Staff') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        except Exception as e:
            print(f"Error creating tables: {e}")



createDb=CreateDatabase()
createDb.create_database()
createDb.create_tables()