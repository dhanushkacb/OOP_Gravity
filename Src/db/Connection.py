#handle db connection and return when required
import mysql.connector

from db import Configuration

class Connection:
    def Server():
        db_connection = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD
        )
        return db_connection

    def Database():
        db_connection = mysql.connector.connect(
            host=Configuration.DB_SERVER,
            user=Configuration.DB_USER,
            password=Configuration.DB_PASSWORD,
            database=Configuration.DB_NAME
        )
        return db_connection