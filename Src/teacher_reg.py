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

# --- Validation functions ---
def validate_contact(new_value):
    """Allow only digits and max 10 length for contact"""
    if new_value == "":
        return True
    if new_value.isdigit() and len(new_value) <= 10:
        return True
    return False


def validate_email(email):
    """Check email format"""
    if email == "":
        return True
    pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    return re.match(pattern, email) is not None


# --- Functions ---
def fetch_data():
    for row in tree.get_children():
        tree.delete(row)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM teachers")
    rows = cursor.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)

    conn.close()


def add_teacher():
    name = entry_name.get()
    subject = entry_subject.get()
    contact = entry_contact.get()
    email = entry_email.get()

    # --- Validations ---
    if name == "" or subject == "":
        messagebox.showerror("Error", "Name and Subject are required!")
        return

    if contact != "" and (not contact.isdigit() or len(contact) > 10):
        messagebox.showerror("Error", "Contact must be digits only (max 10).")
        return

    if email != "" and not validate_email(email):
        messagebox.showerror("Error", "Invalid Email format.")
        return

    # --- Insert into DB ---
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO teachers (name, subject, contact_no, email) VALUES (%s, %s, %s, %s)",
                   (name, subject, contact, email))
    conn.commit()
    conn.close()

    fetch_data()
    clear_inputs()
    messagebox.showinfo("Success", "Teacher added successfully!")


def clear_inputs():
    entry_name.delete(0, tk.END)
    entry_subject.delete(0, tk.END)
    entry_contact.delete(0, tk.END)
    entry_email.delete(0, tk.END)


def delete_teacher():
    selected = tree.selection()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete")
        return

    teacher_id = tree.item(selected[0])['values'][0]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM teachers WHERE teacher_id=%s", (teacher_id,))
    conn.commit()
    conn.close()

    fetch_data()
    messagebox.showinfo("Success", "Teacher deleted successfully!")


# --- Tkinter Window ---
root = tk.Tk()
root.title("Teachers Management System")
root.geometry("750x550")

# Input Frame
frame_input = tk.Frame(root, pady=10)
frame_input.pack()

tk.Label(frame_input, text="Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
entry_name = tk.Entry(frame_input)
entry_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame_input, text="Subject").grid(row=1, column=0, padx=5, pady=5, sticky="w")
entry_subject = tk.Entry(frame_input)
entry_subject.grid(row=1, column=1, padx=5, pady=5)

# Contact with validation
vcmd = root.register(validate_contact)
tk.Label(frame_input, text="Contact").grid(row=2, column=0, padx=5, pady=5, sticky="w")
entry_contact = tk.Entry(frame_input, validate="key", validatecommand=(vcmd, "%P"))
entry_contact.grid(row=2, column=1, padx=5, pady=5)

# Email input
tk.Label(frame_input, text="Email").grid(row=3, column=0, padx=5, pady=5, sticky="w")
entry_email = tk.Entry(frame_input)
entry_email.grid(row=3, column=1, padx=5, pady=5)

# Buttons
tk.Button(frame_input, text="Add Teacher", command=add_teacher, bg="green", fg="white").grid(row=4, column=0, pady=10)
tk.Button(frame_input, text="Clear", command=clear_inputs, bg="orange", fg="white").grid(row=4, column=1, pady=10)

# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(fill="both", expand=True, padx=10, pady=10)

columns = ("ID", "Name", "Subject", "Contact", "Email", "Created At")
tree = ttk.Treeview(frame_table, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120)

tree.pack(fill="both", expand=True)

tk.Button(root, text="Delete Selected", command=delete_teacher, bg="red", fg="white").pack(pady=5)

# Load Data
fetch_data()

root.mainloop()
