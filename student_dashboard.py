import tkinter as tk
from tkinter import messagebox
from tkinter import ttk  # For table display
from db_config import DB_CONFIG
import sys
import subprocess
from tkcalendar import Calendar  # type: ignore
from datetime import datetime
import os


# Get UserID and Username from command-line arguments
user_id = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
STUDENT_USERNAME = sys.argv[2] if len(sys.argv) > 2 else "Student"


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


class StudentDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Dashboard")
        self.root.geometry("700x400")

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
            text="Events",
            command=self.show_events,
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
        """Display the Student Dashboard page."""
        self.clear_frame()
        tk.Label(
            self.content_frame,
            text=f"Welcome, {STUDENT_USERNAME} (UserID: {user_id})",
            font=("Arial", 14),
        ).pack(pady=10)
        tk.Label(self.content_frame, text="Dashboard Page", font=("Arial", 12)).pack(
            pady=20
        )

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

    def show_events(self):
        """Display all available events with registration options."""
        self.clear_frame()
        tk.Label(self.content_frame, text="Available Events", font=("Arial", 14)).pack(
            pady=10
        )

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT EventID, EventName, EventDate, EventVenue FROM Events")
        events = cursor.fetchall()

        if events:
            for event in events:
                event_id = event[0]  # type: ignore
                is_registered = self.check_registration(event_id)
                responsibility_var = tk.StringVar(value="Participant")

                frame = tk.Frame(self.content_frame)
                ttk.Label(frame, text=event[1]).grid(row=0, column=0, padx=5)  # type: ignore
                ttk.Label(frame, text=event[2]).grid(row=0, column=1, padx=5)  # type: ignore
                ttk.Label(frame, text=event[3]).grid(row=0, column=2, padx=5)  # type: ignore

                dropdown = ttk.Combobox(
                    frame,
                    textvariable=responsibility_var,
                    values=["Participant", "Organizer"],
                    state="readonly",
                )
                dropdown.grid(row=0, column=3, padx=5)

                if is_registered:
                    btn = tk.Button(
                        frame,
                        text="Already Registered",
                        state="disabled",
                        bg="#D3D3D3",
                        fg="black",
                    )  # Light Gray
                else:
                    btn = tk.Button(
                        frame,
                        text="Register",
                        command=lambda e=event_id, r=responsibility_var: self.register_event(
                            e, r
                        ),
                    )

                btn.grid(row=0, column=4, padx=5)
                frame.pack(fill="x", padx=10, pady=2)

        else:
            tk.Label(
                self.content_frame, text="No events available.", font=("Arial", 12)
            ).pack(pady=10)

        conn.close()

    def show_my_events(self):
        """Display all events the student has registered for."""
        self.clear_frame()
        tk.Label(
            self.content_frame, text="My Registered Events", font=("Arial", 14)
        ).pack(pady=10)

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT E.EventID, E.EventName, E.EventDate, E.EventVenue, EP.Responsibility "
            "FROM Events E JOIN EventParticipation EP ON E.EventID = EP.EventID "
            "WHERE EP.UserID = %s",
            (user_id,),
        )
        events = cursor.fetchall()
        conn.close()

        if events:
            tree = ttk.Treeview(
                self.content_frame,
                columns=("EventID", "EventName", "EventDate", "EventVenue", "Role"),
                show="headings",
            )
            tree.heading("EventID", text="ID")
            tree.heading("EventName", text="Event Name")
            tree.heading("EventDate", text="Date")
            tree.heading("EventVenue", text="Venue")
            tree.heading("Role", text="Role")

            for event in events:
                tree.insert("", "end", values=event)  # type: ignore

            tree.pack(pady=10)
        else:
            tk.Label(
                self.content_frame,
                text="You have not registered for any events yet.",
                font=("Arial", 12),
            ).pack(pady=10)

    def check_registration(self, event_id):
        """Check if the student is already registered for an event."""
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM EventParticipation WHERE EventID = %s AND UserID = %s",
            (event_id, user_id),
        )
        result = cursor.fetchone()
        conn.close()
        return result is not None  # Returns True if already registered

    def register_event(self, event_id, responsibility_var):
        """Register the student for an event."""
        responsibility = responsibility_var.get()

        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO EventParticipation (EventID, UserID, Responsibility) VALUES (%s, %s, %s)",
                (event_id, user_id, responsibility),
            )
            conn.commit()
            conn.close()

            messagebox.showinfo(
                "Success", "You have successfully registered for the event!"
            )
            self.show_events()  # Refresh event list after registration
        except Exception as e:
            messagebox.showerror("Error", f"Failed to register: {e}")

    def clear_frame(self):
        """Clear the content frame."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()


# Run Student Dashboard
if __name__ == "__main__":
    root = tk.Tk()
    app = StudentDashboard(root)
    root.mainloop()
