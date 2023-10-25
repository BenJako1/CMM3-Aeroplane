
# importing modules
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton
import constants
import forms

#-----------------------------------------------------------------------------------------------------------
# User parameters

velocity = 100  # Aircraft velocity in m/s
gamma = 0.00   # Path angle in rad

#-----------------------------------------------------------------------------------------------------------
# Defining functions for later use. The functions are derived from the project breif.
def g(t, y):
    q, theta, ub, wb = y
    
    # Define auxiliary variables
    alpha = np.arctan2(wb, ub)
    CL = forms.Coefficient_of_Lift(alpha, delta)  # Function to calculate CL
    CD = forms.Coefficient_of_Drag(alpha, delta)  # Function to calculate CD
    L = 0.5 * constants.air_density * velocity**2 * constants.wing_surface * CL
    D = 0.5 * constants.air_density * velocity**2 * constants.wing_surface * CD
    
    # Define the system of differential equations
    dqdt = forms.Moment(alpha, delta, velocity, gamma) / constants.inertia_yy
    dthetadt = q
    dubdt = (L / constants.mass) * np.sin(alpha) - (D / constants.mass) * np.cos(alpha) - q * wb - constants.gravity * np.sin(theta)
    dwbdt = -(L / constants.mass) * np.cos(alpha) - (D / constants.mass) * np.sin(alpha) + q * ub + constants.gravity * np.cos(theta)
    
    return [dqdt, dthetadt, dubdt, dwbdt]

# Runge-Kutta method for integral solving. Parameters from dx/dt = f
def rk4_step(t, y, dt):
    k1 = np.array(g(t, y))
    k2 = np.array(g(t + dt/2, y + dt/2 * k1))
    k3 = np.array(g(t + dt/2, y + dt/2 * k2))
    k4 = np.array(g(t + dt, y + dt * k3))
    
    return y + dt/6 * (k1 + 2*k2 + 2*k3 + k4)

#-----------------------------------------------------------------------------------------------------------
# Final calculations & output

# Define the equilibrium equation as f(a)
def f(a):
    return forms.Equilibrium(a, velocity, gamma)   

# Solve for alpha and delta
initial_guess = 0.01  # Provide an initial guess
alpha = newton(f, initial_guess)
delta = -(constants.CM0 + constants.CMa * alpha)/constants.CMde

# Calculating other variables to output
theta = alpha + gamma
ub = velocity * np.cos(alpha)
wb = velocity * np.sin(alpha)

# Calculating Thrust
thrust = forms.Engine_Thrust(alpha, delta, theta, velocity, gamma)

print(f"alpha = {alpha}")
print(f"delta = {delta}")
print(f"thrust = {thrust}")
print(f"theta = {theta}")
print(f"ub = {ub}")
print(f"wb = {wb}")

#-----------------------------------------------------------------------------------------------------------
# Applying method for solving differential DOF equations

y0 = [0, theta, ub, wb]  # Initial values of q, theta, ub, wb
t0 = 0             # Initial time (s)
t_end = 20        # End time (s)
dt = 0.1           # Time step size (s)

t_values = [t0]
y_values = [y0]

t = t0
y = np.array(y0)

while t < t_end:
    y = rk4_step(t, y, dt)
    t += dt
    t_values.append(t)
    y_values.append(y.tolist())

q_values, theta_values, ub_values, wb_values = zip(*y_values)

plt.plot(t_values, q_values)
