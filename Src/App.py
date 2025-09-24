import tkinter as tk
from tkinter import messagebox
from Src.ClassRoomRegistration import ClassroomRegistration
from Src.ClassSchedule import ClassSchedule
from Src.ImportStudentData import ImportStudentData
from Src.StudentAttendanceProcess import StudentAttendanceProcess
from Src.StudentEnrollments import StudentEnrollments
from Src.StudentPayments import StudentPayments
from Src.StudentRegistration import StudentRegistration
from Src.TeacherRegistration import TeacherRegistration
from Src.login.LoginWindow import LoginWindow
from Src.db.CreateDatabase import CreateDatabase
from Src.log.Logger import Logger
from Src.UserRegistration import UserRegistration
from Src.reports.StudentAttendanceSheet import StudentAttendanceSheet
from Src.reports.StudentRegistrationReport import StudentRegistrationReport

class App:
    def __init__(self, main_window, role):
        self.main_window = main_window
        self.role = role
        self.main_window.title(f"GravityCore - {self.role} Panel")
        self.main_window.geometry("800x600")
        try:
            self.main_window.attributes('-zoomed', True)  # Linux/Mac
        except:
            self.main_window.state('zoomed')  # Windows

        self.create_menu()
        # Main area
        self.main_frame = tk.Frame(self.main_window, bg="white")
        self.main_frame.pack(fill="both", expand=True)

        tk.Label(self.main_frame, text=f"Welcome {self.role}", font=("Arial", 16)).pack(pady=20)

    def create_menu(self):
        menubar = tk.Menu(self.main_window)

        # Configurations Menu (Admin only)
        config_menu = tk.Menu(menubar, tearoff=0)
        config_menu.add_command(label="User Management", command=self.open_user_registration)
        config_menu.add_command(label="Class Room Management", command=self.open_classroom_registration)
        config_menu.add_command(label="System Settings", command=self.not_implemented)
        if self.role == "Admin":
            menubar.add_cascade(label="Configurations", menu=config_menu)

        # Features Menu
        feature_menu = tk.Menu(menubar, tearoff=0)
        feature_menu.add_command(label="Student Management", command=self.open_student_registration)
        feature_menu.add_command(label="Teacher Management", command=self.open_teacher_registration)
        feature_menu.add_command(label="Class Management", command=self.open_class_schedule)
        menubar.add_cascade(label="Features", menu=feature_menu)

        # Operation Menu
        operation_menu = tk.Menu(menubar, tearoff=0)
        operation_menu.add_command(label="Student Enrollment", command=self.open_student_enrollments)
        operation_menu.add_command(label="Student Payments", command=self.open_student_payments)
        operation_menu.add_command(label="Class Management", command=self.not_implemented)
        menubar.add_cascade(label="Operation", menu=operation_menu)

        # Process Menu
        process_menu = tk.Menu(menubar, tearoff=0)
        process_menu.add_command(label="Import Student Record", command=self.open_import_students)
        process_menu.add_command(label="Import Monthly Payments", command=self.open_import_monthly_payments)
        process_menu.add_command(label="Import Attendance Records", command=self.open_import_attendance_records)
        menubar.add_cascade(label="Process", menu=process_menu)


        # Reports Menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Outstanding Payments", command=self.not_implemented)
        report_menu.add_command(label="Student Registration", command=self.report_student_registration)
        report_menu.add_command(label="Attendance Sheet",command=self.report_attendance_sheet)
        menubar.add_cascade(label="Reports", menu=report_menu)

        self.main_window.config(menu=menubar)

    def not_implemented(self):
        messagebox.showinfo("Info", "This feature is not implemented yet!")
          
    def open_user_registration(self):
        if self.role != "Admin":
            messagebox.showerror("Error", "Access denied! Admins only.")
            return
        UserRegistration()

    def open_classroom_registration(self):
        ClassroomRegistration()

    def open_teacher_registration(self):
        TeacherRegistration()

    def open_class_schedule(self):
        ClassSchedule()

    def open_student_registration(self):
        StudentRegistration()

    def open_student_enrollments(self):
        StudentEnrollments()

    def open_student_payments(self):
        StudentPayments()

    def open_import_students(self):
        ImportStudentData()

    def open_import_monthly_payments(self):
        self.not_implemented()

    def open_import_attendance_records(self):
        StudentAttendanceProcess()

    def report_student_registration(self):
        StudentRegistrationReport()

    def report_attendance_sheet(self):
        StudentAttendanceSheet()

def start_main_app(root, role):
    Logger.log("User logged in.")
    for widget in root.winfo_children():
        widget.destroy()
    App(root, role)

if __name__ == "__main__":
    #init DB
    createDb=CreateDatabase()
    createDb.create_database()
    Logger.log("Database and tables created successfully.")
    
    main_window = tk.Tk()
    window_width = 400
    window_height = 300
    screen_width = main_window.winfo_screenwidth()
    screen_height = main_window.winfo_screenheight()
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    main_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

    app = LoginWindow(main_window, start_main_app)
    main_window.mainloop()
