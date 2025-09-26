import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Payments
from Src.log.Logger import Logger


class ImportStudentPayments(BaseRegistration):
    def __init__(self, entity_name="Import Payments", key_column="payment_id"):
        super().__init__(model=Payments(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(entity_name)
        self.reg_window.resizable(True, True)

        self.required_headers = ["class_id", "student_id", "year", "month", "amount", "method", "remarks"]
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

        columns = tuple(self.required_headers)
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=15)

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

            with open(self.file_path, "r", newline="", encoding="utf-8") as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                headers = [h.strip().lower() for h in headers]

                required = [h.lower() for h in self.required_headers]
                if not headers or any(h not in headers for h in required):
                    messagebox.showerror("Error", f"CSV must include headers: {', '.join(self.required_headers)}")
                    return

                self.preview_data = []
                for row in reader:
                    mapped = dict(zip([h.lower() for h in headers], row))
                    self.preview_data.append(mapped)
                    self.tree.insert("", "end", values=tuple(mapped.get(h, "") for h in self.required_headers))

            if self.preview_data:
                self.process_btn.config(state="normal")
                messagebox.showinfo("File Loaded", f"Previewing {len(self.preview_data)} records.")
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
            failed_records = []

            for row in self.preview_data:
                try:
                    self._model.insert(
                        student_id=row.get("student_id"),
                        class_id=row.get("class_id"),
                        month=row.get("month"),
                        year=row.get("year"),
                        amount=row.get("amount"),
                        payment_method=row.get("method"),
                        remarks=row.get("remarks"),
                        discount_applied=0.0  # you can add discount column later if needed
                    )
                    success_count += 1
                except Exception as e:
                    row["error"] = str(e)
                    failed_records.append(row)
                    Logger.log(f"Failed to insert payment: {row} -> {e}")

            # Save failed records into a CSV file
            if failed_records:
                failed_file = f"{self.entity_name}_failed_records.csv"
                with open(failed_file, "w", encoding="utf-8", newline="") as f:
                    writer = csv.writer(f)
                    headers = self.required_headers + ["error"]
                    writer.writerow(headers)
                    for row in failed_records:
                        values = [row.get(h, "") for h in self.required_headers]
                        values.append(row.get("error", ""))
                        writer.writerow(values)

            messagebox.showinfo(
                "Import Complete",
                f"Successfully imported {success_count}, failed {len(failed_records)} payments."
            )
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Import failed.\n{e}")
