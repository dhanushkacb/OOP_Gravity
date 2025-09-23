import tkinter as tk
from tkinter import messagebox, ttk
from Src.BaseRegistration import BaseRegistration
from Src.config.Settings import Settings
from Src.db.Schema import Teachers
from Src.log.Logger import Logger


class TeacherRegistration(BaseRegistration):

    def __init__(self, entity_name="Teacher"):
        super().__init__(model=Teachers(), entity_name=entity_name, key_column="teacher_id")
        self.reg_window = tk.Toplevel()

        self.reg_window.title(f"{entity_name} Registration")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Name
        tk.Label(self.form_frame, text="Name:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Subject
        tk.Label(self.form_frame, text="Subject:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = tk.StringVar()
        self.subject_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.subject_entry,
            values=self._settings.get_subjects(),
            width=27,
            state="readonly"
        )
        self.subject_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Contact No
        tk.Label(self.form_frame, text="Contact No:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.contact_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.contact_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Email
        tk.Label(self.form_frame, text="Email:", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # --- Action Buttons ---
        self.submit_btn = tk.Button(self.form_frame, text="Save", command=self.save_record)
        self.delete_btn = tk.Button(self.form_frame, text="Delete", width=20, command=self.delete_record)
        self.clear_btn = tk.Button(self.form_frame, text="Clear", command=self.clear_form)

        self.submit_btn.grid(row=5, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=5, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=5, column=2, pady=20, padx=5, sticky="ew")

        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("teacher_id", "name", "subject", "contact_no", "email", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        # Scrollbar
        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        # Tree headings
        self.tree.heading("teacher_id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("contact_no", text="Contact No")
        self.tree.heading("email", text="Email")
        self.tree.heading("delete", text="Delete")

        for col in columns:
            self.tree.column(col, width=120, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_item_click)

        self.tree.pack(fill="both", expand=True)
        self.reg_window.bind("<Return>", self.save_record)

        self.load_records()

    # --- CRUD ---
    def save_record(self, event=None):
        try:
            name = self.name_entry.get().strip()
            subject = self.subject_entry.get().strip()
            contact = self.contact_entry.get().strip()
            email = self.email_entry.get().strip()

            if not name or not subject:
                messagebox.showerror("Error", "Name and subject are required.")
                return

            if self._model.insert(name, subject, contact, email):
                messagebox.showinfo("Success", "Teacher saved successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to save teacher.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not save {self.entity_name}. Please try again.")

    def load_records(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            teachers = self._model.select_all()
            for t in teachers:
                self.tree.insert("", "end", values=(
                    t["teacher_id"],
                    t["name"],
                    t["subject"],
                    t.get("contact_no", ""),
                    t.get("email", ""),
                    "🗑️ Delete"
                ))
            self.clear_form()
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not load {self.entity_name}s. Please try again.")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_key = values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.subject_entry.set(values[2])
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, values[3])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[4])

        self.submit_btn.config(text="Update", command=self.update_record)

    def update_record(self, event=None):
        try:
            name = self.name_entry.get().strip()
            subject = self.subject_entry.get().strip()
            contact = self.contact_entry.get().strip()
            email = self.email_entry.get().strip()

            if not name or not subject:
                messagebox.showerror("Error", "Name and subject are required.")
                return

            if self._model.update(self.selected_key, name, subject, contact, email):
                messagebox.showinfo("Success", "Teacher updated successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to update teacher.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not update {self.entity_name}. Please try again.")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.subject_entry.set("")
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.selected_key = None
        self.submit_btn.config(text="Save", command=self.save_record)
