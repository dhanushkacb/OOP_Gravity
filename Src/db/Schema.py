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
    
    def delete_user(self, user_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
            db_conn.commit()
            return True
        
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
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("SELECT * FROM teachers")
                teachers = db_cursor.fetchall()
        return teachers
    
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
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("SELECT * FROM students")
                students = db_cursor.fetchall()
        return students
    
    def delete_student(self, student_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
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
            with db_conn.cursor() as db_cursor:
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
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("SELECT * FROM enrollments")
                enrollments = db_cursor.fetchall()
        return enrollments
    
    def delete_enrollment(self, enrollment_id):
        with Connection.Database() as db_conn:
            with db_conn.cursor() as db_cursor:
                db_cursor.execute("DELETE FROM enrollments WHERE enrollment_id = %s", (enrollment_id,))
            db_conn.commit()
            return True
        