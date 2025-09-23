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
        self.reg_window.geometry("700x500")
        self.reg_window.resizable(True, True)

        # --- Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(
            self.form_frame,
            text="Student Registration Report",
            font=("Arial", 14, "bold")
        ).pack(pady=(0, 10))

        # Preview text area with scrollbar
        self.text_area = tk.Text(self.form_frame, wrap="none", height=20, width=80)
        self.text_area.pack(fill="both", expand=True, padx=5, pady=5)

        scrollbar_y = tk.Scrollbar(self.form_frame, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        # Buttons
        btn_frame = tk.Frame(self.form_frame)
        btn_frame.pack(fill="x", pady=10)

        self.preview_btn = tk.Button(btn_frame, text="Preview Data", width=20, command=self.preview_report)
        self.preview_btn.pack(side="left", padx=5)

        self.generate_btn = tk.Button(btn_frame, text="Save to File", width=20, command=self.generate_report)
        self.generate_btn.pack(side="left", padx=5)

        self.close_btn = tk.Button(btn_frame, text="Close", width=20, command=self.reg_window.destroy)
        self.close_btn.pack(side="right", padx=5)

    def _generate_text_content(self):
        """Helper: build the report text (used for preview and saving)."""
        students = self._model.select_all()

        if not students:
            return "No students found.\n"

        header = (
            "ID | Name | Year | Month | Contact | Discount | Email | Stream\n"
            + "-" * 80 + "\n"
        )

        lines = []
        for s in students:
            line = (
                f"{s['student_id']} | "
                f"{s['name']} | "
                f"{s['registration_year']} | "
                f"{s['registration_month']} | "
                f"{s.get('contact_no', '')} | "
                f"{s.get('discount_percent', 0.00)} | "
                f"{s.get('email', '')} | "
                f"{s.get('stream', '')}"
            )
            lines.append(line)

        return header + "\n".join(lines) + "\n"

    def preview_report(self):
        """Load student records into the preview text area"""
        try:
            text_content = self._generate_text_content()
            self.text_area.delete("1.0", tk.END)
            self.text_area.insert(tk.END, text_content)
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not preview {self.entity_name}.\n{e}")

    def generate_report(self):
        """Save student registration report to a text file"""
        try:
            text_content = self._generate_text_content()
            if "No students found" in text_content:
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
                f.write(text_content)

            messagebox.showinfo("Success", f"{self.entity_name} saved successfully!\nFile: {file_path}")

        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not generate {self.entity_name}.\n{e}")
