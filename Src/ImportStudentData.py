import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import csv
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Students
from Src.log.Logger import Logger


class ImportStudentData(BaseRegistration):
    
    def __init__(self, entity_name="Import Students", key_column="student_id"):
        super().__init__(model=Students(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()

        self.reg_window.title(entity_name)
        self.reg_window.resizable(False, False)

        self.required_headers = ["name", "registration_year", "registration_month",
                                "contact_no", "discount_percent", "email", "stream"]
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
            with open(self.file_path, "r") as file:
                reader = csv.reader(file)
                headers = next(reader, None)
                headers = [h.strip().lower() for h in headers]
                required = [h.lower() for h in self.required_headers]

                if not headers or any(h not in headers for h in required):
                    messagebox.showerror("Error", f"CSV must include headers: {', '.join(self.required_headers)}")
                    return

                # Map rows like dictionary
                self.preview_data = []
                for row in reader:
                    mapped = dict(zip(headers, row))
                    self.preview_data.append(mapped)
                    self.tree.insert("", "end", values=tuple(mapped.get(h, "") for h in self.required_headers))

            if self.preview_data:
                self.process_btn.config(state="normal")
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
                    contact_no=row.get("contact_no")
                    existing = self._model.select_by_contact(contact_no)
                    if existing:
                        self._model.update(
                            existing["student_id"],
                            row.get("name"),
                            int(row.get("registration_year") or 0),
                            int(row.get("registration_month") or 0),
                            contact_no,
                            float(row.get("discount_percent", 0.0)) if row.get("discount_percent") else 0.0,
                            row.get("email"),
                            row.get("stream")
                        )
                    else:
                        self._model.insert(
                            row.get("name"),
                            int(row.get("registration_year") or 0),
                            int(row.get("registration_month") or 0),
                            contact_no,
                            float(row.get("discount_percent", 0.0)) if row.get("discount_percent") else 0.0,
                            row.get("email"),
                            row.get("stream")
                        )
                    success_count += 1
                except Exception as e:
                    row["error"] = str(e)
                    failed_records.append(row)
                    Logger.log(f"Failed to insert record: {row} -> {e}")

            if failed_records:
                failed_file = "failed_imports.csv"
                with open(failed_file, "w") as f:
                    writer = csv.writer(f)
                    headers = self.required_headers + ["error"]
                    writer.writerow(headers)
                    for row in failed_records:
                        values = [row.get(h, "") for h in self.required_headers]
                        values.append(row.get("error", "")) 
                        writer.writerow(values)

            messagebox.showinfo("Import Complete", f"Successfully imported {success_count} students.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Import failed.\n{e}")
