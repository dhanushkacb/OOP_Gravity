import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Payments, Teachers, Classes
from Src.log.Logger import Logger


class TeacherIncomeReport(BaseRegistration):
    def __init__(self, entity_name="Teacher Income Report"):
        super().__init__(model=Payments(), entity_name=entity_name, key_column="payment_id")
        self.reg_window = tk.Toplevel()
        self.reg_window.title(entity_name)
        self.reg_window.geometry("800x500")
        self.reg_window.resizable(True, True)

        # --- Filter Form ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=10)
        self.form_frame.pack(fill="x")

        # Month
        tk.Label(self.form_frame, text="Month:", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.month_entry = tk.Entry(self.form_frame, width=10)
        self.month_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Year
        tk.Label(self.form_frame, text="Year:", anchor="w").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(self.form_frame, width=10)
        self.year_entry.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Generate Button
        self.generate_btn = tk.Button(self.form_frame, text="Generate Report", command=self.generate_report)
        self.generate_btn.grid(row=0, column=4, padx=10, pady=5)

        # Export Button
        self.export_btn = tk.Button(self.form_frame, text="Export", command=self.export_report, state="disabled")
        self.export_btn.grid(row=0, column=5, padx=10, pady=5)

        # --- Table ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True)

        columns = ("teacher_id", "teacher_name", "month", "year", "total_income")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=20)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=150, anchor="center", stretch=True)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.report_data = []

    def generate_report(self):
        try:
            month = self.month_entry.get().strip()
            year = self.year_entry.get().strip()

            if not month or not year:
                messagebox.showerror("Error", "Month and Year are required.")
                return

            # Clear old data
            for row in self.tree.get_children():
                self.tree.delete(row)
            self.report_data = []

            # Fetch teachers
            teachers = Teachers().select_all()
            if not teachers:
                messagebox.showwarning("No Teachers", "No teachers found in the system.")
                return

            for t in teachers:
                teacher_id = t["teacher_id"]
                teacher_name = t["name"]

                # Get classes taught by teacher
                teacher_classes = Classes().select_by_teacher(teacher_id)
                total_income = 0.0

                for cls in teacher_classes:
                    class_id = cls["class_id"]
                    payments = Payments().select_by_class_and_month(class_id, year, month)
                    for p in payments:
                        total_income += float(p["amount"])

                row = {
                    "teacher_id": teacher_id,
                    "teacher_name": teacher_name,
                    "month": month,
                    "year": year,
                    "total_income": total_income
                }
                self.report_data.append(row)

                self.tree.insert("", "end", values=(
                    row["teacher_id"],
                    row["teacher_name"],
                    row["month"],
                    row["year"],
                    f"{row['total_income']:.2f}"
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
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not file_path:
                return

            header = (
                f"Teacher Income Report\n"
                f"Month: {self.month_entry.get()} | Year: {self.year_entry.get()}\n"
                + "-" * 60 + "\n"
                f"{'Teacher ID':<12}{'Teacher Name':<25}{'Month':<8}{'Year':<8}{'Income':<10}\n"
                + "-" * 60 + "\n"
            )

            lines = [
                f"{r['teacher_id']:<12}{r['teacher_name']:<25}{r['month']:<8}{r['year']:<8}{r['total_income']:<10.2f}"
                for r in self.report_data
            ]

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(header + "\n".join(lines) + "\n")

            messagebox.showinfo("Success", f"Report saved successfully!\nFile: {file_path}")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not export report.\n{e}")
