import tkinter as tk
from Src.login.LoginWindow import LoginWindow
from Src.db.CreateDatabase import CreateDatabase
from Src.log.Logger import Logger

class App:
    def __init__(self, main_window, role):
        self.main_window = main_window
        self.role = role
        self.main_window.title(f"GravityCore - {self.role} Panel")
        self.main_window.geometry("800x600")

        tk.Label(self.main_window, text=f"Welcome {self.role}", font=("Arial", 16)).pack(pady=20)

def start_main_app(role):
    Logger.log("User logged in.")
    main_root = tk.Tk()
    App(main_root, role)
    main_root.mainloop()

if __name__ == "__main__":
    #init DB
    createDb=CreateDatabase()
    createDb.create_database()
    createDb.create_tables()
    Logger.log("Database and tables created successfully.")
    main_window = tk.Tk()
    app = LoginWindow(main_window, start_main_app)
    main_window.mainloop()
