#OvenFluxcapillay
# Calculation the lithium atoms flux from capillay oven.
import numpy as np

# Capillary oven geometry 
d = 100e-6 # Capillay diameter 100 um (33RW gauge)
N = 528 # Total capillay number
l = 5e-3 # Capillay tube length

# Temperature
T = 550 + 273 # [k] Oven temp
k = 1.38065e-23 # Boltzmann const
m = 1.1624e-26 # [kg] lithum 7 mass

# Vapor preasure
p = 1e5 * 10 ** (4.98831 - (7918.984 / (T - 9.52))) # Liquid vapor pressure
# Li 7 values of 4.9 7918 -9.52 taken from Hicks, W.t. Evaluation of
#Vapor-Pressure Data of Mercury, Lithium, Sodium, and Potassium, J. Chem. Phys.,
#1963, 38, 8, 1873-1880.[doi:10.1063/1.1733889]

# Fraction of atom can come out of capillary, in fraction of pi,
#compare to effusive oven. 
fraction = np.arcsin(d / np.sqrt(l**2 + d**2)) / np.pi 
area = np.pi * (d / 2)**2 # Opening area of a sigle capillay
v = np.sqrt(3 * k * T / m) # [m/s] lithium 7 velocity
n = p/(k * T) # Atom density, Ideal Gas Law
flux = ( N * area * fraction * v * n ) / 4

print('[Capillary oven flux calculation]\n')
print('--Oven temperature: ', T - 273, ' C')
print('--Lithium flux: ', flux, ' atoms/s\n\n')

