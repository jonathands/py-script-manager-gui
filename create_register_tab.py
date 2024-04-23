import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
import json
import sqlite3
import shutil

def create_register_tab(tab_control, conn, status_bar):  # Add status_bar parameter
    tab = ttk.Frame(tab_control)
    tab_control.add(tab, text='Register Script')
    
    # Function to handle file upload
    def browse_file():
        filename = filedialog.askopenfilename()
        if filename:
            file_entry.delete(0, tk.END)
            file_entry.insert(0, filename)
    
    # Function to add parameter field
    def add_parameter():
        param_entry = tk.Entry(parameters_frame)
        param_entry.pack(fill=tk.X, padx=5, pady=2)
        parameter_entries.append(param_entry)
    
    # Function to save script
    def save_script():
        # Get values from fields
        name = name_entry.get()
        file_path = file_entry.get()
        parameters = [entry.get() for entry in parameter_entries]
        
        # Perform validation
        if not name:
            tk.messagebox.showerror("Error", "Name field is mandatory.")
            return
        if not file_path:
            tk.messagebox.showerror("Error", "File field is mandatory.")
            return
        
        # Copy file to scripts folder
        if not os.path.exists("scripts"):
            os.makedirs("scripts")
        filename = os.path.basename(file_path)
        destination = os.path.join("scripts", filename)
        shutil.copyfile(file_path, destination)  # Copy file to destination
        
        # Save to database
        try:
            conn.execute("INSERT INTO SCRIPTS (name, path, parameters) VALUES (?, ?, ?)",
                         (name, filename, json.dumps(parameters)))  # Save filename instead of full path
            conn.commit()
            
            # Update status bar
            status_bar.config(text="Script added successfully.")
            
            tk.messagebox.showinfo("Success", "Script saved successfully.")
            
            # Clear form fields
            name_entry.delete(0, tk.END)
            file_entry.delete(0, tk.END)
            for entry in parameter_entries:
                entry.delete(0, tk.END)
        except sqlite3.Error as e:
            # Update status bar
            status_bar.config(text=f"Failed to save script: {e}")
            
            tk.messagebox.showerror("Error", f"Failed to save script: {e}")
        except Exception as e:
            # Update status bar
            status_bar.config(text=f"An unexpected error occurred: {e}")
            
            tk.messagebox.showerror("Error", f"An unexpected error occurred: {e}")
    
    # Create widgets
    name_label = tk.Label(tab, text="Name:")
    name_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
    name_entry = tk.Entry(tab)
    name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
    
    file_label = tk.Label(tab, text="File:")
    file_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
    file_entry = tk.Entry(tab)
    file_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
    browse_button = tk.Button(tab, text="Browse", command=browse_file)
    browse_button.grid(row=1, column=2, padx=5, pady=5, sticky=tk.W)
    
    parameters_label = tk.Label(tab, text="Parameters:")
    parameters_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)
    parameters_frame = tk.Frame(tab)
    parameters_frame.grid(row=2, column=1, columnspan=2, padx=5, pady=5, sticky=tk.W)
    add_parameter_button = tk.Button(tab, text="Add Parameter", command=add_parameter)
    add_parameter_button.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
    
    # Button to save script
    save_button = tk.Button(tab, text="Save", command=save_script)
    save_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky=tk.W)
    
    # List to store parameter entry widgets
    parameter_entries = []

