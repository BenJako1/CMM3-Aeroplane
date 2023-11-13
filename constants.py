# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

'''
This module, 'constants,' contains environment-defining parameters, physical aircraft properties, as well as data 
lists copied from the 'aero_tables' file provided with the brief. It utilizes the 'optimize' module from the 
SciPy library to define the data sets with linear and quadratic models and, hence, calculate the relevant 
coefficients needed for fully defining the aerodynamic constants CL, CM, an CD. 

Some limitations of this curve fitting method include its high dependence on the accuracy of initial guesses. 
If a poorly estimated initial guess is input into the curve fitting function, the resulting coefficients may 
be less representative of the data and effect the trimming of the airplane. 
'''

# Importing libraries to perform triginometric functions and use least-squares regression from SciPy.optimize
import numpy as np
from scipy import optimize


#----------------------------------------------------------------------------------------------------------------
# Aircraft parameters: Constants and Environment
#----------------------------------------------------------------------------------------------------------------

gravity = 9.81         # Gravitational acceleration in m/s^2
air_density = 1.0065   # Air density in kg/m^3
wing_surface = 20.0    # Wing surface area in m^2
cbar = 1.75            # Airfoil chord in m
mass = 1300.0          # Mass of the airplane in kg
inertia_yy = 7000      # Moment of inertia in kg/m^2

#-----------------------------------------------------------------------------------------------------------
# Constants data sets, copied from aero_tables file in project description
# Copying the data to this file prevents unnrcerary importing and reduces computing power

alpha_list = np.deg2rad(np.array([-16,-12,-8,-4,-2,0,2,4,8,12])) # List of angle of attack values in radians
delta_el_list  = np.deg2rad(np.array([-20,-10,0,10,20]))         # List of elevator angle values in radians
CD_list = np.array([
    0.115000000000000
  , 0.079000000000000
  , 0.047000000000000
  , 0.031000000000000
  , 0.027000000000000
  , 0.027000000000000
  , 0.029000000000000
  , 0.034000000000000
  , 0.054000000000000
  , 0.089000000000000
  ])
CL_list = np.array([
   -1.421000000000000
  ,-1.092000000000000
  ,-0.695000000000000
  ,-0.312000000000000
  ,-0.132000000000000
  , 0.041000000000000
  , 0.218000000000000
  , 0.402000000000000
  , 0.786000000000000
  , 1.186000000000000
  ])
CM_list = np.array([
    0.077500000000000
  , 0.066300000000000
  , 0.053000000000000
  , 0.033700000000000
  , 0.021700000000000
  , 0.007300000000000
  ,-0.009000000000000
  ,-0.026300000000000 
  ,-0.063200000000000
  ,-0.123500000000000
  ])
CM_el_list = np.array([
    0.084200000000000
  , 0.060100000000000
  ,-0.000100000000000
  ,-0.060100000000000
  ,-0.084300000000000
  ])
CL_el_list = np.array([
   -0.051000000000000
  ,-0.038000000000000
  , 0.0
  , 0.038000000000000
  , 0.052000000000000
  ])

#-----------------------------------------------------------------------------------------------------------
# Part A1 = Claculating Constants
#-----------------------------------------------------------------------------------------------------------
# Fitting curves to data sets, defining constants 
#-----------------------------------------------------------------------------------------------------------

'''
The coefficients CL0, CLa, CLde, CM0, CMde, CD0, and K, are calculated using the least squares method imported from 
the SciPy library. The least squares method requires an initial guess for each coefficient that is being calculated. 
The initial guesses are values that were approximated from graphs included in the report brief and are included 
in the least squares method to reduce the required number of iterations, thus accelerating convergence. 
The values for the coefficients CL0, etc., are assigned an initial guess just above the function. 
These values serve as representative guesses for coefficients 'a' and 'b' in the objective simplified function.
'''

# Example for Cl0 and CLa calculation:
CL0 = 0.04
CLa = 0.1
def CLa_func (x, a, b):
    return a + b * x
[CL0, CLa], _ = optimize.curve_fit(CLa_func, alpha_list, CL_list, [CL0, CLa])

# This procedure is repeated for other constants:

CLde = 0.003
def CLde_func (x, a):
    return x * a
[CLde], _ = optimize.curve_fit(CLde_func, delta_el_list, CL_el_list, CLde)

CM0 = 0.0
CMa = -0.06
def CM_func(x, a, b):
    return a + b * x
[CM0, CMa], _ = optimize.curve_fit(CM_func, alpha_list, CM_list, [CM0, CMa])

CMde = -0.005
def CMde_func (x, a):
    return x * a
[CMde], _ = optimize.curve_fit(CMde_func, delta_el_list, CM_el_list, CMde)

CD0 = 0.02
K = 0.04
def CD_func(x, a, b):
    return a + b * x**2.0
[CD0, K], _ = optimize.curve_fit(CD_func, CL_list, CD_list, [CD0, K])


# The coefficients will only print when this file is run standalone
# Used for debugging
if __name__ == "__main__":
    coefficients = ["CL0", "CLa", "CLde", "CM0", "CMa", "CMde", "CD0", "K"]
    for coeff in coefficients:
        value = globals()[coeff]
        print(f"{coeff} = {value:.5f}")
