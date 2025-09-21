#handle db connection and return when required
import mysql.connector

from Src.db.Configuration import Configuration

class Connection:
    @staticmethod
    def Server():
        conn = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD
        )
        return conn
    @staticmethod
    def Database():
        conn = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD,
            database=Configuration.DB_NAME
        )
        return conn