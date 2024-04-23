# create_run_tab.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os

def create_run_tab(tab_control, conn):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Run Script')

    # Function to run the selected script
    def run_script():
        # Get selected script and parameters
        selected_script = script_combobox.get()
        parameters = parameter_entry.get("1.0", tk.END).strip()

        # Check if a script is selected
        if not selected_script:
            messagebox.showerror("Error", "Please select a script to run.")
            return

        # Extract script path from the selected script
        script_path = selected_script.split(" : ")[1].strip()

        # Check if the script exists
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script '{selected_script}' not found.")
            return

        # Run the script with parameters
        try:
            output = subprocess.check_output([script_path, parameters], universal_newlines=True)
            output_text.insert(tk.END, output)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Failed to run script: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    # Fetch scripts from database
    try:
        cursor = conn.execute("SELECT name, path FROM SCRIPTS")
        scripts = [f"{row[0]} : {row[1]}" for row in cursor.fetchall()]
    except Exception as e:
        messagebox.showerror("Error", f"Failed to fetch scripts from database: {e}")
        scripts = []

    # Create widgets
    script_label = tk.Label(tab, text="Select Script:")
    script_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    script_combobox = ttk.Combobox(tab, values=scripts, state="readonly", width=50)
    script_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    parameter_label = tk.Label(tab, text="Parameters:")
    parameter_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    parameter_entry = tk.Text(tab, width=50, height=5)
    parameter_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    run_button = tk.Button(tab, text="Run", command=run_script)
    run_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)

    output_text = tk.Text(tab, wrap="word", width=80, height=20)
    output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    # Function to update parameters when a script is selected
    def update_parameters(event):
        selected_script = script_combobox.get()
        if selected_script:
            parameters = selected_script.split(" : ")[1].strip()
            parameter_entry.delete("1.0", tk.END)
            parameter_entry.insert(tk.END, parameters)

    script_combobox.bind("<<ComboboxSelected>>", update_parameters)

