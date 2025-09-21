import tkinter as tk
from tkinter import messagebox
from Src.config import Settings
from Src.db.Schema import Users
from Src.config.Settings import Settings

class UserRegistration:

    def __init__(self):
        self.reg_window = tk.Toplevel()
        self._users=Users()
        
        self.reg_window.title("User Registration")
        self.reg_window.geometry("420x260")
        self.reg_window.resizable(False, False)

        # Main frame for form
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        tk.Label(self.form_frame, text="User Registration", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Username
        tk.Label(self.form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.username_entry.focus_set()

        # Password
        tk.Label(self.form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", width=Settings.ENTRY_WIDTH)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Role
        tk.Label(self.form_frame, text="Role:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.role_var = tk.StringVar(value="Staff")
        self.role_menu = tk.OptionMenu(self.form_frame, self.role_var, "Admin", "Staff")
        self.role_menu.config(width=Settings.ENTRY_WIDTH - 4)  # keep consistent width
        self.role_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Register button
        self.submit_btn = tk.Button(
            self.form_frame,
            text="Register",
            command=self.register_user,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white"
        )
        self.submit_btn.grid(row=4, column=0, columnspan=2, pady=20)

        # Grid weight for nice expansion
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=3)

        # Bind Enter
        self.reg_window.bind("<Return>", self.register_user)

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

        