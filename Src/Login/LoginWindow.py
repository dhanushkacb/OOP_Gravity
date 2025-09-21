import tkinter as tk
from tkinter import messagebox
from Src.db.Schema import USERS

class LoginWindow:
    def __init__(self, root, on_login_success):
        self.root = root
        self.root.title("GravityCore Login")
        self.root.geometry("300x200")
        self.on_login_success = on_login_success

        tk.Label(root, text="Username").pack(pady=5)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack()

        tk.Label(root, text="Password").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack()

        tk.Button(root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username in USERS and USERS[username]["password"] == password:
            role = USERS[username]["role"]
            self.on_login_success(self.root,role)
        else:
            messagebox.showerror("Error", "Invalid credentials!")