#WreDetectorTemp.py
'''
---------------------------------------------------------------
Calculation of hot rehinium wire (ribbon) temperature 
Calculation is base on the paper ->
"Optimization of a Langmuir-Taylor detector for lithium"
The physics is based on the equlibrium between the input 
power due to Joule effect and radiative losses
---------------------------------------------------------------
'''

from sympy import Eq, Symbol, solve
import numpy as np

T = Symbol('T')
I = float(input("Input the current in rehinium ribbon [A]:"))
a = 0.001 * 0.0254 #[m] ribbon thickness
b = 0.0315 * 0.0254 #[m] ribbon width
rho = 26.0e-8 * (1 + 1.27e-3 * T) #[Ohm*m] Resistivity
epsilon = 0.0852 * (1 + 1.15e-3 * T)  # total emittance
sigma = 5.670e-8 #[WM^-2K^-4] Stefan_Boltzmann constant

eqn = Eq(rho * I ** 2 / (a * b), epsilon * sigma * T ** 4 * 2 * (a+b))
t = solve(eqn)

print('Rehinium ribbon Temperature [k] : ', t)

