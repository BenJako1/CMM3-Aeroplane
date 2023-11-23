import numpy as np
import matplotlib.pyplot as plt
from scipy import integrate, optimize
import forms as f
import constants as c

#------------------------------------------------------------------------------
# Class for handling the intitial and user inputted trim conditons

class Trim:
    def __init__(self, trimVelocity, trimGamma):
        self.velocity = trimVelocity
        self.gamma = trimGamma
        
        # Solve for alpha
        initial_guess = 0.01  # Provide an initial guess
        self.alpha = optimize.newton(self.alpha_trim_func, initial_guess)
        
        # Solve for delta
        self.delta = -(c.CM0 + c.CMa * self.alpha) / c.CMde
    
        # Calculating other variables to output
        self.theta = self.alpha + trimGamma
        self.ub = trimVelocity * np.cos(self.alpha)
        self.wb = trimVelocity * np.sin(self.alpha)
    
        # Calculating thrust
        self.thrust = f.Engine_Thrust(self.alpha, self.delta, self.theta, trimVelocity)
        
    def alpha_trim_func(self, alpha):
        self.delta = -(c.CM0 + c.CMa * alpha) / c.CMde

        return (-f.Lift(alpha, self.delta, self.velocity) * np.cos(alpha) 
                - f.Drag(alpha, self.delta, self.velocity) * np.sin(alpha) 
                + c.mass * c.gravity * np.cos(alpha + self.gamma))

#------------------------------------------------------------------------------
# Class to display data from other classes: plotting dynamic behavior and trim conditions

class Visualise():
    
    # Plotting aircraft parameter response
    def Display_Sim(self, Data):
        # Split data into components
        self.t = Data.t
        self.q = Data.y[0]
        self.theta = np.rad2deg(Data.y[1])
        self.ub = Data.y[2]
        self.wb = Data.y[3]
        self.xe = Data.y[4]
        self.ze = Data.y[5]
        
        # Calculate altitude because ze is inverted during calculation
        self.altitude = self.ze * -1

        fig, ax = plt.subplots(3, 2, figsize=(9, 7))

        ax[0, 0].plot(self.t, self.ub)
        ax[0, 0].set_title("$u_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 0].set_ylabel("$u_{B}$ [m/s]")
        ax[0, 0].set_xlabel("t [s]")

        ax[0, 1].plot(self.t, self.wb)
        ax[0, 1].set_title("$w_{B}$ Body Axis Velocity vs Time", fontsize=12)
        ax[0, 1].set_ylabel("$w_{B}$ [m/s]")
        ax[0, 1].set_xlabel("t [s]")
        
        ax[1, 1].plot(self.t, self.theta)
        ax[1, 1].set_title("${\Theta}$ Pitch Angle vs Time", fontsize=12)
        ax[1, 1].set_ylabel("${\Theta}$ [$^{0}$]")
        ax[1, 1].set_xlabel("t [s]")

        ax[1, 0].plot(self.t, self.q)
        ax[1, 0].set_title("q Angular Velocity vs Time", fontsize=12)
        ax[1, 0].set_ylabel("q [rad/s]")
        ax[1, 0].set_xlabel("t [s]")

        ax[2, 0].plot(self.t, self.xe)
        ax[2, 0].set_title("$x_{E}$ Horizontal Position vs Time", fontsize=12)
        ax[2, 0].set_ylabel("$x_{e}$ [m]")
        ax[2, 0].set_xlabel("t [s]")

        ax[2, 1].plot(self.t, self.altitude)
        ax[2, 1].set_title("h Altitude  vs Time", fontsize=12)
        ax[2, 1].set_ylabel("Altitude h [m]")
        ax[2, 1].set_xlabel("t [s]")

        plt.tight_layout()

        return fig
    
    def Display_Trim_Conditions(self, V_values, gamma_values, T_values, delta_values):
       plt.figure(figsize=(14, 10))

       # Plot Thrust vs Velocity
       plt.subplot(2, 2, 1)
       for j, gamma in enumerate(gamma_values):
           plt.plot(V_values, T_values[:, j], label=f'γ = {np.rad2deg(gamma):.1f}°')
       plt.xlabel('Velocity V [m/s]')
       plt.ylabel('Thrust [N]')
       plt.title('Thrust vs. Velocity')
       plt.legend()

       # Plot Elevator Angle vs Velocity
       plt.subplot(2, 2, 2)
       for j, gamma in enumerate(gamma_values):
           plt.plot(V_values, delta_values[:, j], label=f'γ = {np.rad2deg(gamma):.1f}°')
       plt.xlabel('Velocity V [m/s]')
       plt.ylabel('Elevator Angle δₑ [$^{0}$]')
       plt.title('Elevator Angle vs. Velocity')
       plt.legend()

       # Plot Thrust vs gamma
       plt.subplot(2, 2, 3)
       for i, V in enumerate(V_values):
           plt.plot(gamma_values, T_values[i, :], label=f'V = {V} m/s')
       plt.xlabel('Flight Path Angle γ [$^{0}$]')
       plt.ylabel('Thrust [N]')
       plt.title('Thrust vs Flight Path Angle')
       plt.legend()

       # Plot Elevator Angle vs Flight Path Angle
       plt.subplot(2, 2, 4)
       for i, V in enumerate(V_values):
           plt.plot(gamma_values, delta_values[i, :], label=f'V = {V} m/s')
       plt.xlabel('Flight Path Angle γ [$^{0}$]')
       plt.ylabel('Elevator Angle δₑ [$^{0}$]')
       plt.title('Elevator Angle vs Flight Path Angle')
       plt.legend()

       plt.tight_layout()

       plt.show()

#------------------------------------------------------------------------------
# Calculates trim conditions for a range of input values

class Trim_Conditions(Visualise):
    def __init__(self, V_min, V_max, gamma_min, gamma_max, V_step, gamma_step):
        self.V_min = V_min
        self.V_max = V_max
        self.gamma_min = gamma_min
        self.gamma_max = gamma_max

        self.V_step = V_step
        self.gamma_step = gamma_step

        self.V_values = np.arange(self.V_min, self.V_max, self.V_step)
        self.gamma_values = np.arange(self.gamma_min, self.gamma_max, self.gamma_step)

        self.T_values = np.empty((len(self.V_values), len(self.gamma_values)))
        self.delta_values = np.empty((len(self.V_values), len(self.gamma_values)))

        for i, V in enumerate(self.V_values):
            for j, gamma in enumerate(self.gamma_values):
                trim_condition = Trim(V, np.deg2rad(gamma))

                self.T_values[i, j] = trim_condition.thrust
                self.delta_values[i, j] = np.rad2deg(trim_condition.delta)
        
        self.Display_B1(self.V_values, self.gamma_values, self.T_values, self.delta_values)
#-------------------------------------------------------------------------------------------------------------------------
# Determines the time required to climb a specified height at a specified angle and velocity

class Climb_Time(Visualise):
    def __init__(self, trimVelocity, trimGamma, t_end, initialAltitude, maxAltitude, pitchTime, climbVelocity, climbGamma, climbTimeGuess = 0, climbStep = 0.5):
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        trimParams2 = Trim(climbVelocity, climbGamma)
        self.Trim2 = trimParams2
        
        self.climbTime = climbTimeGuess
        self.pitchTime = pitchTime
        
        finalAltitude = initialAltitude
        
        while finalAltitude < maxAltitude:
            y = integrate.solve_ivp(self.SimControl, [0,t_end], [0,trimParams.theta, trimParams.ub, trimParams.wb, 0, -initialAltitude], t_eval=np.linspace(0,t_end,t_end*50))
            finalAltitude = -y.y[5][len(y.y[5])-1]
            
            self.climbTime += climbStep
            
        # Send data to "Display" function to be plotted
        self.Display_Sim(y)
        
        print(f"Climb Duration: {self.climbTime}s")
    
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        if t > self.pitchTime and t < self.pitchTime + self.climbTime:
            delta = self.Trim2.delta
            thrust = self.Trim2.thrust
        else:
            delta = self.Trim.delta
            thrust = self.Trim.thrust

        return f.Equations(t, y, delta, thrust)

#--------------------------------------------------------------------------------------------------------------------------
# Simulation of flight - called by UI

class Simulation(Visualise):
    def __init__(self, trimVelocity, trimGamma, t_end, initialAltitude, time_changes):
        self.time_changes = time_changes
        
        trimParams = Trim(trimVelocity, trimGamma)
        self.Trim = trimParams
        
        self.data = integrate.solve_ivp(self.SimControl, [0, t_end], [0, trimParams.theta, trimParams.ub, trimParams.wb, 0, -initialAltitude], t_eval=np.linspace(0, int(t_end), int(t_end * 50)))
        
        self.Display_Sim(self.data)
    
    # Function to change delta and thrust during IVP calculations
    def SimControl(self, t, y):
        delta = self.Trim.delta
        thrust = self.Trim.thrust
        #A3 parameter control
        for change_time, delta_change, thrust_change in self.time_changes:
            if t > change_time:
                delta += delta_change
                thrust += thrust_change

        return f.Equations(t, y, delta, thrust)


#----------------------------------------------------------------------------------------------------------
# Debugging, uncomment and change commands as needed

if __name__ == "__main__":
    
    sim = Simulation(100, 0, 300, 2000, [(100.0, -0.0052, 0.0), (300.0, 0.002, 0.0)])
    sim.Display_Sim(sim.data)

    #B1(V_min=50, V_max=200, gamma_min=-2, gamma_max=2.5, V_step=10, gamma_step=0.5)
      
    #Climb_Time(trimVelocity=109, trimGamma=0, t_end=700, initialAltitude=1000, maxAltitude=2000, pitchTime=10, climbVelocity=109, climbGamma=np.deg2rad(2), climbTimeGuess=200, climbStep=1)

