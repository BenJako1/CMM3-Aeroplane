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
        initialAltitude = float(entry3.get().strip())
        simulationRunTime = float(entry4.get().strip())
        
        # Assuming you have already retrieved the input values from the boxes as strings
        input_values_box1 = entry5.get()  # Replace entry_box1 with the actual Tkinter Entry widget
        input_values_box2 = entry6.get()  # Replace entry_box2 with the actual Tkinter Entry widget
        input_values_box3 = entry7.get()  # Replace entry_box3 with the actual Tkinter Entry widget
        
        # Split the input values into separate elements
        values_box1 = input_values_box1.split(',')
        values_box2 = input_values_box2.split(',')
        values_box3 = input_values_box3.split(',')
        
        # Convert the values to integers (or floats if needed)
        values_box1 = [float(value.strip()) for value in values_box1]
        values_box2 = [float(value.strip()) for value in values_box2]
        values_box3 = [float(value.strip()) for value in values_box3]
        
        # Create a list of tuples
        resultList = [(values_box1[i], values_box2[i], values_box3[i]) for i in range(min(len(values_box1), len(values_box2), len(values_box3)))]
        
        sim = simulation.Simulation(velocity, gamma, initialAltitude, simulationRunTime, resultList)
        
        fig = sim.Display_Sim(sim.data)
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
ttk.Label(input_frame, text="Inital altitude (m):").grid(row=5, column=0)
entry3 = ttk.Entry(input_frame)
entry3.grid(row=5, column=1)

ttk.Label(input_frame, text="Simulation run time (s):").grid(row=6, column=0)
entry4 = ttk.Entry(input_frame)
entry4.grid(row=6, column=1)

ttk.Label(input_frame, text="Time changes (s):").grid(row=7, column=0)
entry5 = ttk.Entry(input_frame)
entry5.grid(row=7, column=1)

ttk.Label(input_frame, text="Elevator changes (rad):").grid(row=8, column=0)
entry6 = ttk.Entry(input_frame)
entry6.grid(row=8, column=1)

ttk.Label(input_frame, text="Thrust changes (N):").grid(row=9, column=0)
entry7 = ttk.Entry(input_frame)
entry7.grid(row=9, column=1)

# Create a button to run the simulation in the input frame
run_button = ttk.Button(input_frame, text="Simulate", command=run_Simulation)
run_button.grid(row=10, column=0, columnspan=2, pady=10)

# Start the Tkinter event loop
root.mainloop()
