import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont

# --- Teachers Data Class (replace with DB later) ---
class Teachers:
    def __init__(self):
        self.data = []  # Each item: {"name":..., "subject":..., "contact":..., "email":...}

    def get_all(self):
        return self.data

    def search_by_name(self, name):
        return [t for t in self.data if name.lower() in t["name"].lower()]

    def delete_teacher(self, index):
        if 0 <= index < len(self.data):
            self.data.pop(index)
            return True
        return False

    def update_teacher(self, index, name, subject, contact, email):
        if 0 <= index < len(self.data):
            self.data[index] = {"name": name, "subject": subject, "contact": contact, "email": email}
            return True
        return False

# --- Teacher Management Window ---
class TeacherManagement:

    def __init__(self, master=None, teachers=None):
        self._teachers = teachers or Teachers()

        if master is None:
            self.window = tk.Tk()
        else:
            self.window = tk.Toplevel(master)

        self.window.title("Teacher Details")
        self.window.geometry("900x600")
        self.window.minsize(700, 400)
        self.window.state("zoomed")  # Start maximized
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(2, weight=1)

        # --- Title Frame ---
        title_frame = tk.Frame(self.window)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)
        tk.Label(title_frame, text="Teacher Details", font=("Arial", 18, "bold")).pack(side="left")

        # --- Search Frame ---
        search_frame = tk.Frame(self.window)
        search_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=5)
        search_frame.columnconfigure(1, weight=1)

        tk.Label(search_frame, text="Search by Name:", font=("Arial", 11)).grid(row=0, column=0, sticky="w")
        self.search_entry = tk.Entry(search_frame, font=("Arial", 11))
        self.search_entry.grid(row=0, column=1, sticky="ew", padx=10)
        tk.Button(search_frame, text="Search", command=self.search_teacher, font=("Arial", 11)).grid(row=0, column=2, padx=5)
        tk.Button(search_frame, text="Show All", command=self.load_teachers, font=("Arial", 11)).grid(row=0, column=3, padx=5)

        # --- Treeview Frame ---
        tree_frame = tk.Frame(self.window)
        tree_frame.grid(row=2, column=0, sticky="nsew", padx=20, pady=10)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        columns = ("name", "subject", "contact", "email")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.title())
            self.tree.column(col, anchor="w")  # Initial anchor

        # Scrollbars
        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")

        # --- Buttons Frame ---
        btn_frame = tk.Frame(self.window)
        btn_frame.grid(row=3, column=0, pady=10)
        tk.Button(btn_frame, text="Edit Selected", command=self.edit_teacher, width=15, font=("Arial", 11)).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_teacher, width=15, font=("Arial", 11)).grid(row=0, column=1, padx=10)

        self.load_teachers()

    # --- Load / Search ---
    def load_teachers(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i, teacher in enumerate(self._teachers.get_all()):
            self.tree.insert("", "end", iid=i, values=(teacher["name"], teacher["subject"], teacher["contact"], teacher["email"]))
        self.auto_resize_columns()

    def search_teacher(self):
        query = self.search_entry.get()
        for i in self.tree.get_children():
            self.tree.delete(i)
        for i, teacher in enumerate(self._teachers.search_by_name(query)):
            self.tree.insert("", "end", iid=i, values=(teacher["name"], teacher["subject"], teacher["contact"], teacher["email"]))
        self.auto_resize_columns()

    # --- Edit Teacher ---
    def edit_teacher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No teacher selected")
            return
        index = int(selected[0])
        TeacherRegistration(self.window, self._teachers, index=index, refresh_callback=self.load_teachers)

    # --- Delete Teacher ---
    def delete_teacher(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "No teacher selected")
            return
        index = int(selected[0])
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this teacher?"):
            self._teachers.delete_teacher(index)
            self.load_teachers()

    # --- Auto Resize Columns Based on Content ---
    def auto_resize_columns(self):
        font = tkfont.Font()
        for col in self.tree["columns"]:
            max_width = font.measure(col.title()) + 10  # Column title width
            for item in self.tree.get_children():
                cell_text = str(self.tree.set(item, col))
                cell_width = font.measure(cell_text) + 10
                if cell_width > max_width:
                    max_width = cell_width
            self.tree.column(col, width=max_width)

# --- Teacher Edit Popup ---
class TeacherRegistration:

    def __init__(self, master, teachers, index=None, refresh_callback=None):
        self._teachers = teachers
        self.index = index
        self.refresh_callback = refresh_callback

        self.window = tk.Toplevel(master)
        self.window.title("Edit Teacher")
        self.window.geometry("450x350")
        self.window.resizable(False, False)

        self.form_frame = tk.Frame(self.window, padx=20, pady=20, relief=tk.RIDGE, borderwidth=2)
        self.form_frame.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Label(self.form_frame, text="Edit Teacher", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 15))

        entry_width = 30
        tk.Label(self.form_frame, text="Teacher Name:").grid(row=1, column=0, sticky="w")
        tk.Label(self.form_frame, text="Subject:").grid(row=2, column=0, sticky="w")
        tk.Label(self.form_frame, text="Contact Number:").grid(row=3, column=0, sticky="w")
        tk.Label(self.form_frame, text="Email:").grid(row=4, column=0, sticky="w")

        self.name_entry = tk.Entry(self.form_frame, width=entry_width)
        self.name_entry.grid(row=1, column=1, pady=5)
        self.subject_entry = tk.Entry(self.form_frame, width=entry_width)
        self.subject_entry.grid(row=2, column=1, pady=5)
        self.contact_entry = tk.Entry(self.form_frame, width=entry_width)
        self.contact_entry.grid(row=3, column=1, pady=5)
        self.email_entry = tk.Entry(self.form_frame, width=entry_width)
        self.email_entry.grid(row=4, column=1, pady=5)

        tk.Button(self.form_frame, text="Update", command=self.save_teacher, width=12, font=("Arial", 11)).grid(row=5, column=1, pady=20, sticky="e")

        # Populate fields if editing
        if index is not None:
            teacher = self._teachers.get_all()[index]
            self.name_entry.insert(0, teacher["name"])
            self.subject_entry.insert(0, teacher["subject"])
            self.contact_entry.insert(0, teacher["contact"])
            self.email_entry.insert(0, teacher["email"])

    def save_teacher(self):
        name = self.name_entry.get()
        subject = self.subject_entry.get()
        contact = self.contact_entry.get()
        email = self.email_entry.get()

        if not name or not subject or not contact or not email:
            messagebox.showerror("Error", "All fields are required")
            return
        if not contact.isdigit() or len(contact) != 10:
            messagebox.showerror("Error", "Contact number must be 10 digits")
            return
        if "@" not in email or "." not in email:
            messagebox.showerror("Error", "Invalid email address")
            return

        self._teachers.update_teacher(self.index, name, subject, contact, email)
        if self.refresh_callback:
            self.refresh_callback()
        self.window.destroy()

# --- Run Management Window ---
if __name__ == "__main__":
    TeachersDB = Teachers()
    app = TeacherManagement(teachers=TeachersDB)
    app.window.mainloop()
