import tkinter as tk
from tkinter import messagebox
from Src.login.LoginWindow import LoginWindow
from Src.db.CreateDatabase import CreateDatabase
from Src.log.Logger import Logger

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
        config_menu.add_command(label="User Management", command=self.not_implemented)
        config_menu.add_command(label="System Settings", command=self.not_implemented)
        if self.role == "Admin":
            menubar.add_cascade(label="Configurations", menu=config_menu)

        # Features Menu
        feature_menu = tk.Menu(menubar, tearoff=0)
        feature_menu.add_command(label="Student Management", command=self.not_implemented)
        feature_menu.add_command(label="Teacher Management", command=self.not_implemented)
        feature_menu.add_command(label="Class Management", command=self.not_implemented)
        menubar.add_cascade(label="Features", menu=feature_menu)

        # Reports Menu
        report_menu = tk.Menu(menubar, tearoff=0)
        report_menu.add_command(label="Outstanding Payments", command=self.not_implemented)
        report_menu.add_command(label="Student Registrations", command=self.not_implemented)
        menubar.add_cascade(label="Reports", menu=report_menu)

        self.main_window.config(menu=menubar)

    def not_implemented(self):
        messagebox.showinfo("Info", "This feature is not implemented yet!")
          
def start_main_app(root, role):
    Logger.log("User logged in.")
    for widget in root.winfo_children():
        widget.destroy()
    App(root, role)

if __name__ == "__main__":
    #init DB
    createDb=CreateDatabase()
    createDb.create_database()
    createDb.create_tables()
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
