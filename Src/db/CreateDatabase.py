#Create DB and tables if not exists
from Src.crypt import Security
from Src.db.Configuration import Configuration
from Src.db.Connection import Connection
from Src.log.Logger import Logger
from Src.crypt.Security import Security

class CreateDatabase:
    
    def __init__(self):
        self.db_connection = Connection.Server()
        self.create_database()
        self.create_tables()
        self.create_admin_user()
        self.init_system_settings()

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
                role VARCHAR(100) NOT NULL,
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
                contact_no VARCHAR(20) NOT NULL UNIQUE,
                discount_percent DECIMAL(5,2) DEFAULT 0.00,
                email VARCHAR(100),
                stream VARCHAR(50),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS classrooms (
                classroom_code VARCHAR(20) PRIMARY KEY,
                capacity INT NOT NULL,
                has_ac BOOLEAN DEFAULT FALSE, 
                has_whiteboard BOOLEAN DEFAULT TRUE,
                has_screen BOOLEAN DEFAULT FALSE
                )
          """)
            
            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS classes (
                class_id INT AUTO_INCREMENT PRIMARY KEY,
                teacher_id INT NOT NULL,
                subject VARCHAR(100) NOT NULL,
                class_type VARCHAR(100) NOT NULL,
                category VARCHAR(100) NOT NULL,
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
                status BOOLEAN NOT NULL,
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
                upload_type VARCHAR(100),
                file_name VARCHAR(255),
                uploaded_by INT,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (uploaded_by) REFERENCES Users(user_id)
                    ON DELETE SET NULL
            )
            """)

            db_cursor.execute("""
                CREATE TABLE IF NOT EXISTS system_settings (
                setting_id INT AUTO_INCREMENT PRIMARY KEY,
                setting_key VARCHAR(50) NOT NULL,
                setting_value VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE KEY uq_setting (setting_key, setting_value)
            )
            """)

        except Exception as e:
            print(f"Error creating tables: {e}")

    def create_admin_user(self):
        try:
            with Connection.Database() as db_conn:
                with db_conn.cursor() as db_cursor:
                    db_cursor.execute("SELECT COUNT(*) FROM users WHERE username = 'admin'")
                    admin_count = db_cursor.fetchone()[0]
                    if admin_count == 0:
                        admin_pwd_hash = Security.hash("123")
                        db_cursor.execute(
                            "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                            ("admin", admin_pwd_hash, "Admin")
                        )
                        db_conn.commit()
                        Logger.log("Default admin user created with username 'admin'")
        except Exception as e:
            Logger.log(f"Error creating user: {e}")

    def init_system_settings(self):
        try:
            with Connection.Database() as db_conn:
                with db_conn.cursor() as db_cursor:
                    default_settings = [
                        ("USER_ROLE", "Admin"),
                        ("USER_ROLE", "Staff"),
                        ("CLS_TYPE", "Group"),
                        ("CLS_TYPE", "Hall"),
                        ("CLS_CATEGORY", "Theory"),
                        ("CLS_CATEGORY", "Revision"),
                        ("SUBJECTS", "Physics"),
                        ("SUBJECTS", "Mathematics"),
                        ("SUBJECTS", "Chemistry"),
                        ("SUBJECTS", "Biology"),
                        ("SUBJECTS", "ICT"),                        
                        ("UPLOAD_TYPE", "Students"),
                        ("UPLOAD_TYPE", "Payments"),
                        ("UPLOAD_TYPE", "Attendance"),
                        ("TIME_SLOT","M-6-9"),
                        ("TIME_SLOT","M-9-12"),
                        ("TIME_SLOT","A-12-3"),
                        ("TIME_SLOT","E-3-6"),
                        ("TIME_SLOT","N-6-9"),
                        ("STREAM", "PHYSICS"),
                        ("STREAM", "BIO"),
                        ("STREAM", "ARTS"),
                        ("STREAM", "COMMERCE"),
                        ("STREAM", "ICT"),
                    ]
                    for key, value in default_settings:
                        db_cursor.execute(
                            """
                            INSERT IGNORE INTO system_settings (setting_key, setting_value)
                            VALUES (%s, %s)
                            """,
                            (key, value)
                        )
                    db_conn.commit()
                    Logger.log("Default system settings initialized.")
        except Exception as e:
            Logger.log(f"Error initializing system settings: {e}")

