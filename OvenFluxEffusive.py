#OvenFluxEffusive.py
# Calculaiton of the lithium flux from effusive oven.

import numpy as np

T = 550 + 273 #[k] Oven temperature

d_oven = 5e-3 #[m] oven opening diameter
d_Li = 0.304e-9 #[m] Lithium atom diameter

k = 1.38065e-23 # Boltzmann const
m = 1.1624e-26 # [kg] lithium 7 mass

p = 1e5 * 10 ** (4.98831 - (7918.984 / ( T - 9.52))) #[pa]vapor pressure lithium

area = np.pi * (d_oven / 2)**2 # Oven openning area
v = np.sqrt(3 * k * T / m) # Velocity of Lithium
n = p / (k * T) # Lithium 7

flux = n * v * area / 4 # Lithium flux out of oven openning
print('[Lithium flux calculation, effusive oven]\n')
print('Oven Temperature:', T-273, 'C')
print('Lithium flux: ', flux, ' atom/sec\n')
