#!/usr/bin/env python3

import libtools

import numpy as np
from tqdm import trange

class Flight():
    def __init__(self):
        self.p0 = 1.225                                             # Air Density | Sea level (kg/m^3)
        self.Pg = 0.1785                                            # Gas Density | Helium (kg/m^3)

        # Environment
        self.rEarth = 6.378e+06                                     # Earth Radius (m)
        self.g0 = 9.80665                                           # Gravity @ Surface - (m/s^2)
        self.atmos = libtools.load_config('config.yml')['us-standard']

        # Radiosonde
        self.payload = 0.625                                        # Payload Mass (kg)
        self.balloon = 0.3                                          # Balloon Mass (kg)
        self.rad = 0.615                                            # Launch Radius (m)
        self.drag_coeff = 0.47                                      # Drag Coefficient
        self.burst_alt = 24700                                      # Burst Altitude (m)
        self.burst_rad = 1.89                                       # Burst Radius (m)
        self.para_rad = 0.5                                         # Parachute Radius (m)
        self.para_drag_coeff = 0.78                                 # Parachute Drag Coefficient
        self.status = "Ascending"                                   # Status Code

    def balloon_dynamics(self, x, t):
        h, vel = x                                                  # Input

        # Launch
        V0 = self._rad2vol(self.rad)                                # Launch Volume
        Mg = self._mass(self.Pg, V0)                                # Mass of Gas
        Mtot = self.payload + self.balloon + Mg                     # Total Mass (Payload + Balloon + Gas)

        # Dynamic
        h_geo = self._geopotential_altitude(self.rEarth, h)         # Geometric Altitude
        rho_a = self._atmospheric_density(h_geo)                    # Air / Fluid Density @ Altitude
        V_a = (self.p0 / rho_a) * V0                                # Balloon Volume Update (m^3)
        rad_a = self._vol2rad(V_a)                                  # Balloon Radius Update (m)

        # Forces
        G = self._gravity_gradient(self.rEarth, h)                  # Gravity @ Altitude

        Fp = 0.0
        if rad_a >= self.burst_rad:
            self.status = "Descending"

        if self.status == "Descending":
            V_a = 0.0
            rad_a = 0.0
            Fp = self._drag(self.para_rad, self.para_drag_coeff, rho_a, Mtot*G)     # Parachute Drag Force ????

        Fb = self._bouyancy(rho_a, G, V_a)                          # Bouyancy (Archimedes' Principle)
        Fd = self._drag(rad_a, self.drag_coeff, rho_a, vel)         # Balloon Drag Force
        Fn = self._net_force(Fb, Mtot, G) - (Fd + Fp)               # Net Force (Free-lift)
        accel = self._acceleration(Fn, Mtot)                        # Acceleration (Newtons 2nd Law)

        # t_vel = self._terminal_velocity(Mtot, G, rho_a, rad_a, self.drag_coeff) # Terminal Velocity (m/s)

        if int(t*1000 % 1000) == 0:
            print("Status: %s | Time: %.2fs | Alt: %.2fm | Vel: %.2fm/s | Radius: %.3fm | Volume: %.2fm" % (self.status, t, h_geo, vel, rad_a, V_a))

        dh_dt = vel
        dv_dt = accel
        return np.array([dh_dt, dv_dt])

    def _rad2vol(self, r):
        return 4 / 3 * np.pi * r ** 3

    def _vol2rad(self, V):
        return (3 * V / (4 * np.pi)) ** (1 / 3)
    
    def _area(self, r):
        return np.pi * (r**2)

    def _mass(self, p, V):
        return p * V

    def _bouyancy(self, p, g, V):
        return p * g * V

    def _net_force(self, Fb, Mtotal, g):
        return Fb - (Mtotal * g)

    def _acceleration(self, Fn, Mtotal):
        return Fn / Mtotal

    def _drag(self, r, Cd, p, vel):
        return 0.5 * Cd * self._area(r) * p * (vel**2)

    def _gravity_gradient(self, r, z):
        return self.g0 * ((r / (r + z)) ** 2)
    
    def _geopotential_altitude(self, r, z):
        return (r * z) / (r + z)

    def _atmospheric_density(self, z):
        band = 0
        for alt in self.atmos['geopotential_altitude']:
            if alt <= z and alt != 0:
                band += 1

        P = self.atmos['static_pressure'][band]
        T = self.atmos['standard_temp'][band]
        R = 287.058 # Dry Air

        return P / (R * T)
    
    def _terminal_velocity(self, m, g, p, r, Cd):
        return np.sqrt((2*m*g) / (p*self._area(r)*Cd))

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
  
    def compute(self, dt, solver="rk4"):
        X = []
        T = []
        
        X.append(np.copy(self.x))
        T.append(np.copy(self.t))

        while self.x[0] > 0.0:
            if solver == "euler":
                self.x += self.f(self.x, self.t) * dt

            if solver == "midpoint":
                x_mp = self.x + self.f(self.x, self.t) * dt/2
                self.x += self.f(x_mp, self.t + dt/2) * dt

            if solver == "rk2":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt, self.t + dt)
                self.x += 0.5 * (k1 + k2) * dt

            if solver == "rk4":
                k1 = self.f(self.x, self.t)
                k2 = self.f(self.x + k1 * dt/2, self.t + dt/2)
                k3 = self.f(self.x + k2 * dt/2, self.t + dt/2)
                k4 = self.f(self.x + k3 * dt, self.t + dt)
                self.x += 1/6 * (k1 + 2*k2 + 2*k3 + k4) * dt

            X.append(np.copy(self.x))
            T.append(self.t + dt)

        return X, T