import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_config import DB_CONFIG


def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def add_student_window(root):
    """Create the Add Student window."""
    add_window = tk.Toplevel(root)
    add_window.title("Add Student")
    add_window.geometry("400x250")

    def add_student():
        """Insert student details into the database."""
        user_id = entry_userid.get()
        username = entry_username.get()
        student_class = class_var.get()

        if not (user_id and username and student_class):
            messagebox.showerror("Error", "All fields are required!", parent=add_window)
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            # Insert into Users table
            cursor.execute(
                "INSERT INTO Users (UserID, UserName, UserRole, UserPass) VALUES (%s, %s, 'Student', %s)",
                (user_id, username, "defaultpass"),
            )

            # Insert into Students table
            cursor.execute(
                "INSERT INTO Students (UserID, StudentClass) VALUES (%s, %s)",
                (user_id, student_class),
            )

            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success", "Student added successfully!", parent=add_window
            )
            entry_userid.delete(0, tk.END)
            entry_username.delete(0, tk.END)
            class_var.set("1")
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=add_window)

    tk.Label(add_window, text="Student Roll Number:").pack()
    entry_userid = tk.Entry(add_window)
    entry_userid.pack()

    tk.Label(add_window, text="Student Name:").pack()
    entry_username = tk.Entry(add_window)
    entry_username.pack()

    tk.Label(add_window, text="Student Class:").pack()
    class_var = tk.StringVar(add_window)
    class_var.set("1")  # Default class
    class_menu = tk.OptionMenu(add_window, class_var, *map(str, range(1, 13)))
    class_menu.pack()

    tk.Button(add_window, text="Add Student", command=add_student).pack(pady=10)
    tk.Button(add_window, text="Close", command=add_window.destroy).pack()
