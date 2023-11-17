# CMM Flight Simulator for the Longitudinal Dynamics of a Small aircraft: Group 07
## Overview
This simulation models the longitudinal dynamics of a small aircraft by outputting response curves of 
time-dependent variables. These variables include body axis velocities, angular velocity, pitch angle, 
horizontal displacement, and altitude. For more details about these responses, refer to the group report.

## Testing Procedure
To test the code, open the 'UI.py' file and ensure that the following files are open in the same directory or 
that they are accessible by the console:
- `forms.py`
- `constants`
- `simulation`

The UI can also be activated through the terminal after downloading the files in the same directory and 
running the following line |INSERT THE RUN COMMAND HERE|.

## Testing the Simulation
The code can be tested through the GUI and by changing specified parameters in 'simulation.py.'

### GUI Setup
The GUI can perform two tasks:
1. Output the required thrust and elevator angle given an initial state velocity and path angle (trimming).
2. Display the response of the aircraft’s time-dependent variables - body axis velocities (x and z axis), 
angular velocity, pitch angle, horizontal position, and altitude. These responses display after the user 
specifies the following parameters:
   - **Initial altitude:** Starting fight altitude
     - Recommended range h > 50m
   - **Simulation run time:** Duration of simulation
     - Recommended range: t = 10 * initializing time
   - **Parameter initializing time:** Time at which later elevator and thrust changes are activated
     - t > 10s
   - **Elevator angle:** Change in elevator angle at initializing time
     - A -60 < δ< 60 
   - **Thrust increase/decrease:** Change in thrust at initializing time
     - -600 < T < 600

The code can also be tested in ‘simulation.py’ by modifying the parameters for running parts A3 B1 and B2. 
Details on how to modify the parameters can be found in the in-code annotations.

## Module and Class Description
### Module
| Name        | Contents                  | Details                                    |
| ----------- | ------------------------- | ------------------------------------------ |
| simulation  | Main simulation A3 B1 B2  | Solves IVP for equations of motion         |
| constants   | A1  aerodynamic constants | Curve fitting coefficients and constants   |
| forms       | Relevant formulas         | Library for equations of motion and aircraft dynamics |
| UI          | Manages user interface    | Contains tkinter GUI code                  |

### Class
| Name        | Contents/ Method          | Details                                    |
| ----------- | ------------------------- | ------------------------------------------ |
| Trim        | Initializing trim conditions based on user inputs | Solves for alpha [Newton-Raphson] |
| Visualize   | Plotting templates         | Called when graphing trim and simulation dynamics |
| A3          | SimControl                | Controls simulation for elevator angle and thrust |
| B1          | Trim for thrust and elevator angle | Trims the aircraft for a range of velocity and flight path angles, then plots for comparison |
| B2          | SimControl                | Calculates required climb time for group 07 specific velocity-plots airplane response |
