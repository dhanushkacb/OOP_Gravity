#create table store schema
from Src.crypt.Security import Security
from Src.db.Connection import Connection

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
            return db_cursor.rowcount > 0
        
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
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT user_id, username, role, created_at FROM users")
                users = db_cursor.fetchall()
        return users
    
    def get_all_users(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT user_id, username, role, created_at FROM users")
                users = db_cursor.fetchall()
        return users
    
    def delete_user(self, user_name):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM users WHERE username = %s", (user_name,))
            db_conn.commit()
            return True
        
    def update_user(self, username, new_password, new_role):
       
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
           
                db_cursor.execute(
                    "UPDATE users SET password_hash=%s, role=%s WHERE username=%s",
                    (new_password, new_role, username)
                )
                db_conn.commit()
            return db_cursor.rowcount > 0
        
    def change_password(self, user_id, new_password):
        new_password_hash = Security.hash(new_password)
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("UPDATE users SET password_hash = %s WHERE user_id = %s", (new_password_hash, user_id))
            db_conn.commit()
            return True
        
class Teachers:
    def __init__(self):
        pass

    def add_teacher(self, name, subject, contact_no=None, email=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO teachers (name, subject, contact_no, email) VALUES (%s, %s, %s, %s)",
                    (name, subject, contact_no, email)
                )
            db_conn.commit()
            return True
    
    def get_all_teachers(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM teachers")
                teachers = db_cursor.fetchall()
        return teachers
    
    def update_teacher(self, teacher_id, name, subject, contact_no=None, email=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "UPDATE teachers SET name = %s, subject = %s, contact_no = %s, email = %s WHERE teacher_id = %s",
                    (name, subject, contact_no, email, teacher_id)
                )
            db_conn.commit()
            return True
    
    def delete_teacher(self, teacher_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM teachers WHERE teacher_id = %s", (teacher_id,))
            db_conn.commit()
            return True
        
class Students:
    def __init__(self):
        pass

    def add_student(self, name, registration_year, registration_month, contact_no=None, discount_percent=0.00, email=None, stream=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO students (name, registration_year, registration_month, contact_no, discount_percent, email, stream) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (name, registration_year, registration_month, contact_no, discount_percent, email, stream)
                )
            db_conn.commit()
            return True
    
    def get_all_students(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM students")
                students = db_cursor.fetchall()
        return students
    
    def delete_student(self, student_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
            db_conn.commit()
            return True
        
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
        
class Classes:
    def __init__(self):
        pass

    def add_class(self, teacher_id, subject, class_type, category, time_slot, classroom=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO classes (teacher_id, subject, class_type, category, time_slot, classroom) VALUES (%s, %s, %s, %s, %s, %s)",
                    (teacher_id, subject, class_type, category, time_slot, classroom)
                )
            db_conn.commit()
            return True
    
    def get_all_classes(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM classes")
                classes = db_cursor.fetchall()
        return classes
    
    def delete_class(self, class_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM classes WHERE class_id = %s", (class_id,))
            db_conn.commit()
            return True 
        
class Enrollments:
    def __init__(self):
        pass

    def add_enrollment(self, student_id, class_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO enrollments (student_id, class_id) VALUES (%s, %s)",
                    (student_id, class_id)
                )
            db_conn.commit()
            return True
    
    def get_all_enrollments(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM enrollments")
                enrollments = db_cursor.fetchall()
        return enrollments
    
    def delete_enrollment(self, enrollment_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM enrollments WHERE enrollment_id = %s", (enrollment_id,))
            db_conn.commit()
            return True

class Payments:
    def __init__(self):
        pass

    def add_payment(self, student_id, class_id, month, year, amount, payment_method, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO payments (student_id, class_id, month, year, amount, payment_method, remarks) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (student_id, class_id, month, year, amount, payment_method, remarks)
                )
            db_conn.commit()
            return True
    
    def get_all_payments(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM payments")
                payments = db_cursor.fetchall()
        return payments
    
    def delete_payment(self, payment_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM payments WHERE payment_id = %s", (payment_id,))
            db_conn.commit()
            return True
        
class Attendance:
    def __init__(self):
        pass

    def add_attendance(self, student_id, class_id, session_date, status):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO attendance (student_id, class_id, session_date, status) VALUES (%s, %s, %s, %s)",
                    (student_id, class_id, session_date, status)
                )
            db_conn.commit()
            return True
    
    def get_all_attendance(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM attendance")
                attendance = db_cursor.fetchall()
        return attendance
    
    def delete_attendance(self, attendance_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM attendance WHERE attendance_id = %s", (attendance_id,))
            db_conn.commit()
            return True

class TuteDistribution:
    def __init__(self):
        pass

    def add_tute_distribution(self, student_id, class_id, remarks=None):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO tute_distribution (student_id, class_id, remarks) VALUES (%s, %s, %s)",
                    (student_id, class_id, remarks)
                )
            db_conn.commit()
            return True
    
    def get_all_tute_distributions(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM tute_distribution")
                distributions = db_cursor.fetchall()
        return distributions
    
    def delete_tute_distribution(self, tute_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM tute_distribution WHERE tute_id = %s", (tute_id,))
            db_conn.commit()
            return True
        
class BulkUploads:
    def __init__(self):
        pass

    def add_bulk_upload(self, upload_type, file_name, uploaded_by):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute(
                    "INSERT INTO bulk_uploads (upload_type, file_name, uploaded_by) VALUES (%s, %s, %s)",
                    (upload_type, file_name, uploaded_by)
                )
            db_conn.commit()
            return True
    
    def get_all_bulk_uploads(self):
        with Connection.Database() as db_conn:
            with db_conn.cursor(dictionary=True) as db_cursor:
                db_cursor.execute("SELECT * FROM bulk_uploads")
                uploads = db_cursor.fetchall()
        return uploads
    
    def delete_bulk_upload(self, upload_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM bulk_uploads WHERE upload_id = %s", (upload_id,))
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
                db_cursor.execute("SELECT setting_value FROM system_settings WHERE setting_key = %s", (setting_key))
                settings = db_cursor.fetchall()
        return settings

    def get_user_roles(self):
        return self.get_settings("USER_ROLE")
    
    def get_class_type(self):
        return self.get_settings("CLASS_TYPE")
    
    def get_class_category(self):
        return self.get_settings("CLASS_CATEGORY")
    
    def get_subjects(self):
        return self.get_settings("SUBJECTS")
    
    def get_attendance_status(self):
        return self.get_settings("ATTENDANCE")
    
    def get_upload_types(self):
        return self.get_settings("UPLOAD_TYPE")
