import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk


# Dummy Teachers class (replace with DB later)
class Teachers:
    def add_teacher(self, name, subject, contact, email):
        print(f"[DEBUG] Adding teacher -> Name: {name}, Subject: {subject}, Contact: {contact}, Email: {email}")
        return True  # Always succeed for testing


class TeacherRegistration:

    def __init__(self, master):
        # Create popup window
        self.reg_window = tk.Toplevel(master)
        self.reg_window.title("Teacher Registration")
        self.reg_window.geometry("450x350")
        self.reg_window.resizable(False, False)

        # Make sure this window closes the app if root is hidden
        self.reg_window.protocol("WM_DELETE_WINDOW", master.destroy)

        self._teachers = Teachers()

        # Main frame for form
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title label
        tk.Label(self.form_frame, text="Teacher Registration", font=("Arial", 16, "bold")).grid(
            row=0, column=0, columnspan=2, pady=(0, 15)
        )

        entry_width = 30

        # Teacher Name
        tk.Label(self.form_frame, text="Teacher Name:", anchor="w").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.name_entry = tk.Entry(self.form_frame, width=entry_width)
        self.name_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")

        # Subject
        tk.Label(self.form_frame, text="Subject:", anchor="w").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.subject_entry = tk.Entry(self.form_frame, width=entry_width)
        self.subject_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")

        # Contact Number
        tk.Label(self.form_frame, text="Contact Number:", anchor="w").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.contact_entry = tk.Entry(self.form_frame, width=entry_width)
        self.contact_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")

        # Email
        tk.Label(self.form_frame, text="Email:", anchor="w").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.email_entry = tk.Entry(self.form_frame, width=entry_width)
        self.email_entry.grid(row=4, column=1, padx=10, pady=5, sticky="w")

        # Buttons
        btn_frame = tk.Frame(self.form_frame)
        btn_frame.grid(row=5, column=1, padx=10, pady=20, sticky="e")

        self.submit_btn = tk.Button(
            btn_frame,
            text="Register",
            command=self.register_teacher,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            relief=tk.RAISED,
            width=12
        )
        self.submit_btn.pack(anchor="e")

        self.form_frame.columnconfigure(0, weight=0)
        self.form_frame.columnconfigure(1, weight=1)

    def register_teacher(self, event=None):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()

        # Basic validations
        if not name or not subject or not contact or not email:
            messagebox.showerror("Error", "All fields are required")
            return

        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Contact number must be 10 digits")
            return

        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Invalid email address")
            return

        if self._teachers.add_teacher(name, subject, contact, email):
            messagebox.showinfo("Success", "Teacher registered successfully!")
            self.reg_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to register teacher.")


# Run standalone as a clean popup
if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    TeacherRegistration(root)
    root.mainloop()

