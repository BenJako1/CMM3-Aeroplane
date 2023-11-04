# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

#This module, 'Forms', is used to define the formulas of the aircraft dynamics without having to include them 
#in the main script. This module imports variables from the 'constants'module so that it recognizes variables such as 
#CL0, CLa, and so on. 
import numpy as np
from scipy.optimize import newton
import constants

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

def Trim(velocity, gamma):
    
    def alpha_trim_func(alpha):
        delta = np.deg2rad(-(constants.CM0 + constants.CMa * np.rad2deg(alpha)) / constants.CMde)

        return (-Lift(alpha, delta, velocity) * np.cos(alpha) - Drag(alpha, delta, velocity) * np.sin(alpha) + constants.mass * constants.gravity * np.cos(alpha + gamma))
    
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
    
    return alpha, delta, 0, theta, ub, wb, thrust

# Definition of the differential equations to be used in IVP solution
def Equations (t, y, delta, thrust):
    q, theta, ub, wb, xe, ze = y
    
    alpha = np.arctan2(wb, ub)
    velocity = np.sqrt(ub**2 + wb**2)
    
    dq_dt = (Moment(alpha, delta, velocity)/constants.inertia_yy)
    dtheta_dt = q
    
    dub_dt = (Lift(alpha, delta, velocity) * np.sin(alpha) - Drag(alpha, delta, velocity) * np.cos(alpha) - constants.mass * q * wb - constants.mass * constants.gravity * np.sin(theta) + thrust) / constants.mass
    dwb_dt = (-Lift(alpha, delta, velocity) * np.cos(alpha) - Drag(alpha, delta, velocity) * np.sin(alpha) + constants.mass * q * wb + constants.mass * constants.gravity * np.cos(theta)) / constants.mass
    
    dxe_dt = ub * np.cos(theta) + wb * np.sin(theta)
    dze_dt = - ub * np.sin(theta) + wb * np.cos(theta)
    
    return dq_dt, dtheta_dt, dub_dt, dwb_dt, dxe_dt, dze_dt

def SimControl (t, y):
    _, delta_0, _, _, _, _, thrust_0 = Trim(100, 0)
    _, delta_1, _, _, _, _, thrust_1 = Trim(120, 0.05)
    if t > 100:
        delta = delta_1
        thrust = thrust_1
    else:
        delta = delta_0
        thrust = thrust_0
    return Equations(t, y, delta, thrust)
 
