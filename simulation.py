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
# User parameters

velocity_0 = 100 # Velocity in m/s
gamma_0 = 0 # Path angle in radians

pitchTime = 100 # Time in seconds after simulationstart at which the values are changed
climbTime = 200

elevatorChange = 10 # in percent
thrustChange = 10 # in percent

#------------------------------------------------------------------------------


class Trim:
    def __init__(self, trimVelocity, trimGamma):
        self.velocity = trimVelocity
        self.gamma = trimGamma
        
        # Solve for alpha
        initial_guess = 0.01  # Provide an initial guess
        self.alpha = optimize.newton(self.alpha_trim_func, initial_guess)
        
        # Solve for delta
        self.delta = np.deg2rad(-(c.CM0 + c.CMa * np.rad2deg(self.alpha)) / c.CMde)
    
        # Calculating other variables to output
        self.theta = self.alpha + trimGamma
        self.ub = trimVelocity * np.cos(self.alpha)
        self.wb = trimVelocity * np.sin(self.alpha)
    
        # Calculating Thrust
        self.thrust = forms.Engine_Thrust(self.alpha, self.delta, self.theta, trimVelocity)
        
    def alpha_trim_func(self, alpha):
        self.delta = np.deg2rad(-(c.CM0 + c.CMa * np.rad2deg(alpha)) / c.CMde)

        return (-forms.Lift(alpha, self.delta, self.velocity) * np.cos(alpha) - forms.Drag(alpha, self.delta, self.velocity) * np.sin(alpha) + c.mass * c.gravity * np.cos(alpha + self.gamma))


class Backend():
    def HandleSimulationData(self,Data,h = 0):
        self.t = Data.t

        self.ub = Data.y[0]
        self.wb = Data.y[1]
        self.theta = Data.y[2]
        self.q = Data.y[3]
        self.xe = Data.y[4]
        self.ze = Data.y[5]

        self.altitude = self.ze * -1
        self.altitude += h

        fig,ax = plt.subplots(3,2)

        ax[0,0].set_ylabel("$u_{B}$",rotation='horizontal')
        ax[0,0].set_xlabel("t")
        ax[0,1].set_ylabel("$w_{B}$",rotation='horizontal')
        ax[0,1].set_xlabel("t")

        ax[1,0].set_ylabel("${\Theta}$",rotation='horizontal')
        ax[1,0].set_xlabel("t")
        ax[1,1].set_ylabel("q",rotation='horizontal')
        ax[1,1].set_xlabel("t")

        ax[2,0].set_ylabel("$x_{e}$",rotation='horizontal')
        ax[2,0].set_xlabel("t")

        ax[2,1].set_ylabel("Altitude h")
        ax[2,1].set_xlabel("t")

        ax[0,0].plot(self.t,self.ub)
        ax[0,1].plot(self.t,self.wb)
        ax[1,0].plot(self.t,self.theta)
        ax[1,1].plot(self.t,self.q)
        ax[2,0].plot(self.t,self.xe)
        ax[2,1].plot(self.t,self.altitude)

        plt.show()
        
    def Equations (self, t, y, delta, thrust):
        q, theta, ub, wb, xe, ze = y
        
        alpha = np.arctan2(wb, ub)
        velocity = np.sqrt(ub**2 + wb**2)
        
        dq_dt = (forms.Moment(alpha, delta, velocity)/c.inertia_yy)
        dtheta_dt = q
        
        dub_dt = (forms.Lift(alpha, delta, velocity) * np.sin(alpha) - forms.Drag(alpha, delta, velocity) * np.cos(alpha) - c.mass * q * wb - c.mass * c.gravity * np.sin(theta) + thrust) / c.mass
        dwb_dt = (-forms.Lift(alpha, delta, velocity) * np.cos(alpha) - forms.Drag(alpha, delta, velocity) * np.sin(alpha) + c.mass * q * ub + c.mass * c.gravity * np.cos(theta)) / c.mass
        
        dxe_dt = ub * np.cos(theta) + wb * np.sin(theta)
        dze_dt = - ub * np.sin(theta) + wb * np.cos(theta)
        
        return dq_dt, dtheta_dt, dub_dt, dwb_dt, dxe_dt, dze_dt

class Simulation(Backend):
    def __init__(self,trimVelocity,trimGamma,t_end):
 
        trimParams = Trim(trimVelocity,trimGamma)
        self.Trim = trimParams

        y = integrate.solve_ivp(self.SimControl,[0,t_end],[0,trimParams.theta,trimParams.ub,trimParams.wb,0,0],t_eval=np.linspace(0,t_end,t_end*10))

        self.HandleSimulationData(y,1000)

    def SimControl(self,t,y):
        if t > pitchTime and t < pitchTime + climbTime:
            delta = self.Trim.delta * (1 + elevatorChange/100)
        else:
            delta = self.Trim.delta

        if t > pitchTime and t < pitchTime + climbTime:
            Thrust = self.Trim.thrust * (1 + thrustChange/100)
        else:
            Thrust = self.Trim.thrust

        return self.Equations(t,y,delta,Thrust)

Simulation(100,0,1000)
     