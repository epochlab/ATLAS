#!/usr/bin/env python3

import engine

import numpy as np
import matplotlib.pyplot as plt

def main():
    HAB = engine.Flight()
    solver = engine.ODESolver(f=HAB.balloon_dynamics)

    x0 = np.array([1000.0, 0.0]) # h=0m, v=0m/s
    dt = 0.1  # Time-step (0.001 = ms)

    solver.reset(x0, t_start=0.0); X, T = solver.compute(dt, "euler") # Simulate

if __name__ == "__main__":
    main()