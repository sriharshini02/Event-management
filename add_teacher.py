import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_config import DB_CONFIG


def connect_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def add_teacher():
    """Insert teacher details into Users and Teachers tables."""
    user_id = entry_user_id.get()
    first_name = entry_first_name.get()
    last_name = entry_last_name.get()
    username = entry_username.get()
    password = entry_password.get()

    if not all([user_id, first_name, last_name, username, password]):
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = None
    try:
        cursor = conn.cursor()

        # Insert into Users table
        cursor.execute(
            "INSERT INTO Users (UserID, UserName, UserRole, UserPass) VALUES (%s, %s, 'Teacher', %s)",
            (user_id, username, password),
        )

        # Insert into Teachers table
        cursor.execute(
            "INSERT INTO Teachers (UserID, TeacherFName, TeacherLName) VALUES (%s, %s, %s)",
            (user_id, first_name, last_name),
        )

        conn.commit()
        messagebox.showinfo("Success", "Teacher added successfully!")
        add_teacher_window.destroy()

    except mysql.connector.Error as err:
        conn.rollback()  # Rollback on failure
        messagebox.showerror("Database Error", f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        conn.close()


def open_add_teacher_window():
    """Open the add teacher window."""
    global add_teacher_window, entry_user_id, entry_first_name, entry_last_name, entry_username, entry_password

    add_teacher_window = tk.Toplevel()
    add_teacher_window.title("Add Teacher")
    add_teacher_window.geometry("350x300")

    tk.Label(add_teacher_window, text="User ID (Role Number)").pack()
    entry_user_id = tk.Entry(add_teacher_window)
    entry_user_id.pack()

    tk.Label(add_teacher_window, text="First Name").pack()
    entry_first_name = tk.Entry(add_teacher_window)
    entry_first_name.pack()

    tk.Label(add_teacher_window, text="Last Name").pack()
    entry_last_name = tk.Entry(add_teacher_window)
    entry_last_name.pack()

    tk.Label(add_teacher_window, text="Username").pack()
    entry_username = tk.Entry(add_teacher_window)
    entry_username.pack()

    tk.Label(add_teacher_window, text="Password").pack()
    entry_password = tk.Entry(add_teacher_window, show="*")  # Hide password input
    entry_password.pack()

    tk.Button(add_teacher_window, text="Add Teacher", command=add_teacher).pack(pady=10)
