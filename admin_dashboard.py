import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkcalendar import Calendar  # type: ignore
from add_teacher import open_add_teacher_window
from edit_events import open_edit_events_window
from db_config import DB_CONFIG
from datetime import datetime
import sys
import subprocess

# Get UserID and Username from command-line arguments
user_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
ADMIN_USERNAME = sys.argv[2] if len(sys.argv) > 2 else "Admin"


def connect_db():
    """Connect to the database."""
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


import os
import sys
import subprocess


def logout():
    root.destroy()  # Close the current dashboard window

    if getattr(sys, "frozen", False):
        # Running as an EXE
        exe_path = os.path.join(os.path.dirname(sys.executable), "event_management.exe")
        print(f"Logging out: Launching {exe_path}")  # Debugging
        subprocess.Popen([exe_path])
    else:
        # Running as a Python script
        print("Logging out: Relaunching login.py")  # Debugging
        subprocess.Popen([sys.executable, "login.py"])

    sys.exit()  # Ensure current process fully exits


class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("500x400")

        # Navbar frame
        self.navbar = tk.Frame(root, bg="#333")
        self.navbar.pack(fill="x")

        tk.Button(
            self.navbar,
            text="Dashboard",
            command=self.show_dashboard,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            self.navbar,
            text="Edit Events",
            command=self.show_edit_events,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            self.navbar,
            text="Add Teacher",
            command=self.show_add_teacher,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)

        tk.Button(
            root,
            text="Logout",
            command=logout,
            fg="white",
            bg="red",
            font=("Arial", 12),
        ).pack(pady=20)

        # Main content frame
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        # Default view
        self.show_dashboard()

    def show_dashboard(self):
        """Display the Dashboard page with the calendar."""
        self.clear_frame()
        tk.Label(
            self.content_frame,
            text=f"Welcome, Admin ({ADMIN_USERNAME})",
            font=("Arial", 14),
        ).pack(pady=10)

        cal = Calendar(self.content_frame, selectmode="day", year=2025, month=3, day=15)
        cal.pack(pady=10)

        def fetch_events():
            selected_date = cal.get_date()
            formatted_date = datetime.strptime(selected_date, "%m/%d/%y").strftime(
                "%Y-%m-%d"
            )

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "SELECT EventName FROM Events WHERE EventDate = %s", (formatted_date,)
            )
            events = cursor.fetchall()
            conn.close()

            event_list = (
                "\n".join([event[0] for event in events])  # type: ignore
                if events
                else "No events on this date."
            )
            messagebox.showinfo("Events", f"Events on {selected_date}:\n{event_list}")

        tk.Button(self.content_frame, text="Show Events", command=fetch_events).pack(
            pady=5
        )

    def show_edit_events(self):
        """Opens the edit events window."""
        open_edit_events_window()

    def show_add_teacher(self):
        """Opens the add teacher window."""
        open_add_teacher_window()

    def clear_frame(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


# Run Admin Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = AdminDashboard(root)
    root.mainloop()
