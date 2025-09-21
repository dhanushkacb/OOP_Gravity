import tkinter as tk
from tkinter import messagebox
from Src.config.Settings import Settings
from Src.db.Schema import ClassRoom

class ClassroomRegistration:

    def __init__(self):
        self.reg_window = tk.Toplevel()
        self._classrooms = ClassRoom()
        
        self.reg_window.title("Classroom Registration")
        self.reg_window.geometry("420x320")
        self.reg_window.resizable(False, False)

        # Main frame
        self.form_frame = tk.Frame(self.reg_window, padx=20, pady=20)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Title
        tk.Label(
            self.form_frame,
            text="Classroom Registration",
            font=("Arial", 16, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Classroom Code
        tk.Label(self.form_frame, text="Classroom Code:", anchor="w").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.code_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.code_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")
        self.code_entry.focus_set()

        # Capacity
        tk.Label(self.form_frame, text="Capacity:", anchor="w").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.capacity_entry = tk.Entry(self.form_frame, width=Settings.ENTRY_WIDTH)
        self.capacity_entry.grid(row=2, column=1, padx=5, pady=5, sticky="ew")

        # Facilities (Boolean options)
        self.has_ac_var = tk.BooleanVar(value=False)
        self.has_whiteboard_var = tk.BooleanVar(value=True)
        self.has_screen_var = tk.BooleanVar(value=False)

        tk.Checkbutton(self.form_frame, text="Air Conditioned", variable=self.has_ac_var).grid(row=3, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Whiteboard", variable=self.has_whiteboard_var).grid(row=4, column=1, sticky="w", padx=5, pady=5)
        tk.Checkbutton(self.form_frame, text="Screen", variable=self.has_screen_var).grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # Register button
        self.submit_btn = tk.Button(
            self.form_frame,
            text="Register Classroom",
            command=self.register_classroom,
            font=("Arial", 12, "bold"),
            bg="#4CAF50",
            fg="white"
        )
        self.submit_btn.grid(row=6, column=0, columnspan=2, pady=20)

        # Grid weights
        self.form_frame.columnconfigure(0, weight=1)
        self.form_frame.columnconfigure(1, weight=3)

        # Bind Enter key
        self.reg_window.bind("<Return>", self.register_classroom)

    def register_classroom(self, event=None):
        code = self.code_entry.get().strip()
        capacity = self.capacity_entry.get().strip()

        # Validate input
        if not code or not capacity.isdigit():
            messagebox.showerror("Error", "Valid classroom code and numeric capacity are required")
            return

        # Convert checkboxes
        has_ac = self.has_ac_var.get()
        has_whiteboard = self.has_whiteboard_var.get()
        has_screen = self.has_screen_var.get()

        if self._classrooms.add_classroom(code, int(capacity), has_ac, has_whiteboard, has_screen):
            messagebox.showinfo("Success", "Classroom registered successfully!")
            self.reg_window.destroy()
        else:
            messagebox.showerror("Error", "Failed to register classroom.")
