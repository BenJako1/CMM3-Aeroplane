# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

This module, 'constants', contains evironment defining parameters, physical aircraft properties, as well as data lists 
copied from aero_tables file provided with the brief. It utilizes the 'optimize' module from the SciPy library to define
the data sets with linear and quadratic models and hence calculate the relvent coefficients needed for solving the 
equations of motions.
'''

# Importing libraries
import numpy as np
from scipy import optimize

#-----------------------------------------------------------------------------------------------------------
# Vehicle and environment parameters

gravity = 9.81  # Gravitational acceleration in m/s^2
air_density = 1.0065    # Air density in kg/m^3
wing_surface = 20.0 # Wing surface in m^2
cbar = 1.75 # airfoil chord in m
mass = 1300.0     # Mass of the airplane in kg
inertia_yy = 7000   # Moment of inertia in kg/m^2

#-----------------------------------------------------------------------------------------------------------
# Coefficient data sets

alpha_list = np.deg2rad(np.array([-16,-12,-8,-4,-2,0,2,4,8,12])) # List of angle of attack values in radians
delta_el_list  = np.deg2rad(np.array([-20,-10,0,10,20]))    # List of elevator angle values in radians
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
# Fit curves to data sets, defining constants

CL0 = 0.04
CLa = 0.1
def CLa_func (x, a, b):
    return a + b * x
[CL0, CLa], _ = optimize.curve_fit(CLa_func, alpha_list, CL_list, [CL0, CLa])

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

# This statement prints coefficients only when this script is run standalone
# Used for debugging
if __name__ == "__main__":
    print(f"CL0 = {CL0}")
    print(f"CLa = {CLa}")
    print(f"CLde = {CLde}")
    print(f"CM0 = {CM0}")
    print(f"CMa = {CMa}")
    print(f"CMde = {CMde}")
    print(f"CD0 = {CD0}")
    print(f"K = {K}")
