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

velocity_0 = 109 # Velocity in m/s
gamma_0 = 0 # Path angle in radians

pitchTime = 10 # Time in seconds after simulationstart at which the values are changed
max_altitude = 2000

climbVelocity = velocity_0
climbGamma = np.deg2rad(2)
climbTimeGuess = 200
climbStep = 0.5

elevatorChange = 10 # in percent
thrustChange = 0 # in percent

initialAltitude = 1000 # Altitude at t=0
maxAltitude = 2000

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
    
    # Simulations visualisation
    def Display(self, Data,initialAltitude = 0):
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
        #self.altitude += initialAltitude

        # Create plot
        fig,ax = plt.subplots(3, 2)
        
        # Format axes
        ax[0,0].set_ylabel("$u_{B}$", rotation='horizontal')
        ax[0,0].set_xlabel("t")
        ax[0,1].set_ylabel("$w_{B}$", rotation='horizontal')
        ax[0,1].set_xlabel("t")
        ax[1,0].set_ylabel("${\Theta}$", rotation='horizontal')
        ax[1,0].set_xlabel("t")
        ax[1,1].set_ylabel("q", rotation='horizontal')
        ax[1,1].set_xlabel("t")
        ax[2,0].set_ylabel("$x_{e}$", rotation='horizontal')
        ax[2,0].set_xlabel("t")
        ax[2,1].set_ylabel("Altitude h")
        ax[2,1].set_xlabel("t")
        
        # Plot data
        ax[0,0].plot(self.t, self.ub)
        ax[0,1].plot(self.t, self.wb)
        ax[1,0].plot(self.t, self.theta)
        ax[1,1].plot(self.t, self.q)
        ax[2,0].plot(self.t, self.xe)
        ax[2,1].plot(self.t, self.altitude)
        
        # Show
        plt.show()

#------------------------------------------------------------------------------
# Simulation calculation and control class

class Simulation(Visualise):
    def __init__(self, trimVelocity, trimGamma, t_end):
        
        # Find trim conditions
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        trimParams2 = Trim(climbVelocity, climbGamma)
        self.Trim2 = trimParams2
        
        self.climbTime = climbTimeGuess
        
        finalAltitude = initialAltitude
        
        while finalAltitude < maxAltitude:
            y = integrate.solve_ivp(self.SimControl, [0,t_end], [0,trimParams.theta, trimParams.ub, trimParams.wb, 0, -initialAltitude], t_eval=np.linspace(0,t_end,t_end*50))
            finalAltitude = -y.y[5][len(y.y[5])-1]
            
            self.climbTime += climbStep
            
        # Send data to "Display" function to be plotted
        self.Display(y, initialAltitude)
        print(f"Climb Duration: {self.climbTime}s")
    
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        if t > pitchTime and t < pitchTime + self.climbTime:
            delta = self.Trim2.delta
            thrust = self.Trim2.thrust
        else:
            delta = self.Trim.delta
            thrust = self.Trim.thrust

        return forms.Equations(t, y, delta, thrust)

# Running the simulation
Simulation(velocity_0, gamma_0, 500)
