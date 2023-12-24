import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import simulation

def run_Trim():
    try:
        velocity = float(entry1.get().strip())
        gamma = np.deg2rad(float(entry2.get().strip()))
        
        if velocity > 343 or gamma > np.deg2rad(89) or velocity < 30 or gamma < np.deg2rad(-89):
           messagebox.showerror("Error", "Values out of range \n  Velocity from 30 to 343 m/s  \n gamma from -89 to 89 degrees ") 
        else:
            trimParams = simulation.Trim(velocity, gamma)
        
        thrust_label.config(text=f"Thrust (N): {round(trimParams.thrust, 4)}")
        delta_label.config(text=f"Elevator angle (deg): {round(np.rad2deg(trimParams.delta),4)}")
    except ValueError:
        messagebox.showerror("Error", "Please enter numeric values.")

def clear_output_frame():
    for widget in output_frame.winfo_children():
        widget.destroy()

def run_Simulation():
    clear_output_frame()
    
    try:
        velocity = float(entry1.get().strip())
        gamma = np.deg2rad(float(entry2.get().strip()))
        initialAltitude = float(entry3.get().strip())
        simulationRunTime = float(entry4.get().strip())
        
        input_values_box1 = entry5.get()  
        input_values_box2 = entry6.get()  
        input_values_box3 = entry7.get()  
        
        values_box1 = input_values_box1.split(',')
        values_box2 = input_values_box2.split(',')
        values_box3 = input_values_box3.split(',')
        
        values_box1 = [float(value.strip()) for value in values_box1]
        values_box2 = [float(value.strip()) for value in values_box2]
        values_box3 = [float(value.strip()) for value in values_box3]
        
        resultList = [(values_box1[i], np.deg2rad(values_box2[i]), values_box3[i]) for i in range(min(len(values_box1), len(values_box2), len(values_box3)))]
        if velocity <= 0:
            messagebox.showerror("Error", "Values out of range \n Velocity must be > 0 m/s \n Not displaying graphs.")
        else:
            if velocity > 200 or gamma > np.deg2rad(89) or velocity < 65 or gamma < np.deg2rad(-89):
               messagebox.showerror("Error", "Flow separation is not simulated, these values may lead to unstable simulation")  
               
            sim = simulation.Simulation(velocity, gamma, simulationRunTime, initialAltitude, resultList)
            
            fig = sim.Display_Sim(sim.data)
            canvas = FigureCanvasTkAgg(fig, master=output_frame)
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    except ValueError:
        messagebox.showerror("Error", "Please enter numeric values.")

root = tk.Tk()
root.title("Aeroplane Simulation")

input_frame = ttk.Frame(root)
input_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

output_frame = ttk.Frame(root)
output_frame.grid(row=0, column=1, padx=10, pady=10, sticky="e")

ttk.Label(input_frame, text="Velocity (m/s):").grid(row=0, column=0)
entry1 = ttk.Entry(input_frame)
entry1.grid(row=0, column=1)

ttk.Label(input_frame, text="Path angle (deg):").grid(row=1, column=0)
entry2 = ttk.Entry(input_frame)
entry2.grid(row=1, column=1)

run_button = ttk.Button(input_frame, text="Get Trim Parameters", command=run_Trim)
run_button.grid(row=2, column=0, columnspan=2, pady=10)

thrust_label = ttk.Label(input_frame, text="")
thrust_label.grid(row=3, column=0, columnspan=2)

delta_label = ttk.Label(input_frame, text="")
delta_label.grid(row=4, column=0, columnspan=2)

ttk.Label(input_frame, text="Initial altitude (m):").grid(row=5, column=0)
entry3 = ttk.Entry(input_frame)
entry3.grid(row=5, column=1)

ttk.Label(input_frame, text="Simulation run time (s):").grid(row=6, column=0)
entry4 = ttk.Entry(input_frame)
entry4.grid(row=6, column=1)

ttk.Label(input_frame, text="Input time (s):").grid(row=7, column=0)
entry5 = ttk.Entry(input_frame)
entry5.grid(row=7, column=1)

ttk.Label(input_frame, text="Change in elevator angle (deg):").grid(row=8, column=0)
entry6 = ttk.Entry(input_frame)
entry6.grid(row=8, column=1)

ttk.Label(input_frame, text="Change in Thrust (N):").grid(row=9, column=0)
entry7 = ttk.Entry(input_frame)
entry7.grid(row=9, column=1)

run_button = ttk.Button(input_frame, text="Simulate", command=run_Simulation)
run_button.grid(row=10, column=0, columnspan=2, pady=10)

instructions_text = "Input initial velocity and path angle for trim conditions.\nSimulation parameters entered in the lower 5 boxes. ""Input time"" (times after start at which changes are executed) are entered as comma seperated integers.\nChanges in elevator and thrust are also comma seperated and are absolute step changes e.g. (-0.1,0,0.1) is change by -0.1 deg, dont change, change by 0.1 deg.\nIf change lists are unequal in length, the length of the shortest length is used.\n\nClick 'simulate' to display or reset graphs."
instructions_label = ttk.Label(input_frame, text=instructions_text, wraplength=300)
instructions_label.grid(row=12, column=0, columnspan=2, pady=10)

root.mainloop()
