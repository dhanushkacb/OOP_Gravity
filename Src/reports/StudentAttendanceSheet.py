import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Classes, Students, Enrollments, Teachers
from Src.log.Logger import Logger


class StudentAttendanceSheet(BaseRegistration):
    def __init__(self, entity_name="Attendance Sheet", key_column="class_id"):
        super().__init__(model=Classes(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(f"{entity_name} Generator")
        self.reg_window.geometry("1000x600")
        self.reg_window.resizable(True, True)

        # --- Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="x")

        # Class ID input
        tk.Label(self.form_frame, text="Class ID:", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.class_id_var = tk.StringVar()
        self.class_id_combo = ttk.Combobox(self.form_frame, textvariable=self.class_id_var, state="readonly", width=30)
        self.class_id_combo.grid(row=0, column=1, padx=5, pady=5)

        classes = self._model.select_class_details()
        self.class_map = {f"{c['class_id']} - {c['subject']} - {c['category']} - {c['class_type']} - {c['teacher_name']}": c["class_id"] for c in classes}
        self.class_id_combo["values"] = list(self.class_map.keys())
        
        # Date input
        tk.Label(self.form_frame, text="Date (YYYY-MM-DD):", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.date_entry = tk.Entry(self.form_frame, width=15)
        self.date_entry.insert(0, datetime.today().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        self.generate_btn = tk.Button(self.form_frame, text="Generate Sheet", width=20, command=self.generate_sheet)
        self.generate_btn.grid(row=1, column=2, padx=5)

        self.export_btn = tk.Button(self.form_frame, text="Export to File", width=20, command=self.export_sheet, state="disabled")
        self.export_btn.grid(row=1, column=3, padx=5)

        # Table Frame
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("class_id", "subject", "student_id", "student_name", "date", "status","tute")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center", stretch=True)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.sheet_data = []

    def generate_sheet(self):
        try:
            selected_text = self.class_id_combo.get().strip()
            class_id = self.class_map.get(selected_text)
            date_str = self.date_entry.get().strip()

            if not class_id or not date_str:
                messagebox.showerror("Error", "Class ID and Date are required.")
                return

            try:
                selected_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
                return

            # Clear old data
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.sheet_data = []

            # --- Class info ---
            class_info = self._model.select_by_id(class_id)
            if not class_info:
                messagebox.showerror("Error", f"No class found with ID {class_id}")
                return

            subject = class_info.get("subject", "")
            teacher_id = class_info.get("teacher_id")

            teacher_name = ""
            if teacher_id:
                teacher = Teachers().select_by_id(teacher_id)  
                if teacher:
                    teacher_name = teacher.get("name", "")

            # --- Enrolled students ---
            enrolled = Enrollments().select_by_class(class_id)
            if not enrolled:
                messagebox.showwarning("No Students", "No students enrolled for this class.")
                return

            for e in enrolled:
                student = Students().select_by_id(e["student_id"])
                if student:
                    row = {
                        "class_id": class_id,
                        "subject": subject,
                        "teacher": teacher_name,
                        "student_id": student["student_id"],
                        "student_name": student["name"],
                        "date": str(selected_date),
                        "status": "[ ]",
                        "tute": "[ ]"
                    }
                    self.sheet_data.append(row)
                    self.tree.insert("", "end", values=(row["class_id"], row["subject"], 
                                                        row["student_id"], row["student_name"], 
                                                        row["date"], row["status"],row["tute"]))

            self.export_btn.config(state="normal")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not generate attendance sheet.\n{e}")


    def export_sheet(self):
        try:
            if not self.sheet_data:
                messagebox.showwarning("No Data", "No attendance sheet to export.")
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Attendance Sheet",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not file_path:
                return

            # Use first row for class metadata
            first = self.sheet_data[0]
            header = (
                f"Class: {first['class_id']}\n"
                f"Subject: {first['subject']}\n"
                f"Date: {first['date']}\n"
                f"Teacher: {first['teacher']}\n"
                + "-" * 45 + "\n"
                "Student Id\t\t| Student Name\t\t| Status\n"
                + "-" * 45 + "\n"
            )

            lines = [
                f"{s['student_id']}\t\t\t\t|{s['student_name']}\t\t\t\t| {s['status']}"
                for s in self.sheet_data
            ]

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(header + "\n".join(lines) + "\n")

            messagebox.showinfo("Success", f"Attendance sheet saved successfully!\nFile: {file_path}")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not export attendance sheet.\n{e}")


