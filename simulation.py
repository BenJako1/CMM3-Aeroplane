#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

# Import libraries & modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import forms
import constants as c

#------------------------------------------------------------------------------
# User parameters (to be replaced with UI)

velocity_0 = 100 # Velocity in m/s
gamma_0 = 0 # Path angle in radians

pitchTime = 100 # Time in seconds after simulationstart at which the values are changed
climbTime = 300 # Duration of climb in seconds

elevatorChange = 10 # in percent
thrustChange = 0 # in percent

initialAltitude = 2000 # Altitude at t=0

simTime = 500

#------------------------------------------------------------------------------
# Class for handling the trim condition

class Trim:
    def __init__(self, trimVelocity, trimGamma):
        self.velocity = trimVelocity
        self.gamma = trimGamma
        
        # Solve for alpha
        initial_guess = 0.01  # Provide an initial guess
        self.alpha = optimize.newton(self.alpha_trim_func, initial_guess)
        
        # Solve for delta
        self.delta = -(c.CM0 + c.CMa * self.alpha) / c.CMde
    
        # Calculating other variables to output
        self.theta = self.alpha + trimGamma
        self.ub = trimVelocity * np.cos(self.alpha)
        self.wb = trimVelocity * np.sin(self.alpha)
    
        # Calculating thrust
        self.thrust = forms.Engine_Thrust(self.alpha, self.delta, self.theta, trimVelocity)
        
    def alpha_trim_func(self, alpha):
        self.delta = -(c.CM0 + c.CMa * alpha) / c.CMde

        return (-forms.Lift(alpha, self.delta, self.velocity) * np.cos(alpha) - forms.Drag(alpha, self.delta, self.velocity) * np.sin(alpha) + c.mass * c.gravity * np.cos(alpha + self.gamma))

#------------------------------------------------------------------------------
# Backend class to handle data and store diff. equations (should be a clearer name)
class Visualise():
    
    # Plotting aircraft parameter response
    def Display(self, Data, initialAltitude = 0):
        # Split data into components
        self.t = Data.t
        self.q = Data.y[0]
        self.theta = Data.y[1]
        self.ub = Data.y[2]
        self.wb = Data.y[3]
        self.xe = Data.y[4]
        self.ze = Data.y[5]
        
        # Calculate altitude because ze is reversed for some reason
        self.altitude = self.ze * -1
        self.altitude += initialAltitude
        
        fig, ax = plt.subplots(3, 2, figsize=(12, 10))

        ax[0, 0].plot(self.t, self.ub)
        ax[0, 0].set_title("$u_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 0].set_ylabel("$u_{B}$ [m/s]", rotation='horizontal')
        ax[0, 0].set_xlabel("t [s]")

        ax[0, 1].plot(self.t, self.wb)
        ax[0, 1].set_title("$w_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 1].set_ylabel("$w_{B}$ [m/s]", rotation='horizontal')
        ax[0, 1].set_xlabel("t [s]")
        
        ax[1, 0].plot(self.t, self.theta)
        ax[1, 0].set_title("${\Theta}$ Pitch Angle vs Time", fontsize=12)
        ax[1, 0].set_ylabel("${\Theta}$ [$^{0}$]", rotation='horizontal')
        ax[1, 0].set_xlabel("t [s]")

        ax[1, 1].plot(self.t, self.q)
        ax[1, 1].set_title("q Angular Velocity vs Time", fontsize=12)
        ax[1, 1].set_ylabel("q [rad/s]", rotation='horizontal')
        ax[1, 1].set_xlabel("t [s]")

        ax[2, 0].plot(self.t, self.xe)
        ax[2, 0].set_title("$x_{E}$ Horizontal Position vs Time", fontsize=12)
        ax[2, 0].set_ylabel("$x_{e}$ [m]")
        ax[2, 0].set_xlabel("t [s]")

        ax[2, 1].plot(self.t, self.altitude)
        ax[2, 1].set_title("h Altitude  vs Time", fontsize=12)
        ax[2, 1].set_ylabel("Altitude h [m]")
        ax[2, 1].set_xlabel("t [s]")

        plt.tight_layout()

        # Output the plot
        return fig

#------------------------------------------------------------------------------
# Simulation calculation and control class

class Simulation(Visualise):
    def __init__(self, trimVelocity, trimGamma, pitchTime, climbTime, elevatorChange, thrustChange, t_end):
        
        # Find trim conditions
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        # IVP library
        y = integrate.solve_ivp(self.SimControl, [0,t_end], [0,trimParams.theta, trimParams.ub, trimParams.wb, 0, 0], t_eval=np.linspace(0,t_end,t_end*50))

        self.data = y
        
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        if t > pitchTime and t < pitchTime + climbTime:
            delta = self.Trim.delta * (1 + elevatorChange/100)
        else:
            delta = self.Trim.delta

        if t > pitchTime and t < pitchTime + climbTime:
            thrust = self.Trim.thrust * (1 + thrustChange/100)
        else:
            thrust = self.Trim.thrust

        return forms.Equations(t, y, delta, thrust)

if __name__ == "__main__":
    # Running the simulation
    sim = Simulation(velocity_0, gamma_0, pitchTime, climbTime, elevatorChange, thrustChange, simTime)
    sim.Display(sim.data)
    