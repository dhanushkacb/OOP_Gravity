import tkinter as tk
from tkinter import messagebox,ttk
from Src.BaseRegistration import BaseRegistration
from Src.config.Settings import Settings
from Src.db.Schema import ClassRoom
from Src.log.Logger import Logger

class ClassroomRegistration(BaseRegistration):

    def __init__(self, entity_name="Classroom",key_column="classroom_code"):
        super().__init__(model=ClassRoom(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()

        self.reg_window.title(f"{entity_name} Registration")
        self.reg_window.resizable(False, False)

        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Fields
        tk.Label(self.form_frame, text="Classroom Code:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.code_entry.focus_set()

        tk.Label(self.form_frame, text="Capacity:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.capacity_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        self.has_ac_var = tk.BooleanVar(value=False)
        self.has_whiteboard_var = tk.BooleanVar(value=True)
        self.has_screen_var = tk.BooleanVar(value=False)

        tk.Checkbutton(self.form_frame, text="Air Conditioned", variable=self.has_ac_var).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Whiteboard", variable=self.has_whiteboard_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Screen", variable=self.has_screen_var).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Actions
        self.submit_btn = tk.Button(
            self.form_frame,
            text="Save",
            width=15,
            command=self.save_record
        )
        self.delete_btn = tk.Button(
            self.form_frame,
            text="Delete",
            width=15,
            command=self.delete_record
        )
        self.clear_btn = tk.Button(
            self.form_frame,
            text="Clear",
            width=15,
            command=self.clear_form
        )
        self.submit_btn.grid(row=6, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=6, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=6, column=2, pady=20, padx=5, sticky="ew")
        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("code", "capacity", "ac", "whiteboard", "screen","delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        # Attach scrollbar
        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.tree.heading("code", text="Code")
        self.tree.heading("capacity", text="Capacity")
        self.tree.heading("ac", text="AC")
        self.tree.heading("whiteboard", text="Whiteboard")
        self.tree.heading("screen", text="Screen")
        self.tree.heading("delete", text="Delete")

        for col in columns:
            self.tree.column(col, width=100, anchor="center", stretch=True)
        self.tree.bind("<Button-1>", self.on_tree_item_click)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.pack(fill="both", expand=True)
        self.reg_window.bind("<Return>", self.save_record)

        self.load_records()

    def save_record(self, event=None):
        try:
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

            if self._model.insert(code, int(capacity), has_ac, has_whiteboard, has_screen):
                messagebox.showinfo("Success", "Record successfully saved!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to register classroom.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Save {self.entity_name}. Please try again.")

    def load_records(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            classrooms = self._model.select_all()
            for c in classrooms:
                self.tree.insert("", "end", values=(
                    c["classroom_code"],
                    c["capacity"],
                    "Yes" if c["has_ac"] else "No",
                    "Yes" if c["has_whiteboard"] else "No",
                    "Yes" if c["has_screen"] else "No",
                    "🗑️ Delete"
                ))
            self.clear_form()
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not select all {self.entity_name}. Please try again.")

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
        self.selected_key = values[0]
        self.submit_btn.config(text="Update", command=self.update_record)

    def update_record(self, event=None):
        try:
            code = self.code_entry.get().strip()
            capacity = self.capacity_entry.get().strip()
            has_ac = self.has_ac_var.get()
            has_whiteboard = self.has_whiteboard_var.get()
            has_screen = self.has_screen_var.get()

            if not code or not capacity.isdigit():
                messagebox.showerror("Error", "Valid classroom code and numeric capacity are required")
                return

            if self._model.update(self.selected_key, int(capacity), has_ac, has_whiteboard, has_screen):
                messagebox.showinfo("Success", "Record updated successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to update record.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not update {self.entity_name}. Please try again.")
        
    def clear_form(self):
        self.code_entry.config(state="normal")
        self.code_entry.delete(0, tk.END)
        self.capacity_entry.delete(0, tk.END)
        self.has_ac_var.set(False)
        self.has_whiteboard_var.set(True)
        self.has_screen_var.set(False)
        self.selected_key = None
        self.submit_btn.config(text="Save", command=self.save_record)