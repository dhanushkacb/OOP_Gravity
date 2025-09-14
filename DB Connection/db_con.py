import mysql.connector

db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="123@asdzxc",
    
)

#creating db cursor to perform sql operation
db_cursor = db_connection.cursor()

db_cursor.execute("CREATE DATABASE IF NOT EXISTS gravity_db")

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
db_cursor.execute("SHOW TABLES")

for table in db_cursor:
    print(table)