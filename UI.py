#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import simulation

# Define the function to execute when the button is pressed
def run_Trim():
    try:
        # Get the values from the entry fields
        velocity = float(entry1.get().strip())
        gamma = float(entry2.get().strip())
        
        # Call your function with the provided values
        trimParams = simulation.Trim(velocity, gamma)
        
        # Display the result in a messagebox
        thrust_label.config(text=f"Thrust: {round(trimParams.thrust, 4)}")
        delta_label.config(text=f"Elevator angle (delta): {round(trimParams.delta, 4)}")
    except ValueError:
        # Handle the case where a non-numeric value is entered
        messagebox.showerror("Error", "Please enter numeric values.")

def run_Simulation():
    try:
        # Get values
        velocity = float(entry1.get().strip())
        gamma = float(entry2.get().strip())
        pitchTime = float(entry3.get().strip())
        climbTime = float(entry4.get().strip())
        elevatorChange = float(entry5.get().strip())
        thrustChange = float(entry6.get().strip())
        
        sim = simulation.Simulation(velocity, gamma, pitchTime, climbTime, elevatorChange, thrustChange, 500)
        
        fig = sim.Display(sim.data)
        canvas = FigureCanvasTkAgg(fig, master=output_frame)
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)  # Use pack geometry manager
        
    except ValueError:
        # Handle the case where a non-numeric value is entered
        messagebox.showerror("Error", "Please enter numeric values.")

# Create the main application window
root = tk.Tk()
root.title("User Interface")

# Create input frame
input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

# Create output frame
output_frame = ttk.Frame(root)
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

# Create labels and entry fields for user input in the input frame
ttk.Label(input_frame, text="Velocity (m/s):").grid(row=0, column=0)
entry1 = ttk.Entry(input_frame)
entry1.grid(row=0, column=1)

ttk.Label(input_frame, text="Path angle (rad):").grid(row=1, column=0)
entry2 = ttk.Entry(input_frame)
entry2.grid(row=1, column=1)

# Create a button to run Trim
run_button = ttk.Button(input_frame, text="Get Trim Parameters", command=run_Trim)
run_button.grid(row=2, column=0, columnspan=2, pady=10)

# Create labels to display the output in the input frame
thrust_label = ttk.Label(input_frame, text="")
thrust_label.grid(row=3, column=0, columnspan=2)

delta_label = ttk.Label(input_frame, text="")
delta_label.grid(row=4, column=0, columnspan=2)

# Add labels and entry fields for simulation parameters in the input frame
ttk.Label(input_frame, text="Pitch time:").grid(row=5, column=0)
entry3 = ttk.Entry(input_frame)
entry3.grid(row=5, column=1)

ttk.Label(input_frame, text="Climb time:").grid(row=6, column=0)
entry4 = ttk.Entry(input_frame)
entry4.grid(row=6, column=1)

ttk.Label(input_frame, text="Elevator change (%):").grid(row=7, column=0)
entry5 = ttk.Entry(input_frame)
entry5.grid(row=7, column=1)

ttk.Label(input_frame, text="Thrust change (%):").grid(row=8, column=0)
entry6 = ttk.Entry(input_frame)
entry6.grid(row=8, column=1)

# Create a button to run the simulation in the input frame
run_button = ttk.Button(input_frame, text="Simulate", command=run_Simulation)
run_button.grid(row=9, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
