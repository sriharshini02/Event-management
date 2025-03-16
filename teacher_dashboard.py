import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For table display
from tkcalendar import Calendar  # type: ignore
from db_config import DB_CONFIG
from datetime import datetime
from add_student import add_student_window
import sys
import subprocess
from create_event import create_event_window
import os


# Get UserID and Username from command-line arguments
user_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
TEACHER_USERNAME = sys.argv[2] if len(sys.argv) > 2 else "Teacher"


def connect_db():
    """Connect to the database."""
    import mysql.connector

    return mysql.connector.connect(**DB_CONFIG)


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


class TeacherDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Teacher Dashboard")
        self.root.geometry("600x400")

        # Navbar
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
            text="Create Events",
            command=self.show_create_events,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)
        tk.Button(
            self.navbar,
            text="All Events",
            command=self.show_all_events,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)
        tk.Button(
            self.navbar,
            text="My Events",
            command=self.show_my_events,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)
        tk.Button(
            self.navbar,
            text="Provide Feedback",
            command=self.show_provide_feedback,
            bg="#444",
            fg="white",
            relief="flat",
            padx=10,
        ).pack(side="left", padx=5, pady=5)
        tk.Button(
            self.navbar,
            text="Add Students",
            command=self.show_add_students,
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
        ).pack(pady=10)

        self.content_frame = tk.Frame(root)
        self.content_frame.pack(fill="both", expand=True, pady=10)

        # Default view
        self.show_dashboard()

    def show_dashboard(self):
        """Display the Dashboard page with a calendar."""
        self.clear_frame()
        tk.Label(
            self.content_frame,
            text=f"Welcome, Teacher ({TEACHER_USERNAME})",
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

    def show_create_events(self):
        """Open Create Event Window."""
        create_event_window(user_id)

    def show_all_events(self):
        """Display all events in the content frame."""
        self.clear_frame()
        tk.Label(self.content_frame, text="All Events", font=("Arial", 14)).pack(
            pady=10
        )

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EventID, EventName, EventDate, EventVenue FROM Events")
        events = cursor.fetchall()
        conn.close()

        if events:
            tree = ttk.Treeview(
                self.content_frame,
                columns=("EventID", "EventName", "EventDate", "EventVenue"),
                show="headings",
            )
            tree.heading("EventID", text="ID")
            tree.heading("EventName", text="Event Name")
            tree.heading("EventDate", text="Date")
            tree.heading("EventVenue", text="Venue")

            for event in events:
                tree.insert("", "end", values=event)  # type: ignore

            tree.pack(pady=10)
        else:
            tk.Label(
                self.content_frame, text="No events available.", font=("Arial", 12)
            ).pack(pady=10)

    def show_my_events(self):
        """Display events created by this teacher in the content frame."""
        self.clear_frame()
        tk.Label(self.content_frame, text="My Events", font=("Arial", 14)).pack(pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT EventID, EventName, EventDate, EventVenue FROM Events WHERE UserID = %s",
            (user_id,),
        )
        events = cursor.fetchall()
        conn.close()

        if events:
            tree = ttk.Treeview(
                self.content_frame,
                columns=("EventID", "EventName", "EventDate", "EventVenue"),
                show="headings",
            )
            tree.heading("EventID", text="ID")
            tree.heading("EventName", text="Event Name")
            tree.heading("EventDate", text="Date")
            tree.heading("EventVenue", text="Venue")

            for event in events:
                tree.insert("", "end", values=event)  # type: ignore

            tree.pack(pady=10)
        else:
            tk.Label(
                self.content_frame,
                text="You haven't created any events yet.",
                font=("Arial", 12),
            ).pack(pady=10)

    def show_provide_feedback(self):
        """Placeholder for Provide Feedback page."""
        self.clear_frame()
        tk.Label(
            self.content_frame,
            text="Provide Feedback Page (Coming Soon)",
            font=("Arial", 14),
        ).pack(pady=20)

    def show_add_students(self):
        """Open the Add Student window."""
        add_student_window(self.root)

    def clear_frame(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


# Run Teacher Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = TeacherDashboard(root)
    root.mainloop()
