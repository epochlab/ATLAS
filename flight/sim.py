#!/usr/bin/env python3

import engine, device

def main():
    HAB = device.Radiosonde()
    solver = engine.ODESolver(f=HAB.dynamics)

    x0 = [0.1, 0.0] # h=0m, v=0m/s
    dt = 0.1  # Time-step (0.001 = ms)

    solver.reset(x0, t_start=0.0); X, T = solver.compute(dt, "EULER") # Simulate

if __name__ == "__main__":
    main()