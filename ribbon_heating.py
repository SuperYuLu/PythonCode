#ribbon_heating.py

import numpy as np
import matplotlib.pyplot as plt

cap = 22e-3 #[F] Capacitance
ribbonRes = 0.2 #[Ohm] Ribbon resistance 
circuitRes = 0.05 #[Ohm] Circuit resistance
totalRes = ribbonRes + circuitRes #[Ohm] Total resistance in the circuit 
ribbonInduc = 2e-6 #[H] Ribbon inductance
volt = 300 #[V] Voltage on caps 
material = 'Nichrome'

ribbonThick = 2 * 0.001 * 0.0254 #[m] ribbon thickness
ribbonLen = 3 * 0.0254 # [m] ribbon length  
ribbonWidth = 0.20 * 0.0254 #[m] ribbon width
specificHeat = 450 #[J/(kg*K)] Specific heat of nichrom
massDensity = 8400 #[Kg/m^3] Density of nichrom
ribbonMass = massDensity * ribbonThick * ribbonLen * ribbonWidth #[Kg] mass of the ribbon


pulseLen = 70e-6 #[s] Ribbon pulse length
period = 3 #[s] Ribbon pulse period 
numPeriod = 6 # Number of period to calculation 
tStep = 5e-6 #[s] Time step for calculation 
t = np.linspace(0, period * numPeriod, period * numPeriod / tStep + 1)
U = np.ndarray((t.size,))

T0 = 30 + 273.16 #[k]
sigma = 5.6703e-8 #[W/(m^2 K^4)] Stefan-Boltzmann Constant

def calcu_current(t):
    u = np.ndarray((t.size,))
    i = 0
    for s in t: # Thru time
        for p in range(1,numPeriod+1): # Thru period
            if (p-1) * period <= s < p * period:
                start = (p - 1) * period
                continue
            if s == period:
                start = (p - 1) * period
        if (s - start) <= pulseLen:
            u[i] = volt * np.exp(-(s - start)/(totalRes * cap))
        else:
            u[i] = 0
        i = i + 1
    return u/totalRes

def calcu_temp_energy(t,initTemp):
    current = calcu_current(t)
    area = 2 * ribbonLen * ribbonWidth;
    temp = np.ndarray(t.size)
    elecTotal = 0
    dissiTotal = 0 
    temp[0] = initTemp
    dissiEng = 0
    elecEng = 0 
    for i in range(1,t.size):
        if temp[i-1] > initTemp:
            dissiEng = sigma * area * temp[i-1] ** 4 * tStep
        else:
            dissiEng = 0
        dissiTotal += dissiEng
        elecEng = current[i-1] ** 2 * ribbonRes * tStep
        elecTotal += elecEng
        deltaTemp = (elecEng - dissiEng) / (specificHeat * ribbonMass)
        temp[i] = deltaTemp + temp[i-1]
        
    return (temp, elecTotal, dissiTotal)

def run():
    temp, elecTotal, dissiTotal = calcu_temp_energy(t, T0)
    curr = calcu_current(t)
    fig = plt.figure(1)

    ax1 = fig.add_subplot(211)
    ax1.plot(t, curr, '-')
    ax1.set_title('Ribbon Current VS Time')
    ax1.set_xlabel('Time [s]')
    ax1.set_ylabel('Current [A]')
    ax1.text(0.8 * max(t), 0.8 * max(curr), \
             'Voltage :' + str(volt) + 'V\n' + \
             'Pulse length: ' + str(pulseLen*1e6) + 'us\n' + \
             'Period: ' + str(period) + 's\n' + \
             'Num of period: ' + str(numPeriod) +'\n', \
             fontsize = 12)

    ax2 = fig.add_subplot(212)
    ax2.plot(t, temp, 'o')
    ax2.set_title('Ribbon temperature V.S. Time')
    ax2.set_xlabel('time [s]')
    ax2.set_ylabel('Temperature [k]')
    ax2.text(0.8 * max(t), 0.8 * max(temp), \
             'Ribbon material: ' + material + '\n' + \
             'Ribbon Res: ' + str(ribbonRes) + 'Ohm\n' +\
             'Ribbon Induc: ' + str(ribbonInduc) + 'Ohm\n' + \
             'Circuit Res: ' + str(circuitRes) + 'Ohm\n' + \
             'Total Res: ' + str(totalRes) + 'Ohm',\
             fontsize = 12, color = 'black')

    plt.show()

run()
