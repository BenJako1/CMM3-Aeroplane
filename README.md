# CMM3-Aeroplane
Model of the longitudinal stability of an aeroplane


Group 07 

Longitudinal Dynamics of a Small Aircraft


-----------------------------------------------------------------------------------------------------------
PROJECT OVERVIEW
-----------------------------------------------------------------------------------------------------------
The following simulation models the longitudinal dynamics of a small aircraft given user prescribed initial
state conditions. The response of the aircraft is displayed in the form of time dependent paramers, including
body axis velocities, angular velocity, pitch angle, horizontal position, and altitude. Please read the project
report for a more detailed discussion.




-----------------------------------------------------------------------------------------------------------
TESTING PROCEDURE
-----------------------------------------------------------------------------------------------------------

To test this code, open and run 'UI.py.' The files 'simulation'|'forms|'constants' will need to be open in 
the same directory or will need to be accessible by the console through the same path.

-----------------------------------------------------------------------------------------------------------
TESTING GUIDE
-----------------------------------------------------------------------------------------------------------

The user interface offers two features:

1. Caluclate the required thrust and elevator angle to maintain an initial state or user inputted velocity 
and path angle

2. A graphic model displaying the time dependent response of following paramters as a function of a user 
prescribed initital state:

-Body axis velocities (ub and wb, the components of velocity in the x and z axis)

-Angular velocity (q)

-Pitch angle (theta)

-The horizontal positon of the airplane (XE)

-Altitude
 
 
When testing the response of the aircraft, it is recommended that the input values fall within the following 
range to achieve the most accraute response:

30 < velocity > 343

0 =< path angle > 90

10m < initial altitude > 3500m

400 < simulation run time > 1000

1 < Time Changes > 10

0 < Elevator angle change > 80 degrees

0 < Thrust changes > 1000
If the thrust is increased by more than 1000N, ensure an appropriate simulation time is chosen



-----------------------------------------------------------------------------------------------------------
Module and Class description
-----------------------------------------------------------------------------------------------------------

Below is a description of the modules and classes used in the simulation. More detail on the modules and classes
can be found at the top of each file and through in-code annotation.

| Module |
|--------------------------------------------------------------------------------------|
| Name        | Contents                  | Details                                    |
| ----------- | ------------------------- | ------------------------------------------ |
| simulation  | Main simulation A3 B1 B2  | Solves IVP for equations of motion         |
| constants   | A1  aerodynamic constants | Curve fitting coefficients and constants   |
| forms       | Relevant formulas         | Library for equations of motion and aircraft dynamics |
| UI          | Manages user interface    | Contains tkinter GUI code                  |

| Class |
|--------------------------------------------------------------------------------------|
| Name        | Contents/ Method          | Details                                    |
| ----------- | ------------------------- | ------------------------------------------ |
| Trim        | Initializing trim conditions based on user inputs | Solves for alpha [Newton-Raphson] |
| Visualize   | Plotting templates         | Called when graphing trim and simulation dynamics |
| A3          | SimControl                | Controls simulation for elevator angle and thrust |
| B1          | Trim for thrust and elevator angle | Trims the aircraft for a range of velocity and flight path angles, then plots for comparison |
| B2          | SimControl                | Calculates required climb time for group 07 specific velocity-plots airplane response |
































































