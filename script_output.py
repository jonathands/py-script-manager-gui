# script_output.py

import tkinter as tk
from tkinter import ttk

def create_output_tab(tab_control, output_text, status_bar):
    # Create a new tab
    output_tab = ttk.Frame(tab_control)
    tab_control.add(output_tab, text="Script Output")

    # Create a scrolled text widget to display the output
    output_text_widget = tk.Text(output_tab, wrap="word", width=80, height=20)
    output_text_widget.pack(expand=True, fill="both")

    # Insert the output text into the text widget
    output_text_widget.insert(tk.END, output_text)

    # Disable editing of the output text
    output_text_widget.configure(state="disabled")

