# -*- coding: utf-8 -*-
'''

CMM3 Group 7
Benjamin, Rodrigo, Maurice, Nick, Jack, Stamatis
October-November 2023  

'''

# importing modules
import numpy as np
import matplotlib.pyplot as plt
import constants, forms
from scipy import integrate

#------------------------------------------------------------------------------
# User parameters

velocity_0 = 100  # Aircraft velocity in m/s
gamma_0 = 0.00   # Path angle in rad

#------------------------------------------------------------------------------
# Trim & output

alpha_0, delta_0, q_0, theta_0, ub_0, wb_0, thrust_0 = forms.Trim(velocity_0, gamma_0)


print(f"alpha = {alpha_0}")
print(f"delta = {delta_0}")
print(f"q = {q_0}")
print(f"thrust = {thrust_0}")
print(f"theta = {theta_0}")
print(f"ub = {ub_0}")
print(f"wb = {wb_0}")

#------------------------------------------------------------------------------

t0 = 0      # Initial time (s)
t_end = 400   # End time (s)

q, theta, ub, wb, xe, ze = q_0, theta_0, ub_0, wb_0, 0, 0

y = integrate.solve_ivp(forms.SimControl, [0,t_end], [q, theta, ub, wb, xe, ze], t_eval=np.linspace(0,t_end,t_end*10))

# Plot the results
plt.subplot(3, 2, 1)
plt.plot(y.t, y.y[0])
plt.xlabel('time')
plt.ylabel('q')
plt.subplot(3, 2, 2)
plt.plot(y.t, y.y[1])
plt.xlabel('time')
plt.ylabel('theta')
plt.subplot(3, 2, 3)
plt.plot(y.t, y.y[2])
plt.xlabel('time')
plt.ylabel('ub')
plt.subplot(3, 2, 4)
plt.plot(y.t, y.y[3])
plt.xlabel('time')
plt.ylabel('wb')
plt.subplot(3, 2, 5)
plt.plot(y.t, y.y[4])
plt.xlabel('time')
plt.ylabel('xe')
plt.subplot(3, 2, 6)
plt.plot(y.t, -y.y[5])
plt.xlabel('time')
plt.ylabel('ze')
plt.show()
