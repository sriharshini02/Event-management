import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys
from db_config import DB_CONFIG
import os


def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def login():
    user_id = entry_user_id.get()
    username = entry_username.get()
    password = entry_password.get()

    conn = connect_db()
    if conn:
        cursor = conn.cursor(dictionary=True)  # type: ignore
        query = "SELECT * FROM Users WHERE UserID=%s AND UserName=%s AND UserPass=%s"
        cursor.execute(query, (user_id, username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            role = user["UserRole"]  # type: ignore
            open_dashboard(role, user_id, username)
        else:
            messagebox.showerror(
                "Login Failed", "Invalid UserID, Username, or Password"
            )


import os
import sys
import subprocess


def open_dashboard(role, user_id, username):
    """Open the respective dashboard and print debug messages."""

    script_map = {
        "Admin": "admin_dashboard.exe",  # Running EXE version
        "Teacher": "teacher_dashboard.exe",
        "Student": "student_dashboard.exe",
    }

    if role in script_map:
        exe_path = os.path.join(os.path.dirname(sys.executable), script_map[role])

        print(f"Trying to open: {exe_path}")  # Debugging

        if os.path.exists(exe_path):
            print(f"File exists: {exe_path}, launching...")
            subprocess.Popen([exe_path, user_id, username])
            sys.exit()  # Close login window
        else:
            print(f"Error: {exe_path} NOT FOUND!")
            messagebox.showerror("Error", f"Dashboard not found: {script_map[role]}")
    else:
        print("Invalid role detected!")
        messagebox.showerror("Error", "Invalid user role. Contact support.")


# Tkinter GUI - Login Window
root = tk.Tk()
root.title("Event Management Login")
root.geometry("400x300")

tk.Label(root, text="User ID:", font=("Arial", 12)).pack(pady=5)
entry_user_id = tk.Entry(root)
entry_user_id.pack()

tk.Label(root, text="Username:", font=("Arial", 12)).pack(pady=5)
entry_username = tk.Entry(root)
entry_username.pack()

tk.Label(root, text="Password:", font=("Arial", 12)).pack(pady=5)
entry_password = tk.Entry(root, show="*")
entry_password.pack()

tk.Button(root, text="Login", command=login).pack(pady=10)

root.mainloop()  # Keep Tkinter running
