#create table store schema
from Src.crypt.Security import Security
from Src.db.Connection import Connection
from datetime import datetime

class BaseModel:
    def __init__(self, table_name):
        self.table_name = table_name

    def select_all(self, columns="*"):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute(f"SELECT {columns} FROM {self.table_name}")
                return db_cursor.fetchall()

    def delete(self, column, value):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(f"DELETE FROM {self.table_name} WHERE {column} = %s", (value,))
            db_conn.commit()
            return True

class Users(BaseModel):
    def __init__(self):
        super().__init__("users")  # table name

    def insert(self, username, password, role):
        password_hash = Security.hash(password)
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                    (username, password_hash, role)
                )
            db_conn.commit()
            return True

    def update(self, username, new_password, new_role):
        password_hash = Security.hash(new_password)
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "UPDATE users SET password_hash=%s, role=%s WHERE username=%s",
                    (password_hash, new_role, username)
                )
            db_conn.commit()
            return True

    def authenticate(self, username, password):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "SELECT role FROM users WHERE username = %s AND password_hash = %s",
                    (username, Security.hash(password))
                )
                result = db_cursor.fetchone()
        return result[0] if result else None

    def change_password(self, user_id, new_password):
        password_hash = Security.hash(new_password)
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "UPDATE users SET password_hash = %s WHERE user_id = %s",
                    (password_hash, user_id)
                )
            db_conn.commit()
            return True
          
class Teachers(BaseModel):
    def __init__(self):
        super().__init__("teachers")

    def insert(self, name, subject, contact_no=None, email=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO teachers (name, subject, contact_no, email) VALUES (%s, %s, %s, %s)",
                    (name, subject, contact_no, email)
                )
            db_conn.commit()
            return True

    def update(self, teacher_id, name, subject, contact_no=None, email=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "UPDATE teachers SET name=%s, subject=%s, contact_no=%s, email=%s WHERE teacher_id=%s",
                    (name, subject, contact_no, email, teacher_id)
                )
            db_conn.commit()
            return True

        
class Students(BaseModel):
    def __init__(self):
        super().__init__("students")

    def insert(self, name, registration_year, registration_month,
               contact_no=None, discount_percent=0.00, email=None, stream=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO students 
                    (name, registration_year, registration_month, contact_no, discount_percent, email, stream) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (name, registration_year, registration_month, contact_no, discount_percent, email, stream)
                )
            db_conn.commit()
            return True

    def update(self, student_id, name, registration_year, registration_month,
               contact_no=None, discount_percent=0.00, email=None, stream=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE students 
                    SET name=%s, registration_year=%s, registration_month=%s, 
                        contact_no=%s, discount_percent=%s, email=%s, stream=%s
                    WHERE student_id=%s
                    """,
                    (name, registration_year, registration_month, contact_no, discount_percent, email, stream, student_id)
                )
            db_conn.commit()
            return True
        
    def select_by_contact(self, contact_no):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT student_id FROM students WHERE contact_no = %s",(contact_no,)
                )
                return db_cursor.fetchone()
        
class ClassRoom(BaseModel):
    def __init__(self):
        super().__init__("classrooms")

    def insert(self, classroom_code, capacity, has_ac=False, has_whiteboard=False, has_screen=False):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO classrooms (classroom_code, capacity, has_ac, has_whiteboard, has_screen) VALUES (%s, %s, %s, %s, %s)",
                    (classroom_code, capacity, has_ac, has_whiteboard, has_screen)
                )
            db_conn.commit()
            return True

    def update(self, classroom_code, capacity, has_ac, has_whiteboard, has_screen):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("UPDATE classrooms SET capacity = %s, has_ac = %s, has_whiteboard = %s, has_screen = %s WHERE classroom_code = %s",
                    (capacity, has_ac, has_whiteboard, has_screen, classroom_code)
                )
            db_conn.commit()
            return True
        
class Classes(BaseModel):
    def __init__(self):
        super().__init__("classes")

    def insert(self, teacher_id, subject, class_type, category, time_slot, classroom=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO classes 
                    (teacher_id, subject, class_type, category, time_slot, classroom) 
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (teacher_id, subject, class_type, category, time_slot, classroom)
                )
            db_conn.commit()
            return True

    def update(self, class_id, teacher_id, subject, class_type, category, time_slot, classroom=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE classes 
                    SET teacher_id=%s, subject=%s, class_type=%s, category=%s, time_slot=%s, classroom=%s 
                    WHERE class_id=%s
                    """,
                    (teacher_id, subject, class_type, category, time_slot, classroom, class_id)
                )
            db_conn.commit()
            return True


class Enrollments(BaseModel):
    def __init__(self):
        super().__init__("enrollments")
    def insert(self, student_id, class_id, enrolled_date=datetime.now()):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO enrollments (student_id, class_id, enrollment_date) VALUES (%s, %s, %s)",
                    (student_id, class_id, enrolled_date)
                )
            db_conn.commit()
            return True
            return True

    def update(self, enrollment_id, student_id, class_id,enrolled_date):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE enrollments 
                    SET student_id=%s, class_id=%s,enrollment_date=%s
                    WHERE enrollment_id=%s
                    """,
                    (student_id, class_id, enrolled_date, enrollment_id)
                )
            db_conn.commit()
            return True


class Payments(BaseModel):
    def __init__(self):
        super().__init__("payments")

    def insert(self, student_id, class_id, month, year, amount, payment_method, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO payments 
                    (student_id, class_id, month, year, amount, payment_method, remarks) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    """,
                    (student_id, class_id, month, year, amount, payment_method, remarks)
                )
            db_conn.commit()
            return True

    def update(self, payment_id, student_id, class_id, month, year, amount, payment_method, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE payments 
                    SET student_id=%s, class_id=%s, month=%s, year=%s, amount=%s, 
                        payment_method=%s, remarks=%s 
                    WHERE payment_id=%s
                    """,
                    (student_id, class_id, month, year, amount, payment_method, remarks, payment_id)
                )
            db_conn.commit()
            return True


class Attendance(BaseModel):
    def __init__(self):
        super().__init__("attendance")

    def insert(self, student_id, class_id, session_date, status):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO attendance 
                    (student_id, class_id, session_date, status) 
                    VALUES (%s, %s, %s, %s)
                    """,
                    (student_id, class_id, session_date, status)
                )
            db_conn.commit()
            return True

    def update(self, attendance_id, student_id, class_id, session_date, status):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE attendance 
                    SET student_id=%s, class_id=%s, session_date=%s, status=%s 
                    WHERE attendance_id=%s
                    """,
                    (student_id, class_id, session_date, status, attendance_id)
                )
            db_conn.commit()
            return True


class TuteDistribution(BaseModel):
    def __init__(self):
        super().__init__("tute_distribution")

    def insert(self, student_id, class_id, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO tute_distribution 
                    (student_id, class_id, remarks) 
                    VALUES (%s, %s, %s)
                    """,
                    (student_id, class_id, remarks)
                )
            db_conn.commit()
            return True

    def update(self, tute_id, student_id, class_id, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE tute_distribution 
                    SET student_id=%s, class_id=%s, remarks=%s 
                    WHERE tute_id=%s
                    """,
                    (student_id, class_id, remarks, tute_id)
                )
            db_conn.commit()
            return True


class BulkUploads(BaseModel):
    def __init__(self):
        super().__init__("bulk_uploads")

    def insert(self, upload_type, file_name, uploaded_by):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    INSERT INTO bulk_uploads 
                    (upload_type, file_name, uploaded_by) 
                    VALUES (%s, %s, %s)
                    """,
                    (upload_type, file_name, uploaded_by)
                )
            db_conn.commit()
            return True

    def update(self, upload_id, upload_type, file_name, uploaded_by):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    """
                    UPDATE bulk_uploads 
                    SET upload_type=%s, file_name=%s, uploaded_by=%s 
                    WHERE upload_id=%s
                    """,
                    (upload_type, file_name, uploaded_by, upload_id)
                )
            db_conn.commit()
            return True

class SystemSettings:
    def __init__(self):
        pass

    def add_setting(self, setting_key, setting_value):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO system_settings (setting_key, setting_value) VALUES (%s, %s)",
                    (setting_key, setting_value)
                )
            db_conn.commit()
            return True
    
    def get_settings(self, setting_key):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                settings=[]
                db_cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = %s", (setting_key,))
                for row in db_cursor.fetchall():
                    settings.append(row["setting_value"])
        return settings

    def get_user_roles(self):
        return self.get_settings("USER_ROLE")
    
    def get_class_type(self):
        return self.get_settings("CLS_TYPE")
    
    def get_class_category(self):
        return self.get_settings("CLS_CATEGORY")
    
    def get_subjects(self):
        return self.get_settings("SUBJECTS")
     
    def get_upload_types(self):
        return self.get_settings("UPLOAD_TYPE")
    
    def get_time_slot(self):
        return self.get_settings("TIME_SLOT")
    
    def get_streams(self):
        return self.get_settings("STREAM")
