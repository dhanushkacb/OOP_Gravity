import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import csv
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Payments, Students, Classes, Enrollments
from Src.log.Logger import Logger
from Src.config.Settings import Settings


class PaymentOutstandingReport(BaseRegistration):
    def __init__(self, entity_name="Payment Outstanding Report",key_column="payment_id"):
        super().__init__(model=Payments(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(entity_name)
        self.reg_window.geometry("1000x600")
        self.reg_window.resizable(True, True)

        # --- Filter Form ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=10)
        self.form_frame.pack(fill="x")

        # Class
        tk.Label(self.form_frame, text="Class:", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_menu = ttk.Combobox(self.form_frame, textvariable=self.class_var, width=40, state="readonly")
        self.class_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        classes = Classes().select_class_details()
        self.class_map = {
            f"{c['class_id']} - {c['subject']} - {c['category']} - {c['class_type']} - {c['teacher_name']}": c["class_id"]
            for c in classes
        }
        self.class_menu["values"] = list(self.class_map.keys())

        # Month
        tk.Label(self.form_frame, text="Month:", anchor="w").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.month_entry = tk.Entry(self.form_frame, width=10)
        self.month_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Year
        tk.Label(self.form_frame, text="Year:", anchor="w").grid(row=0, column=4, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(self.form_frame, width=10)
        self.year_entry.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # Generate Button
        self.generate_btn = tk.Button(self.form_frame, text="Generate Report", command=self.generate_report)
        self.generate_btn.grid(row=0, column=6, padx=10, pady=5)

        # Export Button
        self.export_btn = tk.Button(self.form_frame, text="Export to CSV", command=self.export_report, state="disabled")
        self.export_btn.grid(row=0, column=7, padx=10, pady=5)

        # --- Table ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("student_id", "student_name", "class_id", "month", "year", "status")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=140, anchor="center", stretch=True)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.report_data = []

    def generate_report(self):
        try:
            class_text = self.class_var.get().strip()
            class_id = self.class_map.get(class_text)
            month = self.month_entry.get().strip()
            year = self.year_entry.get().strip()

            if not class_id or not month or not year:
                messagebox.showerror("Error", "Class, Month, and Year are required.")
                return

            # Clear old data
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.report_data = []

            # Enrolled students
            enrolled = Enrollments().select_by_class(class_id)
            if not enrolled:
                messagebox.showwarning("No Students", "No students enrolled for this class.")
                return

            for e in enrolled:
                student = Students().select_by_id(e["student_id"])
                if not student:
                    continue

                payment = Payments().get_payment(student["student_id"], class_id, year, month)
                status = "PAID" if payment else "OUTSTANDING"

                row = {
                    "student_id": student["student_id"],
                    "student_name": student["name"],
                    "class_id": class_id,
                    "month": month,
                    "year": year,
                    "status": status
                }
                self.report_data.append(row)
                self.tree.insert("", "end", values=(
                    row["student_id"],
                    row["student_name"],
                    row["class_id"],
                    row["month"],
                    row["year"],
                    row["status"]
                ))

            self.export_btn.config(state="normal")

        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not generate report.\n{e}")

    def export_report(self):
        try:
            if not self.report_data:
                messagebox.showwarning("No Data", "No report data to export.")
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Report",
                defaultextension=".csv",
                filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
            )
            if not file_path:
                return

            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(["student_id", "student_name", "class_id", "month", "year", "status"])
                for row in self.report_data:
                    writer.writerow([row["student_id"], row["student_name"], row["class_id"],
                                     row["month"], row["year"], row["status"]])

            messagebox.showinfo("Success", f"Report exported successfully!\nFile: {file_path}")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not export report.\n{e}")
