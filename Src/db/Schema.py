#create table store schema
from Src.crypt.Security import Security
from Src.db.Connection import Connection


class Users:
    
    def __init__(self):
        pass

    def authenticate(self, username, password):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("SELECT role FROM users WHERE username = %s AND password_hash = %s", (username, Security.hash(password)))
                result = db_cursor.fetchone()
        if result:
            return result[0]
        return None
    
    def add_user(self, username, password, role):
        password_hash = Security.hash(password)
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    (username, password_hash, role)
                )
            db_conn.commit()
            return True

    def get_all_users(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("SELECT user_id, username, role, created_at FROM users")
                users = db_cursor.fetchall()
        return users