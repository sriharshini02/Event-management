import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry  # type: ignore
import mysql.connector
from db_config import DB_CONFIG
from datetime import datetime


def connect_db():
    """Connect to the MySQL database."""
    return mysql.connector.connect(**DB_CONFIG)


def create_event_window(teacher_id):
    """Open the Create Event window."""
    event_window = tk.Toplevel()
    event_window.title("Create Event")
    event_window.geometry("400x400")

    # Labels and Entry Fields
    tk.Label(event_window, text="Event Name:").pack()
    entry_event_name = tk.Entry(event_window)
    entry_event_name.pack()

    tk.Label(event_window, text="Event Date (YYYY-MM-DD):").pack()
    entry_event_date = DateEntry(event_window, date_pattern="yyyy-mm-dd")
    entry_event_date.pack()

    tk.Label(event_window, text="Start Time (HH:MM:SS):").pack()
    entry_start_time = tk.Entry(event_window)
    entry_start_time.pack()

    tk.Label(event_window, text="End Time (HH:MM:SS):").pack()
    entry_end_time = tk.Entry(event_window)
    entry_end_time.pack()

    tk.Label(event_window, text="Venue:").pack()
    entry_venue = tk.Entry(event_window)
    entry_venue.pack()

    tk.Label(event_window, text="Teacher ID (Auto-filled):").pack()
    entry_teacher_id = tk.Entry(event_window)
    entry_teacher_id.insert(0, teacher_id)  # Pre-fill with teacher ID
    entry_teacher_id.config(state="disabled")  # Disable editing
    entry_teacher_id.pack()

    def submit_event():
        """Insert event into the database."""
        event_name = entry_event_name.get()
        event_date = entry_event_date.get()
        start_time = entry_start_time.get()
        end_time = entry_end_time.get()
        venue = entry_venue.get()

        if not all([event_name, event_date, start_time, end_time, venue]):
            messagebox.showerror(
                "Error", "All fields are required!", parent=event_window
            )
            return

        try:
            conn = connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO Events (EventName, EventDate, EventStartTime, EventEndTime, EventVenue, UserID) VALUES (%s, %s, %s, %s, %s, %s)",
                (event_name, event_date, start_time, end_time, venue, teacher_id),
            )

            conn.commit()
            conn.close()
            messagebox.showinfo(
                "Success", "Event created successfully!", parent=event_window
            )
            event_window.destroy()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error: {err}", parent=event_window)

    tk.Button(event_window, text="Create Event", command=submit_event).pack(pady=10)
    tk.Button(event_window, text="Close", command=event_window.destroy).pack()
