#!/usr/bin/env python3

import math

# Constants
g = -9.80665  # Gravity (m/s^2)
p = 1.225  # Fluid density (kg/m^3)
He = 0.1786  # Gas density (kg/m^3)

# Balloon parameters
radius = 0.15 # m
V = 4 / 3 * math.pi * radius ** 3
mass_balloon = 0.02
mass_He = He * V
total_mass = mass_balloon + mass_He

Fb = p * g * V # Archimedes' principle (Bouyancy)
Fn = Fb - (total_mass * g) # Net force
accel = Fn / total_mass # Acceleration

print(f"Volume of the balloon: {V} m^3")
print(f"Mass of the helium: {mass_He} kg")
print(f"Total mass: {total_mass} kg")
print(f"Buoyant force: {Fb} N")
print(f"Net force: {Fn} N")
print(f"Acceleration: {accel} m/s^2")

# Init
height = 0.1
velocity = 0
time = 0
time_step = 0.1
i = 0

# Simulate
while height > 0.0:
    print(f"ID: {i}, Time (s): {time:.2f}, Height (m): {height:.2f}m, Velocity (m/s): {velocity:.2f}")

    velocity += accel * time_step
    height += velocity * time_step
    time += time_step

    i += 1

    if height >= 1000.0:
        print("Balloon has exploded.")
        break