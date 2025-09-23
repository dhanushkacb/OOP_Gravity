import tkinter as tk
from tkinter import messagebox, ttk
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Users

class UserRegistration(BaseRegistration):

    def __init__(self, entity_name="User"):
        super().__init__(model=Users(), entity_name=entity_name, key_column="username")
        self.reg_window = tk.Toplevel()
        self.selected_username = None
        
        self.reg_window.title(f"{entity_name} Registration")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Username
        tk.Label(self.form_frame, text="Username:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.username_entry = tk.Entry(self.form_frame, width=30)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.username_entry.focus_set()

        # Password
        tk.Label(self.form_frame, text="Password:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.password_entry = tk.Entry(self.form_frame, show="*", width=30)
        self.password_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Role
        tk.Label(self.form_frame, text="Role:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.role_var = tk.StringVar(value="Staff")
        self.role_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.role_var,
            values=["Admin", "Staff"],
            width=27,
            state="readonly"
        )
        self.role_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # --- Action Buttons ---
        self.submit_btn = tk.Button(self.form_frame, text="Save", command=self.save_record)
        self.delete_btn = tk.Button(self.form_frame, text="Delete", width=20, command=self.delete_record)
        self.clear_btn = tk.Button(self.form_frame, text="Clear", command=self.clear_form)

        self.submit_btn.grid(row=4, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=4, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=4, column=2, pady=20, padx=5, sticky="ew")

        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("username", "role", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        # Scrollbar
        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Tree headings
        self.tree.heading("username", text="Username")
        self.tree.heading("role", text="Role")
        self.tree.heading("delete", text="Delete")

        for col in columns:
            self.tree.column(col, width=120, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_item_click)
        self.tree.pack(fill="both", expand=True)
        self.reg_window.bind("<Return>", self.save_record)

        self.load_records()

    # --- CRUD Operations ---
    def save_record(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username or not password:
            messagebox.showerror("Error", "Username and password are required")
            return

        if self._model.insert(username, password, role):
            messagebox.showinfo("Success", "User registered successfully!")
            self.load_records()
        else:
            messagebox.showerror("Error", "Failed to register user.")

    def load_records(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        users = self._model.select_all()
        for u in users:
            self.tree.insert("", "end", values=(u["username"], u["role"], "🗑️ Delete"))
        self.clear_form()

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        # Fill form with selected user
        self.username_entry.config(state="normal")
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, values[0])
        self.username_entry.config(state="readonly")

        self.role_var.set(values[1])
        self.password_entry.delete(0, tk.END)

        self.selected_username = values[0]
        self.submit_btn.config(text="Update", command=self.update_record)

    def update_record(self, event=None):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_var.get()

        if not username:
            messagebox.showerror("Error", "Username is required")
            return
        if not password:
            messagebox.showerror("Error", "Password cannot be empty when updating")
            return

        if self._model.update(username, password, role):
            messagebox.showinfo("Success", "User updated successfully!")
            self.load_records()
        else:
            messagebox.showerror("Error", "Failed to update user.")

    def clear_form(self):
        self.username_entry.config(state="normal")
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.role_var.set("Staff")
        self.selected_username = None
        self.submit_btn.config(text="Save", command=self.save_record)
