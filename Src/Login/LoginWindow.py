import tkinter as tk
import os
from tkinter import messagebox
from Src.db.Schema import Users
from Src.config.Settings import Settings
from Src.log.Logger import Logger
from Src.login import AccessInfo


class LoginWindow:
    def __init__(self, root, on_login_success):
        self._users = Users()
        self.root = root
        self.root.title("GravityCore Login")
        self.root.geometry("500x300")
        self.on_login_success = on_login_success

        # Main frame with border
        self.form_frame = tk.Frame(self.root, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        try:
            self.logo = tk.PhotoImage(file="Src/login/login.png")
            img_label = tk.Label(self.form_frame, image=self.logo)
            img_label.grid(row=0, column=0, columnspan=2, pady=(0, 15))
        except Exception as e:
            Logger.log(f"Image load failed: {e}")
            tk.Label(self.form_frame, text="GravityCore", font=("Arial", 20, "bold")).grid(
                row=0, column=0, columnspan=2, pady=(0, 15)
            )
             
        # Username
        tk.Label(self.form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.username_entry.focus_set()

        # Password
        tk.Label(self.form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", width=Settings.ENTRY_WIDTH)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Login button
        self.login_btn = tk.Button(
            self.form_frame,
            text="Login",
            command=self.login
        )
        self.login_btn.grid(row=3, column=0, columnspan=2, pady=15)

        # Grid weights
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=3)

        # Bind Enter key
        self.root.bind("<Return>", self.login)

    def login(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        auth = self._users.authenticate(username, password)

        if auth:
            user_id = auth["user_id"]
            role = auth["role"]
            AccessInfo.USER_ID=user_id
            AccessInfo.USERNAME=username
            AccessInfo.ROLE=role
            self.on_login_success(self.root, role)
        else:
            Logger.log(f"Invalid credentials!")
            messagebox.showerror("Error", "Invalid credentials!")
