import tkinter as tk
from tkinter import messagebox, ttk
from Src.BaseRegistration import BaseRegistration
from Src.config.Settings import Settings
from Src.db.Schema import ClassRoom, Classes
from Src.log.Logger import Logger


class ClassSchedule(BaseRegistration):
    def __init__(self, entity_name="Class Schedule",key_column="class_id"):
        super().__init__(model=Classes(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()

        self.reg_window.title(f"{entity_name} Registration")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Teacher ID
        tk.Label(self.form_frame, text="Teacher:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.teacher_var = tk.StringVar()
        teacher_records = self.get_teachers()
        self.teacher_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.teacher_var,
            values=[f"{t['teacher_id']} - {t['name']}" for t in teacher_records],
            width=27,
            state="readonly"
        )
        self.teacher_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.teacher_menu.bind("<<ComboboxSelected>>", self.on_teacher_selected)

        # Subject
        tk.Label(self.form_frame, text="Subject:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH, state="readonly")
        self.subject_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Class Type
        tk.Label(self.form_frame, text="Class Type:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.class_type_var = tk.StringVar()
        self.class_type_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.class_type_var,
            values=self._settings.get_class_type(),
            width=27,
            state="readonly"
        )
        self.class_type_menu.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Category
        tk.Label(self.form_frame, text="Category:", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.category_var = tk.StringVar()
        self.category_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.category_var,
            values=self._settings.get_class_category(),
            width=27,
            state="readonly"
        )
        self.category_menu.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Time Slot
        tk.Label(self.form_frame, text="Time Slot:", anchor="w").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.timeslot_var = tk.StringVar()
        self.timeslot_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.timeslot_var,
            values=self._settings.get_time_slot(),
            width=27,
            state="readonly"
        )
        self.timeslot_menu.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Classroom
        tk.Label(self.form_frame, text="Classroom:", anchor="w").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.classroom_var = tk.StringVar()
        classroom_records = self.get_classrooms()
        self.classroom_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.classroom_var,
            values=[c['classroom_code'] for c in classroom_records],
            width=27,
            state="readonly"
        )
        self.classroom_menu.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # --- Action Buttons ---
        self.submit_btn = tk.Button(self.form_frame, text="Save", command=self.save_record)
        self.delete_btn = tk.Button(self.form_frame, text="Delete", width=20, command=self.delete_record)
        self.clear_btn = tk.Button(self.form_frame, text="Clear", command=self.clear_form)

        self.submit_btn.grid(row=7, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=7, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=7, column=2, pady=20, padx=5, sticky="ew")

        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("class_id", "teacher_id", "subject", "class_type", "category", "time_slot", "classroom", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        # Scrollbar
        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_item_click)
        self.tree.pack(fill="both", expand=True)

        self.reg_window.bind("<Return>", self.save_record)
        self.load_records()

    # --- CRUD ---
    def save_record(self, event=None):
        try:
            teacher_text = self.teacher_var.get().strip()
            teacher_id = teacher_text.split(" - ")[0] if teacher_text else None
            subject = self.subject_entry.get().strip()
            class_type = self.class_type_var.get().strip()
            category = self.category_var.get().strip()
            timeslot = self.timeslot_var.get().strip()
            classroom = self.classroom_var.get().strip()

            if not teacher_id or not subject:
                messagebox.showerror("Error", "Teacher and Subject are required")
                return

            if self._model.insert(teacher_id, subject, class_type, category, timeslot, classroom):
                messagebox.showinfo("Success", "Class Schedule saved successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to save class schedule.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Save {self.entity_name}")


    def load_records(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            classes = self._model.select_all()
            for c in classes:
                self.tree.insert("", "end", values=(
                    c["class_id"],
                    c["teacher_id"],
                    c["subject"],
                    c["class_type"],
                    c["category"],
                    c["time_slot"],
                    c["classroom"],
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

        # teacher_id (reset combobox)
        teacher_id = values[1]
        teachers = [f"{t['teacher_id']} - {t['name']}" for t in self.get_teachers()]
        match = next((t for t in teachers if t.startswith(str(teacher_id))), None)
        if match:
            self.teacher_var.set(match)

        # subject
        self.subject_entry.config(state="normal")
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, values[2])
        self.subject_entry.config(state="readonly")

        # others
        self.class_type_var.set(values[3])
        self.category_var.set(values[4])
        self.timeslot_var.set(values[5])
        self.classroom_var.set(values[6])

        self.submit_btn.config(text="Update", command=self.update_record)


    def update_record(self, event=None):
        try:
            teacher_text = self.teacher_var.get().strip()
            teacher_id = teacher_text.split(" - ")[0] if teacher_text else None
            subject = self.subject_entry.get().strip()
            class_type = self.class_type_var.get().strip()
            category = self.category_var.get().strip()
            timeslot = self.timeslot_var.get().strip()
            classroom = self.classroom_var.get().strip()

            if not teacher_id or not subject:
                messagebox.showerror("Error", "Teacher and Subject are required")
                return

            if self._model.update(self.selected_key, teacher_id, subject, class_type, category, timeslot, classroom):
                messagebox.showinfo("Success", "Class Schedule updated successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to update class schedule.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Update {self.entity_name}")


    def clear_form(self):
        self.teacher_var.set("")
        self.subject_entry.config(state="normal")
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.config(state="readonly")
        self.class_type_var.set("")
        self.category_var.set("")
        self.timeslot_var.set("")
        self.classroom_var.set("")
        self.selected_key = None
        self.submit_btn.config(text="Save", command=self.save_record)


    def get_teachers(self):
        try:
            from Src.db.Schema import Teachers
            return Teachers().select_all()
        except Exception as e:
            Logger.log(e)
            return []

    def get_classrooms(self):
        try:
            return ClassRoom().select_all()
        except Exception as e:
            Logger.log(e)
            return []

    def on_teacher_selected(self, event):
        teacher_text = self.teacher_var.get()
        teacher_id = teacher_text.split(" - ")[0] if teacher_text else None
        if teacher_id:
            # lookup teacher’s subject
            from Src.db.Schema import Teachers
            teacher = next((t for t in Teachers().select_all() if str(t['teacher_id']) == str(teacher_id)), None)
            if teacher:
                self.subject_entry.config(state="normal")
                self.subject_entry.delete(0, tk.END)
                self.subject_entry.insert(0, teacher["subject"])
                self.subject_entry.config(state="readonly")
