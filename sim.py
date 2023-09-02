#!/usr/bin/env python3

import engine

import numpy as np
import matplotlib.pyplot as plt

# Constants
profile = {}
profile['fluid'] = 1.225            # Fluid Density | Air (kg/m^3)
profile['gas'] = 0.1785             # Gas density | Helium (kg/m^3)
profile['gravity'] = 9.80665        # Gravity
profile['payload'] = 0.625          # Payload Mass (kg)
profile['balloon_mass'] = 0.3       # Balloon Mass (kg)

# Balloon parameters
radius = 1.23 # m
V = 4 / 3 * np.pi * radius ** 3
mass_gas = profile['gas'] * V
total_mass = profile['payload'] + profile['balloon_mass'] + mass_gas

Fb = profile['fluid'] * profile['gravity'] * V # Archimedes' principle (Bouyancy)
Fn = Fb - (total_mass * profile['gravity']) # Net force
accel = Fn / total_mass # Acceleration

print(f"Volume of the balloon: {V:.2f} m^3")
print(f"Mass of the helium: {mass_gas:.2f} kg")
print(f"Total mass: {total_mass:.2f} kg")
print(f"Buoyant force: {Fb:.2f} N")
print(f"Net force: {Fn:.2f} N") # Equilibrium @ zero (static)
print(f"Acceleration: {accel:.2f} m/s^2")

def balloon_dynamics(x, t):
    _, v = x
    dh_dt = v
    dv_dt = accel
    return np.array([dh_dt, dv_dt])

model = engine.ODESolver(f=balloon_dynamics)

# Init conditions 
x0 = np.array([0.0, 0.0]) # h=0m, v=0m/s
dt = 0.1  # s
Tmax = 100

model.reset(x0, t_start=0.0); X, T = model.runge_kutta4(dt, Tmax)

# Height
plt.figure(figsize=(10,5))
plt.subplot(2, 1, 1)
plt.plot(T, X[0,:], 'k-', lw=1)
plt.title('Height vs Time')
plt.xlabel('Time (s)'), plt.ylabel('Height (m)')
plt.xlim(0,(Tmax*dt)-dt), plt.grid(alpha=0.25)

# Velocity
plt.subplot(2, 1, 2)
plt.plot(T, X[1,:], 'r--', lw=1)
plt.title('Velocity vs Time')
plt.xlabel('Time (s)'), plt.ylabel('Velocity (m/s)')
plt.xlim(0,(Tmax*dt)-dt), plt.grid(alpha=0.25)
plt.tight_layout()
plt.show()