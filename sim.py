#!/usr/bin/env python3

import engine

import numpy as np
import matplotlib.pyplot as plt

# Init conditions
physics = engine.Flight()
solver = engine.ODESolver(f=physics.balloon_dynamics)

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