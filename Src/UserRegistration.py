import tkinter as tk
from tkinter import messagebox
from Src.config import Settings
from Src.db.Schema import Users
from Src.config.Settings import Settings
import tkinter.ttk as ttk

class UserRegistration:

    def __init__(self):
        self.reg_window = tk.Toplevel()
        self.reg_window.title("User Registration")
        self.reg_window.geometry("420x320")
        self.reg_window.resizable(False, False)

        self._users = Users()
        # Main frame for form
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        tk.Label(self.form_frame, text="User Registration", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        entry_width = 30

        # Username
        tk.Label(self.form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.username_entry = tk.Entry(self.form_frame, width=entry_width)
        self.username_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Password
        tk.Label(self.form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", width=entry_width)
        self.password_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        #Role
        tk.Label(self.form_frame, text="Role:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.role_var = tk.StringVar(value="Staff")
        self.role_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.role_var,
            values=["Admin", "Staff"],
            width=27,
            state="readonly"
        )
        self.role_menu.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        btn_frame = tk.Frame(self.form_frame)
        btn_frame.grid(row=4, column=1, padx=10, pady=20, sticky="e")

        self.submit_btn = tk.Button(
            btn_frame,
            text="Register",
            command=self.register_user,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            width=12
        )
        self.submit_btn.pack(anchor="e")
        
        self.form_frame.columnconfigure(0, weight=0)
        self.form_frame.columnconfigure(1, weight=1)
    
    def register_user(self,event=None):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.role = self.role_var.get()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Username and password are required")
            return

        if self._users.add_user(self.username, self.password, self.role):
            messagebox.showinfo("Success", "User registered successfully!")
            self.reg_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to register user.")

        