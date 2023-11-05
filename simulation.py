
import constants 
import Forms
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import integrate

def SimControl (t, y):
    thrust = 0  # Set a default value
    if t > 100:
        delta = -0.0572
         # Assign a value if the condition is met
    else:
        delta = -0.0520009905019009
    return Equations(t, y, delta)


def Equations (t, y, delta):
    q, theta, ub, wb, xe, ze = y
    
    alpha = np.arctan(wb/ub)
    
    velocity = np.sqrt(ub**2 + wb**2)
    #Change to thrust fornula raw if needed
    thrust = Forms.Engine_Thrust(alpha, delta, theta, velocity)
    
    CL = Forms.Coefficient_of_Lift(alpha, delta)
    CM = Forms.Coefficient_of_Moment(alpha, delta)
    CD = Forms.Coefficient_of_Drag(alpha, delta)
    
    Lift = 0.5 * constants.air_density * (velocity**2) * constants.wing_surface * CL
    Drag = 0.5 * constants.air_density * (velocity**2) * constants.wing_surface * CD
    Moment = 0.5 * constants.air_density * (velocity**2) * constants.wing_surface * constants.cbar * CM
    
    dq_dt = (Moment/constants.inertia_yy)
    dtheta_dt = q
    
    dub_dt = (Lift * np.sin(alpha)/constants.mass) - (Drag * np.cos(alpha)/constants.mass) - (q * wb) - (constants.mass * constants.gravity * np.sin(theta)/constants.mass) + (thrust / constants.mass)
    dwb_dt = (-Lift * np.cos(alpha) - Drag * np.sin(alpha) + (constants.mass * q * ub) + constants.mass * constants.gravity * np.cos(theta)) / constants.mass
    
    dxe_dt = ub * np.cos(theta) + wb * np.sin(theta)
    dze_dt = - ub * np.sin(theta) + wb * np.cos(theta)
    
    return dq_dt, dtheta_dt, dub_dt, dwb_dt, dxe_dt, dze_dt


velocity_0 = 100  # Aircraft velocity in m/s
gamma_0 = 0.00   # Path angle in rad

#------------------------------------------------------------------------------
# Trim & output

alpha_0, delta_0, q_0, theta_0, ub_0, wb_0, thrust_0 = Forms.Trim(velocity_0, gamma_0)
'''
print(f"alpha = {alpha_0}")
print(f"delta = {delta_0}")
print(f"q = {q_0}")
print(f"thrust = {thrust_0}")
print(f"theta = {theta_0}")
print(f"ub = {ub_0}")
print(f"wb = {wb_0}")
'''
t0 = 0      # Initial time (s)
t_end = 300   # End time (s)

q, theta, ub, wb, xe, ze = q_0, theta_0, ub_0, wb_0, 0, 0
'''
a = 0.0164
q = 0
theta = 0.0164
ub = 99.86
wb = 1.646
xe = 0
ze = 0
'''
y = integrate.solve_ivp(SimControl, [0,300], [0, theta, ub, wb, xe, ze], method='Radau', t_eval=np.linspace(0, t_end, 3000))

plt.figure(figsize=(12, 10))

plt.subplot(3, 2, 1)
plt.plot(y.t, y.y[2])
plt.xlabel('time')
plt.ylabel('ub')

plt.subplot(3, 2, 2)
plt.plot(y.t, y.y[3])
plt.xlabel('time')
plt.ylabel('wb')

plt.subplot(3, 2, 3)
plt.plot(y.t, y.y[0])
plt.xlabel('time')
plt.ylabel('q')

plt.subplot(3, 2, 4)
plt.plot(y.t, y.y[1])
plt.xlabel('time')
plt.ylabel('theta')

plt.subplot(3, 2, 5)
plt.plot(y.t, y.y[4])
plt.xlabel('time')
plt.ylabel('xe')

plt.subplot(3, 2, 6)
plt.plot(y.t, -y.y[5])
plt.xlabel('time')
plt.ylabel('ze')

plt.tight_layout()  # Adjust the layout for better spacing
plt.show()
