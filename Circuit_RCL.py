# Circuit_RCL.py
# This script is for python3, to calculate the out put current and voltage
# with specific input of R, L, C and U

import numpy as np
import matplotlib.pyplot as plt

# Specify the input parameters here
l=4.6e-6 # [uH] Inductence selected from LBOX+coil inductance
c=32e-6 # [uH]Caps from CBOX
R=0.2 # Res of coil and cuicuit
U=200 # CBOX out put voltage

omiga0=1/np.sqrt(l*c) # w0 in RLC circuit
alpha=R/(2*l) # Attenuation coefficient
damping=R/2*np.sqrt(c/l) # Damping factor
omigad=omiga0*np.sqrt(1-damping**2) # Effective frequency
amp=U/(omigad*l ) # Amplitude of the current oscillation
t=np.linspace(0,500,501)*10**-6 # Generate time sequence
i=amp*np.exp(-alpha *t) *np.sin(omigad *t) # Current V.S. time
plt.figure(1) 
plt.plot(t,i,'b*-') # Plot current V.S. time
plt.xlabel( 'time (s)')
plt.ylabel('current(A)')
plt.title('Coil current V.S. time')


r=5.1*10**-3  # [Ohm]bore radius of coil
u=4*np.pi*10**-7  # constant u0
space=10*10**-3  # [m]coil to coil distance
dia=0.405*10**-3  # [m]Wire diameter

###
# Calculate Mag. field in coils 
B=0 # Initiate field magnitude
I=max(i) # Use max of I to calculate field
Z=np.linspace(-2.5, 2.5,80) *space   #position for calculating field

for j in range(0,4,1): # J goes from inner to outer layer of coils
    R=r+j*dia # Radius of j th layer of coil

    for k in range(0,4,1): # K goes the winding for each layer of front peak
        p1=space/2-1.5*dia+k*dia  # Center positon of each winding
        # Accumulate contribution of B from each winding
        B=B+u*I*R**2/2*1 /(((Z-p1) **2+R **2) **(3/2)) 

    for m in range(0,2,1): # M goes the winding for each layer of back peak
        p2=-(space/2-0.5*dia+m*dia)  # Center position of each winding
        # Accumulate contribution of B 
        B=B-u*I*r**2/2*1 /(((Z-p2) **2+R **2) **(3/2)) 
    
B=abs(B) # Only care about abs value
plt.figure(2) # Plot distribution B V.S. Z
plt.plot(Z *10**3,B,'b.-'), 
plt.title('MagField caulation ~ A')
plt.xlabel('position (mm)')
plt.ylabel('field (T)')
plt.show()





















