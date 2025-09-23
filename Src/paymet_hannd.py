import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

# -------------------------
# Domain Model
# -------------------------
@dataclass
class Payment:
    payment_id: int
    student_id: str
    class_id: str
    month: str
    year: int
    amount: float
    discount_percent: float
    payment_on: str

    @property
    def discount_amount(self) -> float:
        return round(self.amount * self.discount_percent / 100.0, 2)

    @property
    def net_amount(self) -> float:
        return round(self.amount - self.discount_amount, 2)


class PaymentManager:
   
    def __init__(self):
        self._payments: List[Payment] = []
        self._next_id = 1

    def _generate_id(self) -> int:
        pid = self._next_id
        self._next_id += 1
        return pid

    def add_payment(self, student_id: str, class_id: str, month: str, year: int,
                    amount: float, discount_percent: float) -> Payment:
        pid = self._generate_id()
        payment_on = datetime.now().isoformat(sep=" ", timespec="seconds")
        p = Payment(pid, student_id, class_id, month, year, amount, discount_percent, payment_on)
        self._payments.append(p)
        return p

    def update_payment(self, payment_id: int, student_id: str, class_id: str, month: str, year: int,
                       amount: float, discount_percent: float) -> bool:
        p = self.get_by_id(payment_id)
        if p is None:
            return False
        p.student_id = student_id
        p.class_id = class_id
        p.month = month
        p.year = year
        p.amount = amount
        p.discount_percent = discount_percent
        return True

    def delete_payment(self, payment_id: int) -> bool:
        idx = next((i for i, p in enumerate(self._payments) if p.payment_id == payment_id), None)
        if idx is None:
            return False
        self._payments.pop(idx)
        return True

    def list_all(self) -> List[Payment]:
        return list(self._payments)

    def search(self, student_id: Optional[str] = None, class_id: Optional[str] = None) -> List[Payment]:
        results = self._payments
        if student_id:
            results = [p for p in results if student_id.lower() in p.student_id.lower()]
        if class_id:
            results = [p for p in results if class_id.lower() in p.class_id.lower()]
        return results

    def get_by_id(self, payment_id: int) -> Optional[Payment]:
        return next((p for p in self._payments if p.payment_id == payment_id), None)


# -------------------------
# UI Layer
# -------------------------
class PaymentApp:
    def __init__(self, root: tk.Tk, manager: PaymentManager):
        self.root = root
        self.manager = manager
        self.selected_payment_id: Optional[int] = None

        root.title("Student Fee & Discount Manager")
        root.geometry("1000x600")
        root.minsize(900, 500)
        root.columnconfigure(0, weight=1)
        root.rowconfigure(3, weight=1)

        # Title
        tk.Label(root, text="Student Fee & Discount Manager", font=("Arial", 18, "bold")).grid(
            row=0, column=0, pady=10
        )

        # ---------------- Form ----------------
        form_frame = tk.Frame(root, relief=tk.GROOVE, borderwidth=1, padx=10, pady=10)
        form_frame.grid(row=1, column=0, sticky="ew", padx=15, pady=(0, 10))
        form_frame.columnconfigure(1, weight=1)

        lbl_opts = {"anchor": "w", "font": ("Arial", 10)}
        tk.Label(form_frame, text="Student ID:", **lbl_opts).grid(row=0, column=0, sticky="w", padx=5, pady=4)
        self.student_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.student_id_var).grid(row=0, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Class ID:", **lbl_opts).grid(row=1, column=0, sticky="w", padx=5, pady=4)
        self.class_id_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.class_id_var).grid(row=1, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Month:", **lbl_opts).grid(row=2, column=0, sticky="w", padx=5, pady=4)
        self.month_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.month_var).grid(row=2, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Year:", **lbl_opts).grid(row=3, column=0, sticky="w", padx=5, pady=4)
        self.year_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.year_var).grid(row=3, column=1, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Amount:", **lbl_opts).grid(row=0, column=2, sticky="w", padx=15, pady=4)
        self.amount_var = tk.StringVar()
        tk.Entry(form_frame, textvariable=self.amount_var).grid(row=0, column=3, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Discount %:", **lbl_opts).grid(row=1, column=2, sticky="w", padx=15, pady=4)
        self.discount_var = tk.StringVar(value="0")
        tk.Entry(form_frame, textvariable=self.discount_var).grid(row=1, column=3, sticky="ew", padx=5, pady=4)

        tk.Label(form_frame, text="Discount Amount:", **lbl_opts).grid(row=2, column=2, sticky="w", padx=15, pady=4)
        self.discount_amount_lbl = tk.Label(form_frame, text="0.00", anchor="w")
        self.discount_amount_lbl.grid(row=2, column=3, sticky="w", padx=5, pady=4)

        tk.Label(form_frame, text="Net Amount:", **lbl_opts).grid(row=3, column=2, sticky="w", padx=15, pady=4)
        self.net_amount_lbl = tk.Label(form_frame, text="0.00", anchor="w")
        self.net_amount_lbl.grid(row=3, column=3, sticky="w", padx=5, pady=4)

        # Buttons
        action_frame = tk.Frame(form_frame)
        action_frame.grid(row=4, column=0, columnspan=4, pady=(8, 0), sticky="e")
        self.add_btn = tk.Button(action_frame, text="Add Payment", width=15, command=self.add_payment)
        self.add_btn.grid(row=0, column=0, padx=6)
        self.update_btn = tk.Button(action_frame, text="Update Selected", width=15, command=self.update_payment, state="disabled")
        self.update_btn.grid(row=0, column=1, padx=6)
        self.clear_btn = tk.Button(action_frame, text="Clear", width=10, command=self.clear_form)
        self.clear_btn.grid(row=0, column=2, padx=6)

        for var in (self.amount_var, self.discount_var):
            var.trace_add("write", lambda *args: self._recompute_totals())

        # ---------------- Search + Treeview ----------------
        search_frame = tk.Frame(root)
        search_frame.grid(row=2, column=0, sticky="ew", padx=15, pady=6)
        search_frame.columnconfigure(3, weight=1)

        tk.Label(search_frame, text="Search Student ID:").grid(row=0, column=0, sticky="w", padx=5)
        self.search_student_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_student_var).grid(row=0, column=1, padx=5)

        tk.Label(search_frame, text="Class ID:").grid(row=0, column=2, sticky="w", padx=5)
        self.search_class_var = tk.StringVar()
        tk.Entry(search_frame, textvariable=self.search_class_var).grid(row=0, column=3, sticky="ew", padx=5)

        tk.Button(search_frame, text="Search", command=self.search_payments, width=12).grid(row=0, column=4, padx=6)
        tk.Button(search_frame, text="Show All", command=self.load_payments, width=12).grid(row=0, column=5, padx=6)

        # Treeview
        tree_frame = tk.Frame(root)
        tree_frame.grid(row=3, column=0, sticky="nsew", padx=15, pady=6)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        cols = ("payment_id", "student_id", "class_id", "month", "year", "amount",
                "discount_percent", "discount_amount", "net_amount", "payment_on")
        self.tree = ttk.Treeview(tree_frame, columns=cols, show="headings", selectmode="browse")
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100, anchor="center")

        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=1, sticky="ns")

        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        self.load_payments()

    # ---------------- Methods ----------------
    def _recompute_totals(self):
        try:
            amount = float(self.amount_var.get())
        except ValueError:
            amount = 0.0
        try:
            discount = float(self.discount_var.get())
        except ValueError:
            discount = 0.0
        discount_amount = round(amount * discount / 100.0, 2)
        net_amount = round(amount - discount_amount, 2)
        self.discount_amount_lbl.config(text=f"{discount_amount:.2f}")
        self.net_amount_lbl.config(text=f"{net_amount:.2f}")

    def clear_form(self):
        self.student_id_var.set("")
        self.class_id_var.set("")
        self.month_var.set("")
        self.year_var.set("")
        self.amount_var.set("")
        self.discount_var.set("0")
        self.discount_amount_lbl.config(text="0.00")
        self.net_amount_lbl.config(text="0.00")
        self.selected_payment_id = None
        self.update_btn.config(state="disabled")
        self.add_btn.config(state="normal")

    def add_payment(self):
        try:
            p = self.manager.add_payment(
                self.student_id_var.get(),
                self.class_id_var.get(),
                self.month_var.get(),
                int(self.year_var.get()),
                float(self.amount_var.get()),
                float(self.discount_var.get())
            )
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        self.load_payments()
        self.clear_form()

    def update_payment(self):
        if self.selected_payment_id is None:
            return
        try:
            success = self.manager.update_payment(
                self.selected_payment_id,
                self.student_id_var.get(),
                self.class_id_var.get(),
                self.month_var.get(),
                int(self.year_var.get()),
                float(self.amount_var.get()),
                float(self.discount_var.get())
            )
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))
            return
        if success:
            self.load_payments()
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to update payment.")

    def load_payments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in self.manager.list_all():
            self.tree.insert("", "end", values=(
                p.payment_id, p.student_id, p.class_id, p.month, p.year, p.amount,
                p.discount_percent, p.discount_amount, p.net_amount, p.payment_on
            ))

    def search_payments(self):
        student = self.search_student_var.get()
        class_id = self.search_class_var.get()
        results = self.manager.search(student_id=student, class_id=class_id)
        for row in self.tree.get_children():
            self.tree.delete(row)
        for p in results:
            self.tree.insert("", "end", values=(
                p.payment_id, p.student_id, p.class_id, p.month, p.year, p.amount,
                p.discount_percent, p.discount_amount, p.net_amount, p.payment_on
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        item = self.tree.item(selected[0])
        values = item["values"]
        self.selected_payment_id = values[0]
        self.student_id_var.set(values[1])
        self.class_id_var.set(values[2])
        self.month_var.set(values[3])
        self.year_var.set(values[4])
        self.amount_var.set(values[5])
        self.discount_var.set(values[6])
        self._recompute_totals()
        self.update_btn.config(state="normal")
        self.add_btn.config(state="disabled")


# -------------------------
# Main
# -------------------------
if __name__ == "__main__":
    root = tk.Tk()
    manager = PaymentManager()
    app = PaymentApp(root, manager)
    root.mainloop()
