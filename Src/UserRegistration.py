import tkinter as tk
from tkinter import messagebox
from Src.db.Connection import Connection
from Src.db.Configuration import Configuration

def open_user_registration():
    reg_window = tk.Toplevel()
    reg_window.title("User Registration")
    reg_window.geometry("400x300") 
    entry_width = 25

    tk.Label(reg_window, text="Username:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    username_entry = tk.Entry(reg_window, width=entry_width)
    username_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(reg_window, text="Password:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    password_entry = tk.Entry(reg_window, show="*", width=entry_width)
    password_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(reg_window, text="Role:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    role_var = tk.StringVar(value="Staff")
    role_menu = tk.OptionMenu(reg_window, role_var, "Admin", "Staff")
    role_menu.config(width=entry_width)
    role_menu.grid(row=2, column=1, padx=10, pady=5)

    def register_user():
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password required")
            return

        # Hash password (simple example, use a secure hash in production)
        import hashlib
        password_hash = hashlib.sha256(password.encode()).hexdigest()

        try:
            conn = Connection.Server()
            cursor = conn.cursor()
            cursor.execute(f"USE {Configuration.DB_NAME}")
            cursor.execute(
                "INSERT INTO users (username, password_hash, role) VALUES (%s, %s, %s)",
                (username, password_hash, role)
            )
            conn.commit()
            messagebox.showinfo("Success", "User registered successfully!")
            reg_window.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register user: {e}")

    submit_btn = tk.Button(reg_window, text="Register", command=register_user)
    submit_btn.grid(row=3, column=1, sticky="e", padx=10, pady=15)