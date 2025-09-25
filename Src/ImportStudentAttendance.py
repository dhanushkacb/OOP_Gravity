import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
from Src.db.Schema import Attendance
from Src.log.Logger import Logger
from Src.BaseRegistration import BaseRegistration

class ImportStudentAttendance(BaseRegistration):
    def __init__(self, entity_name="Mark Attendance", key_column="attendance_id"):
        super().__init__(model=Attendance(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(entity_name)
        self.reg_window.resizable(False, False)

        self.file_path = None
        self.preview_data = []

        # --- Buttons ---
        btn_frame = tk.Frame(self.reg_window, pady=10)
        btn_frame.pack(fill="x")

        self.select_btn = tk.Button(btn_frame, text="Select CSV File", command=self.select_file)
        self.select_btn.pack(side="left", padx=5)

        self.process_btn = tk.Button(btn_frame, text="Process Import", command=self.process_file, state="disabled")
        self.process_btn.pack(side="left", padx=5)

        # --- Table Preview ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("student_id", "class_id", "session_date", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=12)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center", stretch=True)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

    def select_file(self):
        try:
            self.file_path = filedialog.askopenfilename(
                title="Select CSV File",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
            )
            if not self.file_path:
                return

            # Clear preview
            for row in self.tree.get_children():
                self.tree.delete(row)

            # Read CSV
            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                self.preview_data = []
                for row in reader:
                    self.preview_data.append(row)
                    self.tree.insert("", "end", values=(
                        row.get("student_id", ""),
                        row.get("class_id", ""),
                        row.get("session_date", ""),
                        row.get("status", "")
                    ))

            if self.preview_data:
                self.process_btn.config(state="normal")
                messagebox.showinfo("File Loaded", f"Previewing {len(self.preview_data)} records from CSV.")
            else:
                self.process_btn.config(state="disabled")
                messagebox.showwarning("Empty File", "No records found in selected CSV.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Failed to read CSV file.\n{e}")

    def process_file(self):
        try:
            if not self.preview_data:
                messagebox.showwarning("No Data", "No records available to process.")
                return

            success_count = 0
            for row in self.preview_data:
                try:
                    self._model.insert(
                        row.get("student_id"),
                        row.get("class_id"),
                        row.get("session_date"),
                        row.get("status")
                    )
                    success_count += 1
                except Exception as e:
                    Logger.log(f"Failed to insert record: {row} -> {e}")

            messagebox.showinfo("Import Complete", f"Successfully imported {success_count} attendance records.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Import failed.\n{e}")
