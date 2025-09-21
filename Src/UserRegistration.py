import tkinter as tk
from tkinter import messagebox
from Src.db.Connection import Connection
from Src.db.Configuration import Configuration

def open_user_registration():
    reg_window = tk.Toplevel()
    reg_window.title("User Registration")
    reg_window.geometry("420x320")
    reg_window.resizable(False, False)

    # Main frame for form
    form_frame = tk.Frame(reg_window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
    form_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Title label
    tk.Label(form_frame, text="User Registration", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

    entry_width = 30

    # Username
    tk.Label(form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    username_entry = tk.Entry(form_frame, width=entry_width)
    username_entry.grid(row=1, column=1, padx=10, pady=5)
    username_entry.insert(0, "Enter username")
    username_entry.bind("<FocusIn>", lambda e: username_entry.delete(0, tk.END))
    username_entry.focus_set()

    # Password
    tk.Label(form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    password_entry = tk.Entry(form_frame, show="*", width=entry_width)
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    password_entry.insert(0, "Enter password")
    password_entry.bind("<FocusIn>", lambda e: password_entry.delete(0, tk.END))

    # Role
    tk.Label(form_frame, text="Role:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    role_var = tk.StringVar(value="Staff")
    role_menu = tk.OptionMenu(form_frame, role_var, "Admin", "Staff")
    role_menu.config(width=25)
    role_menu.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

    def register_user(event=None):
        username = username_entry.get()
        password = password_entry.get()
        role = role_var.get()

        if not username or username == "Enter username" or not password or password == "Enter password":
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

    # Register button
    submit_btn = tk.Button(form_frame, text="Register", command=register_user, font=("Arial", 12, "bold"), bg="#4CAF50", fg="white", relief=tk.RAISED)
    submit_btn.grid(row=4, column=1, sticky="e", padx=10, pady=20)

    # Bind Enter key to submit
    reg_window.bind("<Return>", register_user)