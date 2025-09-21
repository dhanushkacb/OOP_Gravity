import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re

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

# --- Fetch Data ---
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    rows = cursor.fetchall()
    for index, row in enumerate(rows):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", tk.END, values=row, tags=(tag,))
    auto_adjust_columns()
    conn.close()

# --- Clear Inputs ---
def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_email.delete(0, tk.END)
    global selected_teacher_id
    selected_teacher_id = None

# --- Select Teacher ---
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
    entry_contact.insert(0, str(data[3]))  # <-- ensure leading zero is preserved

    entry_email.delete(0, tk.END)
    entry_email.insert(0, str(data[4]))

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

    fetch_data()
    clear_inputs()
    messagebox.showinfo("Success", "New teacher added successfully!", parent=root)

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

    fetch_data()
    clear_inputs()
    messagebox.showinfo("Success", "Teacher record updated successfully!", parent=root)

# --- Delete Teacher ---
def delete_teacher():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete", parent=root)
        return
    teacher_id = tree.item(selected[0])['values'][0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE teacher_id=%s", (teacher_id,))
    conn.commit()
    conn.close()

    fetch_data()
    clear_inputs()
    messagebox.showinfo("Success", "Teacher record deleted successfully!", parent=root)

# --- Auto adjust columns width ---
def auto_adjust_columns():
    for col in columns:
        if col == "ID":
            tree.column(col, width=50, anchor="center")
            continue
        max_width = max([len(str(tree.set(item, col))) for item in tree.get_children()] + [len(col)])
        tree.column(col, width=max(120, max_width*10), anchor="w")

# --- Tkinter Window ---
root = tk.Tk()
root.title("Teachers Registration")
center_window(root, 1000, 650)

selected_teacher_id = None

# --- Input Frame ---
frame_input = tk.Frame(root, pady=10)
frame_input.pack(padx=10, pady=10)

label_width = 12  # label width for alignment
entry_width = 45  # wider entry fields

tk.Label(frame_input, text="Name:", width=label_width, anchor="e").grid(row=0, column=0, padx=10, pady=5)
entry_name = tk.Entry(frame_input, width=entry_width)
entry_name.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Subject:", width=label_width, anchor="e").grid(row=1, column=0, padx=10, pady=5)
entry_subject = tk.Entry(frame_input, width=entry_width)
entry_subject.grid(row=1, column=1, padx=10, pady=5)

vcmd = root.register(validate_contact)
tk.Label(frame_input, text="Contact:", width=label_width, anchor="e").grid(row=2, column=0, padx=10, pady=5)
entry_contact = tk.Entry(frame_input, validate="key", validatecommand=(vcmd, "%P"), width=entry_width)
entry_contact.grid(row=2, column=1, padx=10, pady=5)

tk.Label(frame_input, text="Email:", width=label_width, anchor="e").grid(row=3, column=0, padx=10, pady=5)
entry_email = tk.Entry(frame_input, width=entry_width)
entry_email.grid(row=3, column=1, padx=10, pady=5)

# Buttons
btn_frame = tk.Frame(frame_input)
btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

tk.Button(btn_frame, text="Add New", command=add_teacher, bg="green", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame, text="Update", command=update_teacher, bg="blue", fg="white").pack(side="left", padx=5)
tk.Button(btn_frame, text="Clear", command=clear_inputs, bg="orange", fg="white").pack(side="left", padx=5)

# --- Table Frame ---
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Subject", "Contact", "Email", "Created At")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

# Scrollbar
scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview)
tree.configure(yscroll=scrollbar.set)
scrollbar.pack(side="right", fill="y")

# Treeview style
style = ttk.Style()
style.configure("Treeview", rowheight=30, font=('Arial', 11))
tree.tag_configure('oddrow', background='#f9f9f9')
tree.tag_configure('evenrow', background='#ffffff')

# Headings
for col in columns:
    tree.heading(col, text=col, anchor="center")

tree.pack(fill="both", expand=True)
tree.bind("<<TreeviewSelect>>", select_teacher)

tk.Button(root, text="Delete Selected", command=delete_teacher, bg="red", fg="white").pack(pady=5)

fetch_data()
root.mainloop()
