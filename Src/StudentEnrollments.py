import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Enrollments, Students, Classes
from Src.config.Settings import Settings
from Src.log.Logger import Logger


class StudentEnrollments(BaseRegistration):

    def __init__(self, entity_name="Enrollment"):
        super().__init__(model=Enrollments(), entity_name=entity_name, key_column="enrollment_id")
        self.reg_window = tk.Toplevel()

        self.reg_window.title(f"{entity_name} Management")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Student Dropdown
        tk.Label(self.form_frame, text="Student:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.student_var = tk.StringVar()
        self.student_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.student_var,
            width=30,
            state="readonly"
        )
        self.student_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Class Dropdown
        tk.Label(self.form_frame, text="Class:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.class_var,
            width=30,
            state="readonly"
        )
        self.class_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Enrollment Date
        tk.Label(self.form_frame, text="Enrollment Date:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.date_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        # --- Action Buttons ---
        self.submit_btn = tk.Button(self.form_frame, text="Save", command=self.save_record)
        self.delete_btn = tk.Button(self.form_frame, text="Delete", command=self.delete_record)
        self.clear_btn = tk.Button(self.form_frame, text="Clear", command=self.clear_form)

        self.submit_btn.grid(row=4, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=4, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=4, column=2, pady=20, padx=5, sticky="ew")

        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("enrollment_id", "student", "class", "date", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=140, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_item_click)
        self.tree.pack(fill="both", expand=True)

        self.reg_window.bind("<Return>", self.save_record)

        # Load dropdowns and records
        self.load_dropdowns()
        self.load_records()

    # Load dropdown values from Students and Classes
    def load_dropdowns(self):
        try:
            students = Students().select_all()
            classes = Classes().select_class_details()

            self.student_map = {f"{s['student_id']} - {s['name']}": s["student_id"] for s in students}
            self.class_map = {f"{c['class_id']} - {c['subject']} - {c['category']} - {c['class_type']} - {c['teacher_name']}": c["class_id"] for c in classes}

            self.student_menu["values"] = list(self.student_map.keys())
            self.class_menu["values"] = list(self.class_map.keys())
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", "Could not load students or classes.")

    # --- CRUD ---
    def save_record(self, event=None):
        try:
            student_text = self.student_var.get()
            class_text = self.class_var.get()
            enrolled_date = self.date_entry.get().strip()

            if not student_text or not class_text:
                messagebox.showerror("Error", "Student and Class are required")
                return

            student_id = self.student_map.get(student_text)
            class_id = self.class_map.get(class_text)

            if self._model.insert(student_id, class_id, enrolled_date):
                messagebox.showinfo("Success", "Enrollment saved successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to save enrollment.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Save {self.entity_name}")

    def load_records(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            enrollments = self._model.select_all()
            for e in enrollments:
                student_text = f"{e['student_id']}"  # could extend with JOIN later
                class_text = f"{e['class_id']}"
                self.tree.insert("", "end", values=(
                    e["enrollment_id"],
                    student_text,
                    class_text,
                    e["enrollment_date"],
                    "🗑️ Delete"
                ))
            self.clear_form()
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Load {self.entity_name}")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_key = values[0]

        # student_id (reset combobox)
        student_id = values[1]
        students = [f"{s['student_id']} - {s['name']}" for s in self.get_students()]
        match = next((t for t in students if t.startswith(str(student_id))), None)
        if match:
            self.student_var.set(match)

        # class_id (reset combobox)
        class_id = values[2]
        classes = [f"{c['class_id']} - {c['subject']} - {c['category']} - {c['class_type']} - {c['teacher_name']}" for c in self.get_classes()]
        match = next((t for t in classes if t.startswith(str(class_id))), None)
        if match:
            self.class_var.set(match)

        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, values[3])

        self.submit_btn.config(text="Update", command=self.update_record)

    def update_record(self, event=None):
        try:
            student_text = self.student_var.get()
            class_text = self.class_var.get()
            enrolled_date = self.date_entry.get().strip()

            if not student_text or not class_text:
                messagebox.showerror("Error", "Student and Class are required")
                return

            student_id = self.student_map.get(student_text)
            class_id = self.class_map.get(class_text)

            if self._model.update(self.selected_key, student_id, class_id, enrolled_date):
                messagebox.showinfo("Success", "Enrollment updated successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to update enrollment.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Update {self.entity_name}")

    def clear_form(self):
        self.student_var.set("")
        self.class_var.set("")
        self.date_entry.delete(0, tk.END)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.selected_key = None
        self.submit_btn.config(text="Save", command=self.save_record)

    def get_students(self):
        try:
            from Src.db.Schema import Teachers
            return Students().select_all()
        except Exception as e:
            Logger.log(e)
            return []

    def get_classes(self):
        try:
            return Classes().select_class_details()
        except Exception as e:
            Logger.log(e)
            return []
