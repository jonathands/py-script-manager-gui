# main.py

import tkinter as tk
from tkinter import ttk
import sqlite3
from pathlib import Path
import json
from create_run_tab import create_run_tab
from create_register_tab import create_register_tab
from script_output import create_output_tab

def connect_to_database(root, status_bar):
    status_bar.config(text="Connecting to database...")
    root.update_idletasks()
    
    database_path = Path("scriptrun.db")
    try:
        if database_path.exists():
            conn = sqlite3.connect("scriptrun.db")
            status_bar.config(text="Connected to existing database.")
        else:
            conn = sqlite3.connect("scriptrun.db")
            status_bar.config(text="Created and connected to new database.")
            conn.execute("CREATE TABLE IF NOT EXISTS SCRIPTS (id INTEGER PRIMARY KEY, name TEXT, path TEXT, parameters TEXT)")
            conn.commit()
    except sqlite3.Error as e:
        status_bar.config(text=f"Failed connecting to database: {e}")
    else:
        return conn

def on_close_window(root, conn):
    if conn:
        conn.close()
    root.destroy()

def fetch_scripts_from_database():
    try:
        conn = sqlite3.connect("scriptrun.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, path FROM SCRIPTS")
        scripts = [f"{row[0]} : {row[1]}" for row in cursor.fetchall()]
        conn.close()
        return scripts
    except Exception as e:
        print(f"Error fetching scripts from database: {e}")
        return []

def main():
    root = tk.Tk()
    root.title("Python Script Manager")
    root.geometry("800x600")
    
    # Create status bar
    status_bar = tk.Label(root, text="Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
    status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    # Connect to the SQLite database
    conn = connect_to_database(root, status_bar)
    
    # Close the database connection and window properly
    root.protocol("WM_DELETE_WINDOW", lambda: on_close_window(root, conn))
    
    # Create tab control
    tab_control = ttk.Notebook(root)
    tab_control.pack(expand=1, fill="both")
    
    # Populate tabs
    create_run_tab(tab_control, fetch_scripts_from_database, status_bar, root)
    create_register_tab(tab_control, conn, status_bar)
    create_output_tab(tab_control, 'xxx', status_bar)
    
    root.mainloop()

if __name__ == "__main__":
    main()

