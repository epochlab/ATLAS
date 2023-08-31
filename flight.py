#!/usr/bin/env python3

class Environment:
    def __init__(self):
        self.name = 'Earth'

    def us_standard_atmosphere(self):
        # 1976 - Height (km), Pressure (pascals), Temp (°K), Temp Lapse Rate (°K/km)
        atmos = {
            'height': [0.0, 11.0, 20.0, 32.0, 47.0, 51.0, 71.0],
            'pressure': [101325.0, 22632.1, 5474.89, 868.019, 110.906, 66.9389, 3.95642],
            'temp': [288.15, 216.65, 216.65, 228.65, 270.65, 270.65, 214.65],
            'lapse_rate': [-6.5, 0.0, 1.0, 2.8, 0.0, -2.8, -2.0]
            }
        return atmos

class Balloon:
    def __init__(self):
        self.weight = 150

    def kaymont(self):
        # Balloon weight (g) > Burst diameter (m)
        balloon = {
            '150': 2.52,
            '200': 3.0,
            '300': 3.78,
            '350': 4.12,
            '500': 4.99,
            '600': 6.02,
            '800': 7.00,
            '1000': 7.86,
            '1200': 8.63,
            '1500': 9.44,
            '2000': 10.54,
            '3000': 13.00,
            }
        return balloon