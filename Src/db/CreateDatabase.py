#Create DB and tables if not exists
from Src.crypt import Security
from Src.db.Configuration import Configuration
from Src.db.Connection import Connection
from Src.log.Logger import Logger

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
            db_cursor.execute(f"USE {Configuration.DB_NAME}")

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                user_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                role ENUM('Admin', 'Staff') NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS teachers (
                teacher_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                subject VARCHAR(100) NOT NULL,
                contact_no VARCHAR(20),
                email VARCHAR(100),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                registration_year INT NOT NULL,
                registration_month INT NOT NULL,
                contact_no VARCHAR(20),
                discount_percent DECIMAL(5,2) DEFAULT 0.00,
                email VARCHAR(100),
                stream VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                class_id INT AUTO_INCREMENT PRIMARY KEY,
                teacher_id INT NOT NULL,
                subject VARCHAR(100) NOT NULL,
                class_type ENUM('Group', 'Hall') NOT NULL,
                category ENUM('Theory', 'Revision') NOT NULL,
                time_slot VARCHAR(50) NOT NULL,
                classroom VARCHAR(50),
                FOREIGN KEY (teacher_id) REFERENCES teachers(teacher_id)
                    ON DELETE CASCADE ON UPDATE CASCADE
                ) 
            """)    

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS enrollments (
                enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                enrollment_date DATE DEFAULT (CURRENT_DATE),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE(student_id, class_id)
                )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS payments (
                payment_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                month INT NOT NULL,
                year INT NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                discount_applied DECIMAL(5,2) DEFAULT 0.00,
                paid_on DATE DEFAULT (CURRENT_DATE),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE(student_id, class_id, month, year) 
            )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS attendance (
                attendance_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                session_date DATE NOT NULL,
                status ENUM('Present', 'Absent') DEFAULT 'Present',
                FOREIGN KEY (student_id) REFERENCES Students(student_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                UNIQUE(student_id, class_id, session_date)
            )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS tute_distribution (
                tute_id INT AUTO_INCREMENT PRIMARY KEY,
                student_id INT NOT NULL,
                class_id INT NOT NULL,
                distribution_date DATE DEFAULT (CURRENT_DATE),
                remarks VARCHAR(255),
                FOREIGN KEY (student_id) REFERENCES students(student_id)
                    ON DELETE CASCADE ON UPDATE CASCADE,
                FOREIGN KEY (class_id) REFERENCES classes(class_id)
                    ON DELETE CASCADE ON UPDATE CASCADE
            )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS bulk_uploads (
                upload_id INT AUTO_INCREMENT PRIMARY KEY,
                upload_type ENUM('Students', 'Payments'),
                file_name VARCHAR(255),
                uploaded_by INT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
                    ON DELETE SET NULL
            )
            """)


        except Exception as e:
            print(f"Error creating tables: {e}")

    def create_admin_user(self):
        try:
            with Connection.Database() as db_conn:
                with db_conn.cursor() as db_cursor:
                    db_cursor.execute("SELECT COUNT(*) FROM users WHERE user_id = 'admin'")
                    admin_count = db_cursor.fetchone()[0]
                    if admin_count == 0:
                        admin_pwd_hash = Security.hash('123')
                        db_cursor.execute(
                            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                            ("admin", admin_pwd_hash, "Admin")
                        )
                        db_conn.commit()
                        Logger.Log("Default admin user created with username 'admin'")
        except Exception as e:
            Logger.Log(f"Error creating user: {e}")
