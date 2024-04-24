# create_run_tab.py

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess
import os
import threading
import queue  


def create_run_tab(tab_control, fetch_scripts_func, status_bar, root):
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Run Script')

    # Function to execute the script in a separate thread
    def execute_script(script_path, parameters, output_queue):
        try:
            # Execute the script and capture the output
            process = subprocess.Popen([script_path, parameters], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            # Check if there's any error output
            if stderr:
                output_queue.put((False, stderr.decode('utf-8')))
            else:
                output_queue.put((True, stdout.decode('utf-8')))
        except Exception as e:
            output_queue.put((False, f"An unexpected error occurred: {e}"))

    # Function to run the selected script
    def run_script(root):  # Pass root as an argument
        # Disable the run button
        run_button.config(state=tk.DISABLED)

        # Get selected script and parameters
        selected_script = script_combobox.get()
        parameters = parameter_entry.get("1.0", tk.END).strip()

        # Check if a script is selected
        if not selected_script:
            messagebox.showerror("Error", "Please select a script to run.")
            run_button.config(state=tk.NORMAL)  # Re-enable the run button
            return

        # Extract script name and path from the selected script
        script_name, script_relative_path = selected_script.split(" : ")
        script_path = os.path.join(os.getcwd(), "scripts", script_relative_path.strip())

        # Check if the script exists
        if not os.path.exists(script_path):
            messagebox.showerror("Error", f"Script '{script_name}' not found at path: {script_path}")
            run_button.config(state=tk.NORMAL)  # Re-enable the run button
            return

        # Construct the command to be executed
        command = f"{script_path} {parameters}"

        # Update status bar with the command being executed
        status_bar.config(text=f"Running command: {command}")

        # Create a queue to receive the output from the thread
        output_queue = queue.Queue()

        # Start a thread to execute the script
        thread = threading.Thread(target=execute_script, args=(script_path, parameters, output_queue))
        thread.start()

        # Define a function to handle the output after the thread finishes
        def handle_output():
            thread.join()

            success, output = output_queue.get()

            if not success:
                messagebox.showerror("Error", f"Failed to run script '{script_name}': {output}")
            else:
                output_text.insert(tk.END, output)

            status_bar.config(text="Done")

            run_button.config(state=tk.NORMAL)

        # Call the function to handle the output
        root.after(100, handle_output)  # Schedule it to run after a short delay



    
    # Fetch scripts from database
    def update_scripts():
        nonlocal scripts  # Define scripts as nonlocal to modify it
        try:
            scripts = fetch_scripts_func()
            script_combobox["values"] = scripts
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch scripts from database: {e}")

    # Function to update parameters when a script is selected
    def update_parameters(event):
        selected_script = script_combobox.get()
        if selected_script:
            parameters = selected_script.split(" : ")[1].strip()
            parameter_entry.delete("1.0", tk.END)
            parameter_entry.insert(tk.END, parameters)

    # Initialize scripts variable
    scripts = []
    
    # Create widgets
    script_label = tk.Label(tab, text="Select Script:")
    script_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)

    # Define script_combobox after update_scripts is defined
    script_combobox = ttk.Combobox(tab, values=scripts, state="readonly", width=50)
    script_combobox.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

    parameter_label = tk.Label(tab, text="Parameters:")
    parameter_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)

    parameter_entry = tk.Text(tab, width=50, height=5)
    parameter_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

    run_button = tk.Button(tab, text="Run", command=lambda: run_script(root))
    run_button.grid(row=2, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)

    output_text = tk.Text(tab, wrap="word", width=80, height=20)
    output_text.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky=tk.W)

    update_scripts()  # Update scripts initially
    
    script_combobox.bind("<<ComboboxSelected>>", update_parameters)

    # Bind event to update scripts when the tab is selected
    tab.bind("<Visibility>", lambda event: update_scripts())
