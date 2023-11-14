#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

'''
'simulation' is the main script of the aircraft simulation. It contains the computationally intense code used to solve the equations
of motion using the initial value problem method. classes are heavily integrated into this module to reference repeating processes 
like graphing and calculating trim conditions for a variety of elevator angles and thrusts. Despite its highly 
object-oriented nature, this section seamlessly aligns with the overall modular design of the code, contributing to its 
efficiency and cohesion.
'''
# Import libraries & modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import forms
import constants as c

#------------------------------------------------------------------------------
# Class for handling the intitial and user unputted trim consitons

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
# Class to display data from other classes: plotting dynamic behavior and trim conditions

class Visualise():
    
    # Plotting aircraft parameter response
    def Display_Sim(self, Data):
        # Split data into components
        self.t = Data.t
        self.q = Data.y[0]
        self.theta = np.rad2deg(Data.y[1])
        self.ub = Data.y[2]
        self.wb = Data.y[3]
        self.xe = Data.y[4]
        self.ze = Data.y[5]
        
        # Calculate altitude because ze is reversed for some reason
        self.altitude = self.ze * -1
        #self.altitude += initialAltitude
        # Output the plot
        plt.show()

        fig, ax = plt.subplots(3, 2, figsize=(9, 7))

        ax[0, 0].plot(self.t, self.ub)
        ax[0, 0].set_title("$u_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 0].set_ylabel("$u_{B}$ [m/s]")
        ax[0, 0].set_xlabel("t [s]")

        ax[0, 1].plot(self.t, self.wb)
        ax[0, 1].set_title("$w_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 1].set_ylabel("$w_{B}$ [m/s]")
        ax[0, 1].set_xlabel("t [s]")
        
        ax[1, 0].plot(self.t, self.theta)
        ax[1, 0].set_title("${\Theta}$ Pitch Angle vs Time", fontsize=12)
        ax[1, 0].set_ylabel("${\Theta}$ [$^{0}$]")
        ax[1, 0].set_xlabel("t [s]")

        ax[1, 1].plot(self.t, self.q)
        ax[1, 1].set_title("q Angular Velocity vs Time", fontsize=12)
        ax[1, 1].set_ylabel("q [rad/s]")
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
    
    def Display_B1(self, V_values, gamma_values, T_values, delta_values):
       # Create a single figure with all the required subplots
       plt.figure(figsize=(14, 10))

       # Plot Thrust vs Velocity
       plt.subplot(2, 2, 1)
       for j, gamma in enumerate(gamma_values):
           plt.plot(V_values, T_values[:, j], label=f'γ = {np.rad2deg(gamma):.1f}°')
       plt.xlabel('Velocity V [m/s]')
       plt.ylabel('Thrust [N]')
       plt.title('Thrust vs. Velocity')
       plt.legend()

       # Plot Elevator Angle vs Velocity
       plt.subplot(2, 2, 2)
       for j, gamma in enumerate(gamma_values):
           plt.plot(V_values, delta_values[:, j], label=f'γ = {np.rad2deg(gamma):.1f}°')
       plt.xlabel('Velocity V [m/s]')
       plt.ylabel('Elevator Angle δₑ [$^{0}$]')
       plt.title('Elevator Angle vs. Velocity')
       plt.legend()

       # Plot Thrust vs gamma
       plt.subplot(2, 2, 3)
       for i, V in enumerate(V_values):
           plt.plot(gamma_values, T_values[i, :], label=f'V = {V} m/s')
       plt.xlabel('Flight Path Angle γ [$^{0}$]')
       plt.ylabel('Thrust [N]')
       plt.title('Thrust vs Flight Path Angle')
       plt.legend()

       # Plot Elevator Angle vs Flight Path Angle
       plt.subplot(2, 2, 4)
       for i, V in enumerate(V_values):
           plt.plot(np.rad2deg(gamma_values), delta_values[i, :], label=f'V = {V} m/s')
       plt.xlabel('Flight Path Angle γ [$^{0}$]')
       plt.ylabel('Elevator Angle δₑ [$^{0}$]')
       plt.title('Elevator Angle vs Flight Path Angle')
       plt.legend()

       # Adjust the layout for better appearance
       plt.tight_layout()

       # Display the plots
       plt.show()

#------------------------------------------------------------------------------
# B1 - To calculate trim conditions for various values of velocity and path angle

class B1(Visualise):
    def __init__(self, V_min, V_max, gamma_min, gamma_max, V_step, gamma_step):
        # Define the ranges for V and gamma
        self.V_min = V_min
        self.V_max = V_max
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max

        # Define step sizes for V and gamma
        self.V_step = V_step
        self.gamma_step = gamma_step

        # Create arrays to store results
        self.V_values = np.arange(self.V_min, self.V_max, self.V_step)
        self.gamma_values = np.arange(self.gamma_min, self.gamma_max, self.gamma_step)

        # Create arrays to store T and delta
        self.T_values = np.empty((len(self.V_values), len(self.gamma_values)))
        self.delta_values = np.empty((len(self.V_values), len(self.gamma_values)))

        for i, V in enumerate(self.V_values):
            for j, gamma in enumerate(self.gamma_values):
                # Create a new Trim instance with the current V and gamma
                trim_condition = Trim(V, gamma)

                # Store T and delta values from the trim condition
                self.T_values[i, j] = trim_condition.thrust
                self.delta_values[i, j] = np.rad2deg(trim_condition.delta)
        
        self.Display_B1(self.V_values, self.gamma_values, self.T_values, self.delta_values)

# B2 - To find the time required to climb a specified altitude at a specified angle and velocity
class B2(Visualise):
    def __init__(self, trimVelocity, trimGamma, t_end, initialAltitude, maxAltitude, pitchTime, climbVelocity, climbGamma, climbTimeGuess = 0, climbStep = 0.5):
        # Find trim conditions
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        trimParams2 = Trim(climbVelocity, climbGamma)
        self.Trim2 = trimParams2
        
        self.climbTime = climbTimeGuess
        self.pitchTime = pitchTime
        
        finalAltitude = initialAltitude
        
        while finalAltitude < maxAltitude:
            y = integrate.solve_ivp(self.SimControl, [0,t_end], [0,trimParams.theta, trimParams.ub, trimParams.wb, 0, -initialAltitude], t_eval=np.linspace(0,t_end,t_end*50))
            finalAltitude = -y.y[5][len(y.y[5])-1]
            
            self.climbTime += climbStep
            
        # Send data to "Display" function to be plotted
        self.Display_Sim(y)
        
        print(f"Climb Duration: {self.climbTime}s")
    
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        if t > self.pitchTime and t < self.pitchTime + self.climbTime:
            delta = self.Trim2.delta
            thrust = self.Trim2.thrust
        else:
            delta = self.Trim.delta
            thrust = self.Trim.thrust

        return forms.Equations(t, y, delta, thrust)

class Simulation(Visualise):
    def __init__(self, trimVelocity, trimGamma, initialAltitude, t_end, time_changes):
        self.time_changes = time_changes
        
        # Find trim conditions
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        y = integrate.solve_ivp(self.SimControl, [0,t_end], [0,trimParams.theta, trimParams.ub, trimParams.wb, 0, -initialAltitude], t_eval=np.linspace(0,int(t_end),int(t_end*50)))
            
        # Send data to "Display" function to be plotted
        self.data = y
    
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        delta = self.Trim.delta
        thrust = self.Trim.thrust
        
        for change_time, delta_change, thrust_change in self.time_changes:
            if t > change_time:
                delta += delta_change
                thrust += thrust_change

        return forms.Equations(t, y, delta, thrust)

# Debugging, uncomment and change commands as needed
if __name__ == "__main__":
    # Running the simulation
    sim = Simulation(100, 0, 1000, 1000, [(100.0, -0.002, 0.0), (300.0, 0.002, 0.0)])
    sim.Display_Sim(sim.data)
    
    # Running B1
    #B1(V_min=50, V_max=200, gamma_min=0, gamma_max=1, V_step=10, gamma_step=0.1)
      
    # Running B2
    #B2(trimVelocity=109, trimGamma=0, t_end=500, initialAltitude=1000, maxAltitude=2000, pitchTime=10, climbVelocity=109, climbGamma=np.deg2rad(2), climbTimeGuess=200, climbStep=1)
    