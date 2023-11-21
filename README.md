# CMM Flight Simulator for the Longitudinal Dynamics of a Small aircraft: Group 07
## Overview
This simulation models the longitudinal dynamics of a small aircraft by outputting response curves of time-dependent variables. These variables include body axis velocities, angular velocity, pitch angle, horizontal displacement, and altitude. The full repository can be found on [GitHub](https://github.com/BenJako1/CMM3-Aeroplane)

## Running
Once the code in downloaded, navigate to the code directory using the command line (terminal on MacOS). Install the required packages with `pip install -r requirements.txt` and run the code using the following command `python UI.py` in the command line. The code can also be run from a IDE like Spyder or VSCode by running UI.py.

## Testing the Simulation
Other aspects of the code can be tested in ‘simulation.py’. This is done simply with uncommenting the function calls at the bottom and experimenting with input values. In this manner, trim conditions can be found for ranges of velocity and path angle (B1) as well as a calculation for the time required to climb a specified altitude (B2).

### GUI Setup
The GUI can perform two tasks:
1. Output the required thrust and elevator angle given an initial state velocity and path angle (trimming). These values are range-capped to prevent unstable simulations.
2. Display the response of the aircraft’s time-dependent variables - body axis velocities (x and z axis), angular velocity, pitch angle, horizontal position, and altitude. These responses display after the user specifies the following parameters:
   - **Initial altitude:** Starting fight altitude
   - **Simulation run time:** Duration of simulation
   - **Input time:** Time at which later elevator and thrust changes are activated, comma-seperated values accepted e.g. 100, 500, 600
   - **Change in elevator angle:** Change in elevator angle at input time comma-seperated values accepted e.g. -0.1, 0, 0.1
   - **Change in thrust:** Change in thrust at input time, comma-seperated values accepted e.g. 500, 0, -500

Note: There is no range cap on the simulation inputs. The user can test the limits of the simulation without restrictions but will encounter unusual results at large input values.

When running "simulation", the program will give a warning for values that may result in unstable graphs (i.e. low velocities where the plane cannot generate enough lift) but will still display graphs. For non-sensical values e.g. negative velocities, the graphs will not display.

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
