# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

import numpy as np

gravity = 9.81  # Gravitational acceleration in m/s^2
air_density = 1.0065    # Air density in kg/m^3
wing_surface = 20.0 # Wing surface in m^2
cbar = 1.75 # airfoil chord in m
mass = 1300.0     # Mass of the airplane in kg
inertia_yy = 7000   # Moment of inertia in kg/m^2

alpha_list = np.array(np.deg2rad([-16,-12,-8,-4,-2,0,2,4,8,12])) # List of angle of attack values in radians
delta_el_list  = np.array(np.deg2rad([-20,-10,0,10,20]))    # List of elevator angle values in radians
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
CLa, CL0 = np.polyfit(alpha_list, CL_list, 1)
CLde, _ = np.polyfit(delta_el_list, CL_el_list, 1)
CMa, CM0 = np.polyfit(alpha_list, CM_list, 1)
CMde, _ = np.polyfit(delta_el_list, CM_el_list, 1)
K, _, CD0 = np.polyfit(CL_list, CD_list, 2)

# Print constant values
print(f"CLa = {CLa}")
print(f"CL0 = {CL0}")
print(f"CMa = {CMa}")
print(f"CM0 = {CM0}")
print(f"CLde = {CLde}")
print(f"CMde = {CMde}")
print(f"CD0 = {CD0}")
print(f"K = {K}")