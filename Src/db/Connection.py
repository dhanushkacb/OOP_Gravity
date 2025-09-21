#handle db connection and return when required
import mysql.connector

from db.Connection import Configuration

class Connection:
    def Server():
        conn = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD
        )
        return conn

    def Database():
        conn = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD,
            database=Configuration.DB_NAME
        )
        return conn