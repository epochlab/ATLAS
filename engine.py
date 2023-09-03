#!/usr/bin/env python3

import numpy as np
from tqdm import trange

class ODESolver:
    def __init__(self, f):
        self.f = f
        self.x, self.t, self.ndim = [], [], []
       
    def reset(self, x_start, t_start):
        if isinstance(x_start, float):
            x_start = np.array([x_start])

        self.ndim = np.shape(x_start)[0]

        self.x = x_start
        self.t = t_start

    def compute(self, dt, niter, solver="rk4"):
        X = np.zeros([self.ndim, niter])
        T = np.zeros([niter])
        
        X[:,0] = np.copy(self.x)
        T[0] = np.copy(self.t)
        
        for n in (t := trange(1, niter)):
            if solver == "euler":
                self.x += self.f(self.x, self.t, True) * dt

            if solver == "midpoint":
                x_mp = self.x + self.f(self.x, self.t) * dt/2
                self.x += self.f(x_mp, self.t + dt/2, True) * dt

            if solver == "rk2":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt, self.t + dt, True)
                self.x += 0.5 * (k1 + k2) * dt

            if solver == "rk4":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt/2, self.t + dt/2)
                k3 = self.f(self.x + k2 * dt/2, self.t + dt/2)
                k4 = self.f(self.x + k3 * dt, self.t + dt, True)
                self.x += 1/6 * (k1 + 2*k2 + 2*k3 + k4) * dt
        
            X[:,n] = np.copy(self.x)
            self.t = self.t + dt
            T[n] = self.t

            t.set_description("Time: %.0fs | Altitude: %.2fm | Velocity: %.2fm/s" % (self.t, self.x[0], self.x[1]))

        return X, T