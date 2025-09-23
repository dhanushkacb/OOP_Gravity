import tkinter as tk
from tkinter import messagebox, ttk
from Src.config.Settings import Settings
from Src.db.Schema import Teachers  # You should have a Teachers class similar to ClassRoom

class TeacherRegistration:
    def __init__(self):
        self.reg_window = tk.Toplevel()
        self._teachers = Teachers()
        self.selected_teacher_id = None

        self.reg_window.title("Teacher Registration")
        #self.reg_window.resizable(False, False)

        # Main frame
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(self.form_frame, text="Teacher Registration").grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Name
        tk.Label(self.form_frame, text="Name:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.name_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Subject
        tk.Label(self.form_frame, text="Subject:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.subject_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.subject_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Contact No
        tk.Label(self.form_frame, text="Contact No:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.contact_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.contact_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Email
        tk.Label(self.form_frame, text="Email:", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.email_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.email_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Register button
        self.submit_btn = tk.Button(
            self.form_frame,
            text="Register Teacher",
            command=self.register_teacher
        )
        self.submit_btn.grid(row=5, column=0, columnspan=2, pady=20)

        # Table Frame for displaying teachers
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("teacher_id", "name", "subject", "contact_no", "email")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)
        self.tree.heading("teacher_id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("subject", text="Subject")
        self.tree.heading("contact_no", text="Contact No")
        self.tree.heading("email", text="Email")
        for col in columns:
            self.tree.column(col, width=100)
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_teachers()

    def register_teacher(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not subject:
            messagebox.showerror("Error", "Name and subject are required.")
            return

        # Insert teacher (implement this in your Teachers class)
        if self._teachers.add_teacher(name, subject, contact, email):
            messagebox.showinfo("Success", "Teacher registered successfully!")
            self.load_teachers()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to register teacher.")

    def load_teachers(self):
        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Load teachers (implement get_all_teachers in your Teachers class)
        teachers = self._teachers.get_all_teachers()
        for t in teachers:
            self.tree.insert("", "end", values=(
            t["teacher_id"],
            t["name"],
            t["subject"],
            t["contact_no"],
            t["email"]
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_teacher_id = values[0]
        self.name_entry.delete(0, tk.END)
        self.name_entry.insert(0, values[1])
        self.subject_entry.delete(0, tk.END)
        self.subject_entry.insert(0, values[2])
        self.contact_entry.delete(0, tk.END)
        self.contact_entry.insert(0, values[3])
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, values[4])

        self.submit_btn.config(text="Update Teacher", command=self.update_teacher)

    def update_teacher(self):
        name = self.name_entry.get().strip()
        subject = self.subject_entry.get().strip()
        contact = self.contact_entry.get().strip()
        email = self.email_entry.get().strip()

        if not name or not subject:
            messagebox.showerror("Error", "Name and subject are required.")
            return

        # Update teacher (implement this in your Teachers class)
        if self._teachers.update_teacher(self.selected_teacher_id, name, subject, contact, email):
            messagebox.showinfo("Success", "Teacher updated successfully!")
            self.load_teachers()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update teacher.")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.subject_entry.delete(0, tk.END)
        self.contact_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.submit_btn.config(text="Register Teacher", command=self.register_teacher)
        self.selected_teacher_id = None