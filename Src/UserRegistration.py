import tkinter as tk
from tkinter import messagebox
from Src.db.Schema import Users
import tkinter.ttk as ttk

class UserRegistration:

    def __init__(self):
        self.reg_window = tk.Toplevel()
        self.reg_window.title("User Registration")
        self.reg_window.geometry("420x520")
        self.reg_window.resizable(False, False)

        self._users = Users()
        # Main frame for form
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)


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

        self.submit_btn = tk.Button(
            self.form_frame,
            text="Register User",
            command=self.register_user,
            width=15
            # bg="#4CAF50",
            # fg="white"
        )
        self.submit_btn.grid(row=4, column=1, sticky="e", padx=10, pady=15)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("username", "role", "edit", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        # Define headings
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("edit", text="Edit")
        self.tree.heading("delete", text="Delete")

        # Column widths
        self.tree.column("username", width=150)
        self.tree.column("role", width=100)
        self.tree.column("edit", width=60, anchor="center")
        self.tree.column("delete", width=60, anchor="center")

        self.tree.pack(fill="both", expand=True)

        # Load existing users
        self.load_users()

        # Bind tree clicks
        self.tree.bind("<Double-1>", self.on_tree_item_click)

    def load_users(self):
        # Clear existing rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self._users.get_all_users()
        for user in users:
            # Insert user row with Edit/Delete text
            self.tree.insert("", "end", values=(user["username"], user["role"], "✏️ Edit", "🗑️ Delete"))

        # Bind single click (not double click)
        self.tree.bind("<Button-1>", self.on_tree_item_click)

    def on_tree_item_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region != "cell":
            return

        row_id = self.tree.identify_row(event.y)
        col = self.tree.identify_column(event.x)
        if not row_id or not col:
            return

        values = self.tree.item(row_id, "values")
        username = values[0]

        if col == "#3":  # Edit column
            self.open_edit_screen(username)
        elif col == "#4":  # Delete column
            self.delete_user(username)

    def open_edit_screen(self, username):
        """Open a popup window to edit user details."""
        edit_win = tk.Toplevel(self.reg_window)
        edit_win.title(f"Edit User: {username}")
        edit_win.geometry("350x200")
        edit_win.resizable(False, False)

        # Username (read-only)
        tk.Label(edit_win, text="Username:", font=("Arial", 10, "bold")).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        tk.Label(edit_win, text=username).grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # Password field
        tk.Label(edit_win, text="New Password:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        pwd_entry = tk.Entry(edit_win, show="*")
        pwd_entry.grid(row=1, column=1, padx=10, pady=10)

        # Role dropdown
        tk.Label(edit_win, text="Role:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        role_var = tk.StringVar()
        role_combo = ttk.Combobox(edit_win, textvariable=role_var, values=["Admin", "Staff"], state="readonly")
        role_combo.grid(row=2, column=1, padx=10, pady=10)

        # --- Inner function has access to edit_win ---
        def save_changes():
            new_pwd = pwd_entry.get()
            new_role = role_var.get()

            if not new_pwd:
                messagebox.showerror("Error", "Password cannot be empty", parent=edit_win)
                return

            # You must implement update_user() in Users class
            if self._users.update_user(username, new_pwd, new_role):
                messagebox.showinfo("Updated", f"User '{username}' updated successfully.", parent=edit_win)
                self.load_users()
                edit_win.destroy()
            else:
                messagebox.showerror("Error", "Failed to update user.", parent=edit_win)

        # Save button
        tk.Button(edit_win, text="Save", bg="blue", fg="white", command=save_changes).grid(
            row=3, column=1, pady=15, sticky="e"
        )

    def delete_user(self, username):
        if messagebox.askyesno("Delete", f"Are you sure you want to delete user '{username}'?"):
            self._users.delete_user(username)
            self.load_users()


    def register_user(self,event=None):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()
        self.role = self.role_var.get()

        if not self.username or not self.password:
            messagebox.showerror("Error", "Username and password are required")
            return

        if self._users.add_user(self.username, self.password, self.role):
            messagebox.showinfo("Success", "User registered successfully!")
            self.load_users() 
        else:
            messagebox.showerror("Error", "Failed to register user.")

        