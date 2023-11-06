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
 
