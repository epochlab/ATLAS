#!/usr/bin/env python3

import numpy as np

class ODESolver:
    def __init__(self, f):
        self.f = f
       
    def reset(self, x_start=None, t_start=0.0):
        self.x = x_start
        self.t = t_start

    def compute(self, dt, solver="MIDPOINT"):
        x0, x1, T = [self.x[0]], [self.x[1]], [self.t] # Init

        while self.x[0] > 0.0:
            if solver == "EULER":
                self.x += self.f(self.x, self.t) * dt
            elif solver == "MIDPOINT":
                x_mp = self.x + self.f(self.x, self.t) * dt/2
                self.x += self.f(x_mp, self.t + dt/2) * dt
            elif solver == "RK2":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt, self.t + dt)
                self.x += 0.5 * (k1 + k2) * dt
            elif solver == "RK4":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt/2, self.t + dt/2)
                k3 = self.f(self.x + k2 * dt/2, self.t + dt/2)
                k4 = self.f(self.x + k3 * dt, self.t + dt)
                self.x += 1/6 * (k1 + 2*k2 + 2*k3 + k4) * dt
            else:
                raise ValueError("Invalid solver method")

            self.t += dt

            x0.append(np.copy(self.x[0])) # Altitude
            x1.append(np.copy(self.x[1])) # Velocity
            T.append(self.t)

        return np.array([x0, x1]), T