# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

This module, 'forms', is used to define the equations of motion, trim equations, and equilibrium equations of the aircraft.
These functions are called in the 'simulation' module(main script) to perform heavy computational tasks.
'forms' imports parameters from the 'constants' module, including the coefficients of lift, moment, and drag that were 
calculated using curve fitting methods, as well as environment defining parameters. Refer to the nomenclature in the README file 
for a comprehensive list of variable and function definitions.
''' 

#importing numpy library for trigonometric functions
#importing coefficients and constants from the 'constants' module
import numpy as np
import constants as c

def Coefficient_of_Lift(alpha, delta):
    return c.CL0 + c.CLa * alpha + c.CLde * delta

def Coefficient_of_Moment(alpha, delta):
    return c.CM0 + c.CMa * alpha + c.CMde * delta

def Coefficient_of_Drag(alpha, delta):
    return c.CD0 + c.K * (Coefficient_of_Lift(alpha, delta))**2

def Lift(alpha, delta, velocity):
    return (0.5 * c.air_density * velocity**2 * c.wing_surface *
            Coefficient_of_Lift(alpha, delta))

def Drag(alpha, delta, velocity):
    return (0.5 * c.air_density * velocity**2 * c.wing_surface *
            Coefficient_of_Drag(alpha, delta))

def Moment(alpha, delta, velocity):
    return (0.5 * c.air_density * velocity**2 * c.wing_surface *
           c.cbar * Coefficient_of_Moment(alpha, delta))

def Engine_Thrust(alpha, delta, theta, velocity):
    return (Drag(alpha, delta, velocity) * np.cos(alpha) - Lift(alpha, delta, velocity) * np.sin(alpha) + c.mass * c.gravity * np.sin(theta))

# Definition of differential equations
def Equations ( t, y, delta, thrust):
    q, theta, ub, wb, xe, ze = y
    
    alpha = np.arctan2(wb, ub)
    velocity = np.sqrt(ub**2 + wb**2)
    
    dq_dt = (Moment(alpha, delta, velocity)/c.inertia_yy)
    dtheta_dt = q
    
    dub_dt = (Lift(alpha, delta, velocity) * np.sin(alpha) - Drag(alpha, delta, velocity) * np.cos(alpha) - c.mass * q * wb - c.mass * c.gravity * np.sin(theta) + thrust) / c.mass
    dwb_dt = (-Lift(alpha, delta, velocity) * np.cos(alpha) - Drag(alpha, delta, velocity) * np.sin(alpha) + c.mass * q * ub + c.mass * c.gravity * np.cos(theta)) / c.mass
    
    dxe_dt = ub * np.cos(theta) + wb * np.sin(theta)
    dze_dt = - ub * np.sin(theta) + wb * np.cos(theta)
    
    return dq_dt, dtheta_dt, dub_dt, dwb_dt, dxe_dt, dze_dt
