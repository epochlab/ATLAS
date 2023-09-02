#!/usr/bin/env python3

import engine, flight

import numpy as np
import matplotlib.pyplot as plt

def balloon_dynamics(x, t, status=False):

    h, v = x                                            # Input

    # Constants
    Pf = 1.293                                          # Fluid Density | Air (kg/m^3)
    Pg = 0.1785                                         # Gas Density | Helium (kg/m^3)
    payload = 0.625                                     # Payload Mass (kg)
    balloon = 0.3                                       # Balloon Mass (kg)
    rEarth = 6.378e+06                                  # Earth Radius (m)

    # Launch dimensions
    r0 = 1.0
    V0 = flight.volume(r0)
    Mg = flight.mass(Pg, V0)
    Mtotal = payload + balloon + Mg
    
    g0 = 9.80665                                        # Gravity - (m/s^2)
    h_geom = flight.geopotential_altitude(rEarth, h)    # Geometric Altitude
    G = flight.gravity_gradient(g0, rEarth, h_geom)     # Gravity @ Altitude

    rad = 1.0                                           # Balloon Radius Update (m)******
    V = flight.volume(rad)                              # Balloon Volume Update (m^3)

    Fb = flight.bouyancy(Pf, G, V)                      # Bouyancy (Archimedes' Principle)
    Fn = flight.net_force(Fb, Mtotal, G)                # Net Force (Free-lift)
    accel = flight.accel(Fn, Mtotal)                    # Acceleration (Newtons 2nd Law)

    if status == True:
        print(f"Time: {t:.2f}s, Altitude: {h_geom:.2f}m, Velocity: {v:.2f}m/s")

    dh_dt = v
    dv_dt = accel
    return np.array([dh_dt, dv_dt])

# Init conditions
solver = engine.ODESolver(f=balloon_dynamics)

x0 = np.array([0.1, 0.0]) # h=0m, v=0m/s
dt = 0.1  # secs
Tmax = 10

# Simulate
solver.reset(x0, t_start=0.0); X, T = solver.compute(dt, int(Tmax/dt), "rk4")

# # Height
# plt.figure(figsize=(10,5))
# plt.subplot(2, 1, 1)
# plt.plot(T, X[0,:], 'k-', lw=1)
# plt.title('Height vs Time')
# plt.xlabel('Time (s)'), plt.ylabel('Height (m)')
# plt.xlim(0,Tmax-dt), plt.grid(alpha=0.25)

# # Velocity
# plt.subplot(2, 1, 2)
# plt.plot(T, X[1,:], 'r--', lw=1)
# plt.title('Velocity vs Time')
# plt.xlabel('Time (s)'), plt.ylabel('Velocity (m/s)')
# plt.xlim(0,Tmax-dt), plt.grid(alpha=0.25)
# plt.tight_layout()
# plt.show()

# Radius & Volume update
# Burst Radius
# Temperture
# Drag???
# Air Density Update > Bouyancy update
# Time & Payload