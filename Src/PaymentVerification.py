import tkinter as tk
from tkinter import messagebox, ttk
from Src.BaseRegistration import BaseRegistration
from Src.db.Schema import Payments, Students, Classes
from Src.log.Logger import Logger
from Src.config.Settings import Settings


class PaymentVerification(BaseRegistration):

    def __init__(self, entity_name="Payment Verification"):
        super().__init__(model=Payments(), entity_name=entity_name, key_column=None)
        self.reg_window = tk.Toplevel()
        self.reg_window.title(f"{entity_name} Screen")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="x", padx=10, pady=10)

        # Student
        tk.Label(self.form_frame, text="Student:", anchor="w").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.student_var = tk.StringVar()
        self.student_menu = ttk.Combobox(self.form_frame, textvariable=self.student_var, width=30, state="readonly")
        self.student_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Class
        tk.Label(self.form_frame, text="Class:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_menu = ttk.Combobox(self.form_frame, textvariable=self.class_var, width=30, state="readonly")
        self.class_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Month
        tk.Label(self.form_frame, text="Month:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.month_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.month_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Year
        tk.Label(self.form_frame, text="Year:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.year_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Verify Button
        self.verify_btn = tk.Button(self.form_frame, text="Verify Payment", command=self.verify_payment)
        self.verify_btn.grid(row=4, column=0, columnspan=2, pady=15, sticky="ew")

        # Result Label
        self.result_label = tk.Label(self.form_frame, text="", fg="blue", anchor="w")
        self.result_label.grid(row=5, column=0, columnspan=2, sticky="w", padx=5, pady=5)

        self.load_dropdowns()

    def load_dropdowns(self):
        try:
            students = Students().select_all()
            classes = Classes().select_class_details()

            self.student_map = {f"{s['student_id']} - {s['name']}": s["student_id"] for s in students}
            self.class_map = {f"{c['class_id']} - {c['subject']} - {c['category']} - {c['class_type']} - {c['teacher_name']}": c["class_id"] for c in classes}

            self.student_menu["values"] = list(self.student_map.keys())
            self.class_menu["values"] = list(self.class_map.keys())
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", "Could not load students or classes.")

    def verify_payment(self):
        try:
            student_id = self.student_map.get(self.student_var.get())
            class_id = self.class_map.get(self.class_var.get())
            month = self.month_entry.get().strip()
            year = self.year_entry.get().strip()

            if not student_id or not class_id or not month or not year:
                messagebox.showerror("Error", "All fields are required.")
                return

            if self._model.has_paid(student_id, class_id, year, month):
                payment = self._model.get_payment(student_id, class_id, year, month)
                msg = f"Payment FOUND!\nAmount: {payment['amount']}\nMethod: {payment['payment_method']}\nDate: {payment['paid_on']}"
                self.result_label.config(text=msg, fg="green")
            else:
                msg = "Payment NOT found for the selected month."
                self.result_label.config(text=msg, fg="red")

        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not verify payment.\n{e}")
