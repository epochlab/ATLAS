#!/usr/bin/env python3

import math

def volume(rad):
    return 4 / 3 * math.pi * rad ** 3

def mass(p, V):
    return p * V

def bouyancy(p, g, V):
    return p * g * V

def net_force(Fb, Mtotal, g):
    return Fb - (Mtotal * g)

def accel(Fn, Mtotal):
    return Fn / Mtotal

def gravity_gradient(g0, r, z):
    return g0 * ((r / (r + z)) ** 2)

def geopotential_altitude(r, z):
    return (r * z) / (r + z)