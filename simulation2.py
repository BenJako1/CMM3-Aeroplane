#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  3 17:22:39 2023

@author: ben
"""

# Import libraries & modules
import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import forms, constants

#------------------------------------------------------------------------------
# User parameters

velocity_0 = 100
gamma_0 = 0 # Path angle in radians

#------------------------------------------------------------------------------


class Trim:
    def __init__(self, trimVelocity, trimGamma):
        self.velocity = trimVelocity
        self.gamma = trimGamma
        
        # Solve for alpha
        initial_guess = 0.01  # Provide an initial guess
        self.alpha = optimize.newton(self.alpha_trim_func, initial_guess)
        
        # Solve for delta
        self.delta = np.deg2rad(-(constants.CM0 + constants.CMa * np.rad2deg(self.alpha)) / constants.CMde)
    
        # Calculating other variables to output
        self.theta = self.alpha + trimGamma
        self.ub = trimVelocity * np.cos(self.alpha)
        self.wb = trimVelocity * np.sin(self.alpha)
    
        # Calculating Thrust
        self.thrust = forms.Engine_Thrust(self.alpha, self.delta, self.theta, trimVelocity)
        
    def alpha_trim_func(self, alpha):
        self.delta = np.deg2rad(-(constants.CM0 + constants.CMa * np.rad2deg(alpha)) / constants.CMde)

        return (-forms.Lift(alpha, self.delta, self.velocity) * np.cos(alpha) - forms.Drag(alpha, self.delta, self.velocity) * np.sin(alpha) + constants.mass * constants.gravity * np.cos(alpha + self.gamma))


class Sim():
    def HandleSimulationData(self,Data,h = 0):
        self.t = Data.t

        self.u_b = Data.y[0]
        self.w_b = Data.y[1]
        self.theta = Data.y[2] 
        self.theta = np.rad2deg(self.theta)
        self.q = Data.y[3]
        self.x_e = Data.y[4]
        self.z_e = Data.y[5]

        self.altitude = self.z_e * -1
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

        #ze is negative of the altitude
        # ax[2,1].set_ylabel("$z_{e}$",rotation='horizontal')
        # ax[2,1].set_xlabel("t")

        ax[2,1].set_ylabel("Altitude h")
        ax[2,1].set_xlabel("t")

        ax[0,0].plot(self.t,self.u_b)
        ax[0,1].plot(self.t,self.w_b)
        ax[1,0].plot(self.t,self.theta)
        ax[1,1].plot(self.t,self.q)
        ax[2,0].plot(self.t,self.x_e)
        # ax[2,1].plot(t,z_e)
        ax[2,1].plot(self.t,self.altitude)

        plt.show()
        
    def Equations (self, t, y, delta, thrust):
        q, theta, ub, wb, xe, ze = y
        
        alpha = np.arctan2(wb, ub)
        velocity = np.sqrt(ub**2 + wb**2)
        
        dq_dt = (forms.Moment(alpha, delta, velocity)/constants.inertia_yy)
        dtheta_dt = q
        
        dub_dt = (forms.Lift(alpha, delta, velocity) * np.sin(alpha) - forms.Drag(alpha, delta, velocity) * np.cos(alpha) - constants.mass * q * wb - constants.mass * constants.gravity * np.sin(theta) + thrust) / constants.mass
        dwb_dt = (-forms.Lift(alpha, delta, velocity) * np.cos(alpha) - forms.Drag(alpha, delta, velocity) * np.sin(alpha) + constants.mass * q * wb + constants.mass * constants.gravity * np.cos(theta)) / constants.mass
        
        dxe_dt = ub * np.cos(theta) + wb * np.sin(theta)
        dze_dt = - ub * np.sin(theta) + wb * np.cos(theta)
        
        return dq_dt, dtheta_dt, dub_dt, dwb_dt, dxe_dt, dze_dt

class Simulation(Sim):
    def __init__(self,trimVelocity,trimGamma,t_end,t_climb_end,Precision):

 
        trimParams = Trim(trimVelocity,trimGamma)
        self.Trim = trimParams

        y = integrate.solve_ivp(self.Model,[0,t_end],[0,trimParams.theta,trimParams.ub,trimParams.wb,0,0],t_eval=np.linspace(0,t_end,t_end*10))

        self.HandleSimulationData(y,1000)

 

    def Model(self,t,y):
        if t > 10 and t < 10 + self.T_climb:
            delta = self.Trim2.delta
        else:
            delta = self.Trim.delta

        if t > 10 and t < 10 + self.T_climb:
            Thrust = self.Trim2.thrust
        else:
            Thrust = self.Trim.thrust

        return self.Equations(t,y,delta,Thrust)

Simulation(100,0,500,230,10)
     