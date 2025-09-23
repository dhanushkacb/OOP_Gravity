import tkinter as tk
from tkinter import messagebox, filedialog
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Students
from Src.log.Logger import Logger


class StudentRegistrationReport(BaseRegistration):

    def __init__(self, entity_name="Student Report", key_column="student_id"):
        super().__init__(model=Students(), entity_name=entity_name, key_column=key_column)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(f"{entity_name} Generator")
        self.reg_window.resizable(False, False)

        # --- Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(
            self.form_frame,
            text="Generate Student Registration Report",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        # Generate button
        self.generate_btn = tk.Button(
            self.form_frame,
            text="Generate Report",
            width=25,
            command=self.generate_report
        )
        self.generate_btn.grid(row=1, column=0, columnspan=2, pady=10)

        # Close button
        self.close_btn = tk.Button(
            self.form_frame,
            text="Close",
            width=25,
            command=self.reg_window.destroy
        )
        self.close_btn.grid(row=2, column=0, columnspan=2, pady=5)

    def generate_report(self):
        """Generate student registration report into a text file"""
        try:
            students = self._model.select_all()
            if not students:
                messagebox.showinfo("Info", f"No {self.entity_name.lower()}s found.")
                return

            file_path = filedialog.asksaveasfilename(
                title="Save Report",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
            )
            if not file_path:
                return  # Cancelled

            with open(file_path, "w", encoding="utf-8") as f:
                f.write("=== Student Registration Report ===\n\n")
                for s in students:
                    line = (
                        f"ID: {s['student_id']} | "
                        f"Name: {s['name']} | "
                        f"Year: {s['registration_year']} | "
                        f"Month: {s['registration_month']} | "
                        f"Contact: {s.get('contact_no', '')} | "
                        f"Discount: {s.get('discount_percent', 0.00)} | "
                        f"Email: {s.get('email', '')} | "
                        f"Stream: {s.get('stream', '')}\n"
                    )
                    f.write(line)

            messagebox.showinfo("Success", f"{self.entity_name} generated successfully!\nSaved at: {file_path}")

        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not generate {self.entity_name}.\n{e}")
