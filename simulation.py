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

#-----------------------------------------------------------------------------------------------------------
# User parameters

velocity = 100  # Aircraft velocity in m/s
gamma = 0.00   # Path angle in rad

#-----------------------------------------------------------------------------------------------------------
# Trim & output

alpha, delta, theta, ub, wb, thrust = forms.Trim(velocity, gamma)


print(f"alpha = {alpha}")
print(f"delta = {delta}")
print(f"thrust = {thrust}")
print(f"theta = {theta}")
print(f"ub = {ub}")
print(f"wb = {wb}")

#-----------------------------------------------------------------------------------------------------------
# Applying Euler method for solving differential DOF equations

t0 = 0      # Initial time (s)
tEnd = 10   # End time (s)
dt = 0.1    # Time step size (s)

q = 0 # Initial angular velocity in rad/sec
xe = 0
ze = 0
t = t0

moment = forms.Moment(alpha, delta, velocity)

tValues = [t0]
thetaValues = [theta]
qValues = [q]
xeValues = [xe]
zeValues = [ze]
ubValues = [ub]
wbValues = [wb]
gammaValues = [gamma]
alphaValues = [alpha]
momentValues = [moment]

while t < tEnd:
    if t >= 1:
        delta = -0.0572
    
    # Compute new values using the DOF equations
    theta += q * dt
    alpha = np.arctan2(wb, ub)
    gamma = theta - alpha
    moment = forms.Moment(alpha, delta, velocity)
    thrust = forms.Engine_Thrust(alpha, delta, theta, velocity)
    q += (moment/constants.inertia_yy) * dt
    xe += (ub * np.cos(theta) + wb * np.sin(theta)) * dt
    ze -= (- ub * np.sin(theta) + wb * np.cos(theta)) * dt
    ub += (forms.Lift(alpha, delta, velocity) * np.sin(alpha) / constants.mass - forms.Drag(alpha, delta, velocity) *
           np.cos(alpha) / constants.mass - q * wb - constants.gravity * np.sin(theta) +
           thrust/constants.mass) * dt
    wb += (- np.cos(alpha) * forms.Lift(alpha, delta, velocity) / constants.mass - forms.Drag(alpha, delta, velocity) *
           np.sin(alpha) / constants.mass + q * ub + constants.gravity * np.cos(theta)) * dt
    # Append new values to arrays
    t += dt
    
    tValues.append(round(t, 1))
    thetaValues.append(theta)
    qValues.append(q)
    xeValues.append(xe)
    zeValues.append(ze)
    ubValues.append(ub)
    wbValues.append(wb)
    alphaValues.append(alpha)
    gammaValues.append(gamma)
    momentValues.append(moment)

# Plot the results
plt.plot(tValues, alphaValues, 'b-')
plt.subplot(4, 2, 1)
plt.plot(tValues, ubValues)
plt.xlabel('time')
plt.ylabel('ub')
plt.subplot(4, 2, 2)
plt.plot(tValues, wbValues)
plt.xlabel('time')
plt.ylabel('wb')
plt.subplot(4, 2, 3)
plt.plot(tValues, qValues)
plt.xlabel('time')
plt.ylabel('q')
plt.subplot(4, 2, 4)
plt.plot(tValues, thetaValues)
plt.xlabel('time')
plt.ylabel('theta')
plt.subplot(4, 2, 5)
plt.plot(tValues, gammaValues)
plt.xlabel('time')
plt.ylabel('path angle')
plt.subplot(4, 2, 6)
plt.plot(tValues, zeValues)
plt.xlabel('time')
plt.ylabel('ze')
plt.subplot(4, 2, 7)
plt.plot(tValues, alphaValues)
plt.xlabel('time')
plt.ylabel('alpha')
plt.subplot(4, 2, 8)
plt.plot(tValues, momentValues)
plt.xlabel('time')
plt.ylabel('moment')
plt.show()
