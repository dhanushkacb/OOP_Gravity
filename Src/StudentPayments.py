import tkinter as tk
from tkinter import messagebox, ttk
from Src.BaseRegistration import BaseRegistration
from Src.DiscountHandler import DiscountHandler
from Src.db.Schema import Payments, Students, Classes
from Src.config.Settings import Settings
from Src.log.Logger import Logger


class StudentPayments(BaseRegistration):

    def __init__(self, entity_name="Payment"):
        super().__init__(model=Payments(), entity_name=entity_name, key_column="payment_id")
        self.reg_window = tk.Toplevel()
        self.student_discount = 0.00

        self.reg_window.title(f"{entity_name} Management")
        self.reg_window.resizable(False, False)

        # --- Form Frame ---
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Student
        tk.Label(self.form_frame, text="Student:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.student_var = tk.StringVar()
        self.student_menu = ttk.Combobox(self.form_frame, textvariable=self.student_var, width=30, state="readonly")
        self.student_menu.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

        # Class
        tk.Label(self.form_frame, text="Class:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.class_var = tk.StringVar()
        self.class_menu = ttk.Combobox(self.form_frame, textvariable=self.class_var, width=30, state="readonly")
        self.class_menu.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Month
        tk.Label(self.form_frame, text="Month:", anchor="w").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.month_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.month_entry.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

        # Year
        tk.Label(self.form_frame, text="Year:", anchor="w").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.year_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.year_entry.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

        # Class Fee (readonly)
        tk.Label(self.form_frame, text="Class Fee:", anchor="w").grid(row=5, column=0, sticky="w", padx=5, pady=5)
        self.class_fee_var = tk.StringVar()
        self.class_fee_entry = tk.Entry(self.form_frame, textvariable=self.class_fee_var,
                                        width=Settings.ENTRY_WIDTH, state="readonly")
        self.class_fee_entry.grid(row=5, column=1, padx=5, pady=5, sticky="ew")

        # Discounted Fee (readonly)
        tk.Label(self.form_frame, text="Discounted Fee:", anchor="w").grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.discounted_fee_var = tk.StringVar()
        self.discounted_fee_entry = tk.Entry(self.form_frame, textvariable=self.discounted_fee_var,
                                             width=Settings.ENTRY_WIDTH, state="readonly")
        self.discounted_fee_entry.grid(row=6, column=1, padx=5, pady=5, sticky="ew")

        # Final Amount (editable)
        tk.Label(self.form_frame, text="Amount to Pay:", anchor="w").grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.amount_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.amount_entry.grid(row=7, column=1, padx=5, pady=5, sticky="ew")

        # Payment Method
        tk.Label(self.form_frame, text="Payment Method:", anchor="w").grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.payment_method_var = tk.StringVar()
        self.payment_method_menu = ttk.Combobox(
            self.form_frame,
            textvariable=self.payment_method_var,
            values=self._settings.get_payment_methods() if hasattr(self._settings, "get_payment_methods")
            else ["Cash", "Card", "Online"],
            width=27,
            state="readonly"
        )
        self.payment_method_menu.grid(row=8, column=1, padx=5, pady=5, sticky="ew")

        # Remarks
        tk.Label(self.form_frame, text="Remarks:", anchor="w").grid(row=9, column=0, sticky="w", padx=5, pady=5)
        self.remarks_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.remarks_entry.grid(row=9, column=1, padx=5, pady=5, sticky="ew")

        # --- Action Buttons ---
        self.submit_btn = tk.Button(self.form_frame, text="Save", command=self.save_record)
        self.delete_btn = tk.Button(self.form_frame, text="Delete", command=self.delete_record)
        self.clear_btn = tk.Button(self.form_frame, text="Clear", command=self.clear_form)

        self.submit_btn.grid(row=10, column=0, pady=20, padx=5, sticky="ew")
        self.delete_btn.grid(row=10, column=1, pady=20, padx=5, sticky="ew")
        self.clear_btn.grid(row=10, column=2, pady=20, padx=5, sticky="ew")

        for col in range(3):
            self.form_frame.columnconfigure(col, weight=1, minsize=100)

        # --- Table Frame ---
        self.table_frame = tk.Frame(self.reg_window, padx=10, pady=10)
        self.table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("payment_id", "student", "class", "month", "year", "amount", "discount_applied", "method", "remarks", "delete")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=6)

        scrollbar_y = tk.Scrollbar(self.table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120, anchor="center", stretch=True)

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Button-1>", self.on_tree_item_click)

        # auto fee calc on student/class change
        self.student_menu.bind("<<ComboboxSelected>>", self.update_fee_display)
        self.class_menu.bind("<<ComboboxSelected>>", self.update_fee_display)

        self.reg_window.bind("<Return>", self.save_record)

        self.load_dropdowns()
        self.load_records()

    # -----------------------------
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

    def save_record(self, event=None):
        try:
            student_id = self.student_map.get(self.student_var.get())
            class_id = self.class_map.get(self.class_var.get())
            month = self.month_entry.get().strip()
            year = self.year_entry.get().strip()
            amount = self.amount_entry.get().strip()
            method = self.payment_method_var.get()
            remarks = self.remarks_entry.get().strip()
            discount = self.student_discount

            if not student_id or not class_id or not amount or not method:
                messagebox.showerror("Error", "Student, Class, Amount, and Payment Method are required")
                return

            if self._model.insert(student_id, class_id, month, year, amount, method, discount, remarks):
                messagebox.showinfo("Success", "Payment saved successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to save payment.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Save {self.entity_name}")

    def load_records(self):
        try:
            for row in self.tree.get_children():
                self.tree.delete(row)

            payments = self._model.select_all()
            for p in payments:
                self.tree.insert("", "end", values=(
                    p["payment_id"],
                    p["student_id"],
                    p["class_id"],
                    p["month"],
                    p["year"],
                    p["amount"],
                    p["discount_applied"],
                    p["payment_method"],
                    p.get("remarks", ""),
                    "🗑️ Delete"
                ))
            self.clear_form()
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Load {self.entity_name}")

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]

        self.selected_key = values[0]

        student_id = values[1]
        student_text = next((k for k, v in self.student_map.items() if v == student_id), "")
        self.student_var.set(student_text)

        class_id = values[2]
        class_text = next((k for k, v in self.class_map.items() if v == class_id), "")
        self.class_var.set(class_text)

        # --- Other fields ---
        self.month_entry.delete(0, tk.END)
        self.month_entry.insert(0, values[3])
        self.year_entry.delete(0, tk.END)
        self.year_entry.insert(0, values[4])
        self.amount_entry.delete(0, tk.END)
        self.amount_entry.insert(0, values[5])
        self.payment_method_var.set(values[7])
        self.remarks_entry.delete(0, tk.END)
        self.remarks_entry.insert(0, values[8])

        self.update_fee_display()
        self.submit_btn.config(text="Update", command=self.update_record)

    def update_record(self, event=None):
        try:
            student_id = self.student_map.get(self.student_var.get())
            class_id = self.class_map.get(self.class_var.get())
            month = self.month_entry.get().strip()
            year = self.year_entry.get().strip()
            amount = self.amount_entry.get().strip()
            method = self.payment_method_var.get()
            remarks = self.remarks_entry.get().strip()
            discount = self.student_discount

            if not student_id or not class_id or not amount or not method:
                messagebox.showerror("Error", "Student, Class, Amount, and Payment Method are required")
                return

            if self._model.update(self.selected_key, student_id, class_id, month, year, amount, method, discount, remarks):
                messagebox.showinfo("Success", "Payment updated successfully!")
                self.load_records()
            else:
                messagebox.showerror("Error", "Failed to update payment.")
        except Exception as e:
            Logger.log(e)
            messagebox.showerror("Error", f"Could not Update {self.entity_name}")

    def update_fee_display(self, event=None):
        try:
            student_id = self.student_map.get(self.student_var.get())
            class_id = self.class_map.get(self.class_var.get())

            if not student_id or not class_id:
                return

            # Fetch fee
            cls = Classes().select_by_id(class_id)
            fee = float(cls.get("fee", 0.0)) if cls else 0.0

            # Fetch student discount
            self.student_discount = DiscountHandler().calculate_discount(student_id, fee)
            discounted = fee - self.student_discount

            # Update UI
            self.class_fee_var.set(f"{fee:.2f}")
            self.discounted_fee_var.set(f"{discounted:.2f}")

            # Autofill into Amount field
            self.amount_entry.delete(0, tk.END)
            self.amount_entry.insert(0, f"{discounted:.2f}")

        except Exception as e:
            Logger.log(e)

    def clear_form(self):
        self.student_var.set("")
        self.class_var.set("")
        self.month_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)
        self.class_fee_var.set("")
        self.discounted_fee_var.set("")
        self.payment_method_var.set("")
        self.remarks_entry.delete(0, tk.END)
        self.selected_key = None
        self.submit_btn.config(text="Save", command=self.save_record)
