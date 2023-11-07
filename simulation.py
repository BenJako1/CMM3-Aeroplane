# -*- coding: utf-8 -*-
"""
Created on Sun Nov  5 16:05:39 2023

@author: mauri + nick 
https://tkdocs.com/tutorial/windows.html
"""

# importing modules
import constants 
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import integrate
from scipy.optimize import newton
from tkinter import *
from tkinter import ttk

#------------------------------------------------------------------------------
#imported from forms cos idk how to pull values from the interface from another module.
#define the formulas of the aircraft dynamics
#imports variables from the 'constants'module so that it recognizes variables such as CL0, CLa, and so on

def Coefficient_of_Lift(a, d):
    return constants.CL0 + constants.CLa * np.rad2deg(a) + constants.CLde * np.rad2deg(d)

def Coefficient_of_Moment(a, d):
    return constants.CM0 + constants.CMa * np.rad2deg(a) + constants.CMde * np.rad2deg(d)

def Coefficient_of_Drag(a, d):
    return constants.CD0 + constants.K * (Coefficient_of_Lift(a, d))**2

def Lift(a, d, velocity):
    return (0.5 * constants.air_density * velocity**2 * constants.wing_surface *
            Coefficient_of_Lift(a, d))

def Drag(a, d, velocity):
    return (0.5 * constants.air_density * velocity**2 * constants.wing_surface *
            Coefficient_of_Drag(a, d))

def Moment(a, d, velocity):
    return (0.5 * constants.air_density * velocity**2 * constants.wing_surface *
           constants.cbar * Coefficient_of_Moment(a, d))

def Engine_Thrust(alpha, delta, theta, velocity):
    return (Drag(alpha, delta, velocity) * np.cos(alpha) - Lift(alpha, delta, velocity) * np.sin(alpha) + constants.mass * constants.gravity * np.sin(theta))


#Here we are defining a function for the trim conditions 
def Trim():
    
    #calling values from the interface inputs
    velocity=float(velocity_entry.get())
    gamma=float(gamma_entry.get())
    
    def alpha_trim_func(alpha):
        alpha_deg = np.rad2deg(alpha)
        delta_deg = -(constants.CM0 + constants.CMa * alpha_deg) / constants.CMde

        CL = constants.CL0 + (constants.CLa * alpha_deg) + (constants.CLde * delta_deg)
        CD = constants.CD0 + constants.K * (CL**2)

        Lift_component = 0.5 * constants.air_density * (velocity**2) * constants.wing_surface * CL
        Drag_component = 0.5 * constants.air_density * (velocity**2) * constants.wing_surface * CD
        # Print intermediate values
        
        return (-Lift_component * np.cos(alpha) - Drag_component * np.sin(alpha) + constants.mass * constants.gravity * np.cos(alpha + gamma))
   
    # Solve for alpha and delta
    initial_guess = 0.01  # Provide an initial guess
    alpha = newton(alpha_trim_func, initial_guess)
    delta = np.deg2rad(-(constants.CM0 + constants.CMa * np.rad2deg(alpha)) / constants.CMde)
    
    # Calculating other variables to output
    theta = alpha + gamma
    ub = velocity * np.cos(alpha)
    wb = velocity * np.sin(alpha)

    # Calculating Thrust
    thrust = Engine_Thrust(alpha, delta, theta, velocity)
    
    # Sets the variables in the labels in the interface
    return alpha_entry.set(alpha), delta_entry.set(delta), q_entry.set(0), theta_entry.set(theta), ub_entry.set(ub), wb_entry.set(wb), thrust_entry.set(thrust)

#------------------------------------------------------------------------------
# interface!!!!!!!!!!!!

#root is like the interface
root = Tk()
root.title("Plane Simulation User Interface")

#padding around the interface
mainframe = ttk.Frame(root, padding="3 3 10 10")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#defining variables for the velocity and gamma input
velocity_entry = StringVar()
velocity_entry = ttk.Entry(mainframe, width=15, textvariable=velocity_entry)
velocity_entry.grid(column=2, row=1, sticky=(W, E))
gamma_entry = StringVar()
gamma_entry = ttk.Entry(mainframe, width=7, textvariable=gamma_entry)
gamma_entry.grid(column=2, row=2, sticky=(W, E))

#defining variables for alpha, delta, q... etc and the labels that display these variables
alpha_entry = StringVar()
ttk.Label(mainframe, textvariable=alpha_entry).grid(column=2, row=4, sticky=(W, E))
delta_entry = StringVar()
ttk.Label(mainframe, textvariable=delta_entry).grid(column=2, row=5, sticky=(W, E))
q_entry = StringVar()
ttk.Label(mainframe, textvariable=q_entry).grid(column=2, row=6, sticky=(W, E))
thrust_entry = StringVar()
ttk.Label(mainframe, textvariable=thrust_entry).grid(column=2, row=7, sticky=(W, E))
theta_entry = StringVar()
ttk.Label(mainframe, textvariable=theta_entry).grid(column=2, row=8, sticky=(W, E))
ub_entry = StringVar()
ttk.Label(mainframe, textvariable=ub_entry).grid(column=2, row=9, sticky=(W, E))
wb_entry = StringVar()
ttk.Label(mainframe, textvariable=wb_entry).grid(column=2, row=10, sticky=(W, E))

#calculate button that calls on trim function
ttk.Button(mainframe, text="Calculate", command=Trim).grid(column=1, row=3, sticky=W)

#labels that display text
ttk.Label(mainframe, text="velocity:").grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text="gamma:").grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text="alpha:").grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text="delta:").grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, text="q:").grid(column=1, row=6, sticky=W)
ttk.Label(mainframe, text="thrust:").grid(column=1, row=7, sticky=W)
ttk.Label(mainframe, text="theta:").grid(column=1, row=8, sticky=W)
ttk.Label(mainframe, text="ub:").grid(column=1, row=9, sticky=W)
ttk.Label(mainframe, text="wb:").grid(column=1, row=10, sticky=W)

#idk what any of this does runs in a loop or something lol
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

velocity_entry.focus()
root.bind("<Return>", calculate)

root.mainloop()

