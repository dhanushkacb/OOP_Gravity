import tkinter as tk
from tkinter import messagebox,ttk
from Src.config.Settings import Settings
from Src.db.Schema import ClassRoom

class ClassroomRegistration:

    def __init__(self):
        self.reg_window = tk.Toplevel()
        self._classrooms = ClassRoom()
        self.selected_code = None

        self.reg_window.title("Classroom Registration")
        self.reg_window.resizable(False, False)

        # Main frame
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(
            self.form_frame,
            text="Classroom Registration",
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Classroom Code
        tk.Label(self.form_frame, text="Classroom Code:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.code_entry.focus_set()

        # Capacity
        tk.Label(self.form_frame, text="Capacity:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.capacity_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Facilities (Boolean options)
        self.has_ac_var = tk.BooleanVar(value=False)
        self.has_whiteboard_var = tk.BooleanVar(value=True)
        self.has_screen_var = tk.BooleanVar(value=False)

        tk.Checkbutton(self.form_frame, text="Air Conditioned", variable=self.has_ac_var).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Whiteboard", variable=self.has_whiteboard_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Screen", variable=self.has_screen_var).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Register button
        self.submit_btn = tk.Button(
            self.form_frame,
            text="Register Classroom",
            command=self.register_classroom
        )
        self.submit_btn.grid(row=6, column=0, columnspan=2, pady=20)

        # Grid weights
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=3)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("code", "capacity", "ac", "whiteboard", "screen")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)
        # Treeview selection binding
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Define headings
        self.tree.heading("code", text="Code")
        self.tree.heading("capacity", text="Capacity")
        self.tree.heading("ac", text="AC")
        self.tree.heading("whiteboard", text="Whiteboard")
        self.tree.heading("screen", text="Screen")

        # Column widths
        self.tree.column("code", width=100)
        self.tree.column("capacity", width=80)
        self.tree.column("ac", width=60)
        self.tree.column("whiteboard", width=100)
        self.tree.column("screen", width=80)

        self.tree.pack(fill="both", expand=True)

        # Load existing records
        self.load_classrooms()

        # Bind Enter key
        self.reg_window.bind("<Return>", self.register_classroom)

    def register_classroom(self, event=None):
        code = self.code_entry.get().strip()
        capacity = self.capacity_entry.get().strip()

        # Validate input
        if not code or not capacity.isdigit():
            messagebox.showerror("Error", "Valid classroom code and numeric capacity are required")
            return

        # Convert checkboxes
        has_ac = self.has_ac_var.get()
        has_whiteboard = self.has_whiteboard_var.get()
        has_screen = self.has_screen_var.get()

        if self._classrooms.add_classroom(code, int(capacity), has_ac, has_whiteboard, has_screen):
            messagebox.showinfo("Success", "Classroom registered successfully!")
            self.load_classrooms()
        else:
            messagebox.showerror("Error", "Failed to register classroom.")

    def load_classrooms(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        classrooms = self._classrooms.get_all_classrooms()
        for c in classrooms:
            self.tree.insert("", "end", values=(
                c["classroom_code"],
                c["capacity"],
                "Yes" if c["has_ac"] else "No",
                "Yes" if c["has_whiteboard"] else "No",
                "Yes" if c["has_screen"] else "No"
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        # Populate form fields
        self.code_entry.config(state="normal") 
        self.code_entry.delete(0, tk.END)
        self.code_entry.insert(0, values[0])
        self.code_entry.config(state="readonly") 
        self.capacity_entry.delete(0, tk.END)
        self.capacity_entry.insert(0, values[1])
        self.has_ac_var.set(values[2] == "Yes")
        self.has_whiteboard_var.set(values[3] == "Yes")
        self.has_screen_var.set(values[4] == "Yes")

        self.selected_code = values[0]  # Save for update

        # Change button text to "Update Classroom"
        self.submit_btn.config(text="Update Classroom", command=self.update_classroom)

    def update_classroom(self, event=None):
        code = self.code_entry.get().strip()
        capacity = self.capacity_entry.get().strip()
        has_ac = self.has_ac_var.get()
        has_whiteboard = self.has_whiteboard_var.get()
        has_screen = self.has_screen_var.get()

        if not code or not capacity.isdigit():
            messagebox.showerror("Error", "Valid classroom code and numeric capacity are required")
            return

        # Call your update method (implement this in your ClassRoom class)
        if self._classrooms.update_classroom(self.selected_code, int(capacity), has_ac, has_whiteboard, has_screen):
            messagebox.showinfo("Success", "Classroom updated successfully!")
            self.load_classrooms()
            self.clear_form()
            self.submit_btn.config(text="Register Classroom", command=self.register_classroom)
            self.selected_code = None
        else:
            messagebox.showerror("Error", "Failed to update classroom.")

    def clear_form(self):
        self.code_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.has_ac_var.set(False)
        self.has_whiteboard_var.set(True)
        self.has_screen_var.set(False)