#!/usr/bin/env python3

import libtools
import numpy as np

class Flight():
    def __init__(self):
        self.p0 = 1.225                                                                                 # Air Density | Sea level (kg/m^3)
        self.Pg = 0.1785                                                                                # Gas Density | Helium (kg/m^3)

        # Environment
        self.rEarth = 6.378e+06                                                                         # Earth Radius (m)
        self.g0 = 9.80665                                                                               # Gravity @ Surface - (m/s^2)
        self.atmos = libtools.load_config('profiles.yml')['us-standard']                                # Atmosphere Profile

        # Radiosonde Profile
        self.payload = 0.625                                                                            # Payload Mass (kg)
        self.parachute = 0.1                                                                            # Parachute Mass (kg)
        self.balloon = 0.3                                                                              # Balloon Mass (kg)
        self.rad = 0.615                                                                                # Launch Radius (m)
        self.Cd = 0.47                                                                                  # Drag Coefficient
        self.burst_alt = 24700                                                                          # Burst Altitude (m)
        self.burst_rad = 1.89                                                                           # Burst Radius (m)
        self.para_rad = 0.5                                                                             # Parachute Radius (m)
        self.para_Cd = 0.47                                                                             # Parachute Drag Coefficient
        self.status = 1                                                                                 # Status Code (Ascent = 1, Descent = 0)

    def balloon_dynamics(self, x, t):
        alt, vel = x

        # Launch
        V0 = self._rad2vol(self.rad)                                                                    # Launch Volume
        Mg = self._mass(self.Pg, V0)                                                                    # Mass of Gas
        Mtot = self.payload + self.balloon + Mg                                                         # Total Mass (Payload + Parachute + Balloon + Gas)
        Fp = 0.0                                                                                        # Parachute Force (Ascent)

        # Dynamic
        geo_alt = self._geopotential_altitude(self.rEarth, alt)                                         # Geometric Altitude
        rho_a = self._atmospheric_density(geo_alt)                                                      # Air / Fluid Density @ Altitude
        Vb = (self.p0 / rho_a) * V0                                                                     # Balloon Volume Update (m^3)
        rad = self._vol2rad(Vb)                                                                         # Balloon Radius Update (m)

        # Forces       
        if rad >= self.burst_rad: self.status = 0
        if self.status == 0:                                                                            # Descent Profile
            Vb = 0.0
            rad = 0.0
            Mtot = self.payload + self.balloon
            Fp = self._drag(self.para_rad, self.para_Cd, self._area(self.para_rad), rho_a, vel)         # Parachute Drag

        G = self._gravity_gradient(self.rEarth, geo_alt)                                                # Gravity @ Altitude
        Fb = self._bouyancy(rho_a, G, Vb)                                                               # Bouyancy (Archimedes' Principle)
        Fd = self._drag(rad, self.Cd, self._area(rad), rho_a, vel)                                      # Atmospheric Drag Force
        Fn = self._net_force(Fb, Mtot, G) - (Fd - Fp)                                                   # Net Force
        accel = self._acceleration(Fn, Mtot)                                                            # Acceleration (Newtons 2nd Law)

        Tv = self._terminal_velocity(Mtot, G, rho_a, self._area(self.para_rad), self.para_Cd)           # Terminal Velocity

        hrs, mins, secs = libtools.sec2time(t)
        print(f"Status: %i | Time: {hrs}h:{mins}m:{secs:.1f}s | Altitude: {geo_alt:.3f}m | Vel: {vel:.3f}m/s | Radius: {rad}m")

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

    def _drag(self, r, Cd, Ac, p, vel):
        return 0.5 * Cd * Ac * p * (vel**2)

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
    
    def _terminal_velocity(self, m, g, p, Ac, Cd):
        return np.sqrt((2 * m * g) / (p * Ac * Cd))

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