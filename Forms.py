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
    return constants.CL0 + constants.CLa * a + constants.CLde * d

def Coefficient_of_Moment(a, d):
    return constants.CM0 + constants.CMa * a + constants.CMde * d

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

def Engine_Thrust(a, d, the, velocity):
    return (Drag(a, d, velocity) * np.cos(a) +
            constants.mass * constants.gravity * np.sin(the) -
            0.5 * constants.air_density * velocity**2 * constants.wing_surface *
            Coefficient_of_Lift(a, d) * np.sin(a))

def Equilibrium(a, velocity, gamma):
    return (-0.5 * constants.air_density * velocity**2 * constants.wing_surface *
            (constants.CL0 + constants.CLa * a - constants.CLde * (constants.CM0 + constants.CMa * a) / constants.CMde) * np.cos(a) -
            0.5 * constants.air_density * velocity**2 * constants.wing_surface *
            (constants.CD0 + constants.K * (constants.CL0 + constants.CLa * a - constants.CLde * (constants.CM0 + constants.CMa * a) / constants.CMde)**2) * np.sin(a) +
            constants.mass * constants.gravity * np.cos(a + gamma))

def Trim(velocity, gamma):
    # Define the equilibrium equation as f(a)
    def f(a):
        return Equilibrium(a, velocity, gamma)   

    # Solve for alpha and delta
    initial_guess = 0.01  # Provide an initial guess
    alpha = newton(f, initial_guess)
    delta = -(constants.CM0 + constants.CMa * alpha)/constants.CMde

    # Calculating other variables to output
    theta = alpha + gamma
    ub = velocity * np.cos(alpha)
    wb = velocity * np.sin(alpha)

    # Calculating Thrust
    thrust = Drag(alpha, delta, velocity) * np.cos(alpha) - Lift(alpha, delta, velocity) * np.sin(alpha) + constants.mass * constants.gravity * np.sin(theta)
    
    return alpha, delta, theta, ub, wb, thrust
