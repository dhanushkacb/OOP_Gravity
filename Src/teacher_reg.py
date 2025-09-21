import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

# --- Database Connection ---
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="gravity_db"
    )

# --- Validations ---
def validate_contact(new_value):
    if new_value == "":
        return True
    if new_value.isdigit() and len(new_value) <= 10:
        return True
    return False

def validate_email(email):
    if email == "":
        return True
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None

# --- Center Window ---
def center_window(win, width, height):
    screen_width = win.winfo_screenwidth()
    screen_height = win.winfo_screenheight()
    x = int((screen_width - width) / 2)
    y = int((screen_height - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

# --- Clear Inputs ---
def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    entry_search.delete(0, tk.END)
    global selected_teacher_id
    selected_teacher_id = None

    # Enable Add button when form is cleared
    btn_add.config(state="normal")

    fetch_data()

# --- Add New Teacher ---
def add_teacher():
    name = entry_name.get().strip()
    subject = entry_subject.get().strip()
    contact = entry_contact.get().strip()
    email = entry_email.get().strip()

    if name == "" or subject == "":
        messagebox.showerror("Error", "Name and Subject are required!", parent=root)
        return
    if contact == "":
        messagebox.showerror("Error", "Contact is required!", parent=root)
        return
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Contact must be exactly 10 digits numeric!", parent=root)
        return
    if email != "" and not validate_email(email):
        messagebox.showerror("Error", "Invalid Email format.", parent=root)
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO teachers(name, subject, contact_no, email)
        VALUES (%s, %s, %s, %s)
    """, (name, subject, contact, email))
    conn.commit()
    conn.close()

    clear_inputs()
    messagebox.showinfo("Success", "New teacher added successfully!", parent=root)

# --- Fetch Data ---
def fetch_data(search_text=""):
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()

    if search_text.strip() == "":
        cursor.execute("SELECT teacher_id, name, subject, contact_no, email FROM teachers")
    else:
        query = """
        SELECT teacher_id, name, subject, contact_no, email 
        FROM teachers
        WHERE name LIKE %s OR contact_no LIKE %s
        """
        like_pattern = f"%{search_text}%"
        cursor.execute(query, (like_pattern, like_pattern))

    rows = cursor.fetchall()
    for index, row in enumerate(rows):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=row, tags=(tag,))
    conn.close()

# --- Search ---
def search_teacher():
    search_text = entry_search.get().strip()
    fetch_data(search_text)

# --- Select Record for Update ---
def select_teacher(event):
    global selected_teacher_id
    selected = tree.selection()
    if not selected:
        return
    data = tree.item(selected[0])['values']
    selected_teacher_id = data[0]

    entry_name.delete(0, tk.END)
    entry_name.insert(0, str(data[1]))

    entry_subject.delete(0, tk.END)
    entry_subject.insert(0, str(data[2]))

    entry_contact.delete(0, tk.END)
    entry_contact.insert(0, str(data[3]))

    entry_email.delete(0, tk.END)
    entry_email.insert(0, str(data[4]))

    # Disable Add button when editing
    btn_add.config(state="disabled")

# --- Update Teacher ---
def update_teacher():
    global selected_teacher_id
    if not selected_teacher_id:
        messagebox.showerror("Error", "Select a record to update", parent=root)
        return

    name = entry_name.get().strip()
    subject = entry_subject.get().strip()
    contact = entry_contact.get().strip()
    email = entry_email.get().strip()

    if name == "" or subject == "":
        messagebox.showerror("Error", "Name and Subject are required!", parent=root)
        return
    if contact == "":
        messagebox.showerror("Error", "Contact is required!", parent=root)
        return
    if not contact.isdigit() or len(contact) != 10:
        messagebox.showerror("Error", "Contact must be exactly 10 digits numeric!", parent=root)
        return
    if email != "" and not validate_email(email):
        messagebox.showerror("Error", "Invalid Email format.", parent=root)
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE teachers
        SET name=%s, subject=%s, contact_no=%s, email=%s
        WHERE teacher_id=%s
    """, (name, subject, contact, email, selected_teacher_id))
    conn.commit()
    conn.close()

    clear_inputs()
    messagebox.showinfo("Success", "Teacher record updated successfully!", parent=root)

# --- Tkinter Window ---
root = tk.Tk()
root.title("Teachers Registration")
center_window(root, 850, 550)

# --- Input Frame ---
frame_input = tk.Frame(root, pady=10)
frame_input.pack(padx=10, pady=10, anchor="w")

label_width = 12
entry_width = 40

# --- Entry Widgets ---
tk.Label(frame_input, text="Name:", width=label_width, anchor="w").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_input, width=entry_width)
entry_name.grid(row=0, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_input, text="Subject:", width=label_width, anchor="w").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_subject = tk.Entry(frame_input, width=entry_width)
entry_subject.grid(row=1, column=1, padx=5, pady=5, sticky="w")

vcmd = root.register(validate_contact)
tk.Label(frame_input, text="Contact:", width=label_width, anchor="w").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_contact = tk.Entry(frame_input, validate="key", validatecommand=(vcmd, "%P"), width=entry_width)
entry_contact.grid(row=2, column=1, padx=5, pady=5, sticky="w")

tk.Label(frame_input, text="Email:", width=label_width, anchor="w").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_input, width=entry_width)
entry_email.grid(row=3, column=1, padx=5, pady=5, sticky="w")

# --- Buttons Frame ---
btn_frame = tk.Frame(frame_input, pady=20)
btn_frame.grid(row=4, column=0, columnspan=2)

btn_add = tk.Button(btn_frame, text="Add New", command=add_teacher, bg="green", fg="white")
btn_add.pack(side="left", padx=10)

btn_update = tk.Button(btn_frame, text="Update", command=update_teacher, bg="blue", fg="white")
btn_update.pack(side="left", padx=10)

btn_clear = tk.Button(btn_frame, text="Clear", command=clear_inputs, bg="orange", fg="white")
btn_clear.pack(side="left", padx=10)

# --- Search Frame ---
search_frame = tk.Frame(root, pady=5)
search_frame.pack(fill="x", padx=10)

tk.Label(search_frame, text="Search by Name or Phone:", anchor="w").pack(side="left")
entry_search = tk.Entry(search_frame, width=30)
entry_search.pack(side="left", padx=5)
tk.Button(search_frame, text="Search", command=search_teacher, bg="blue", fg="white").pack(side="left", padx=5)

# --- Table Frame ---
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Subject", "Contact", "Email")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Scrollbar
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Treeview style
style = ttk.Style()
style.configure("Treeview", rowheight=25, font=('Arial', 11))
tree.tag_configure('oddrow', background='#f9f9f9')
tree.tag_configure('evenrow', background='#ffffff')

# Headings
for col in columns:
    tree.heading(col, text=col, anchor="w")
    tree.column(col, anchor="w", width=120)

tree.pack(fill="both", expand=True)

# Bind select
tree.bind("<<TreeviewSelect>>", select_teacher)

# --- Initial Data Load ---
selected_teacher_id = None
fetch_data()

root.mainloop()
