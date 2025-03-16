import tkinter as tk
from tkinter import messagebox
import mysql.connector
from db_config import DB_CONFIG


def connect_db():

    conn = mysql.connector.connect(**DB_CONFIG)
    return conn


def update_event():
    event_id = entry_event_id.get()
    new_event_name = entry_new_event.get()

    if not event_id or not new_event_name:
        messagebox.showerror("Error", "All fields are required!")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE Events SET EventName = %s WHERE EventID = %s",
        (new_event_name, event_id),
    )
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Event updated successfully!")
    edit_event_window.destroy()


def open_edit_events_window():
    global edit_event_window, entry_event_id, entry_new_event

    edit_event_window = tk.Toplevel()
    edit_event_window.title("Edit Events")
    edit_event_window.geometry("300x200")

    tk.Label(edit_event_window, text="Event ID").pack()
    entry_event_id = tk.Entry(edit_event_window)
    entry_event_id.pack()

    tk.Label(edit_event_window, text="New Event Name").pack()
    entry_new_event = tk.Entry(edit_event_window)
    entry_new_event.pack()

    tk.Button(edit_event_window, text="Update", command=update_event).pack(pady=10)
