#generate1.py

'''
Generate1.py 
Version: 3.0
Author: Yu Lu, Raizen Lab, CNLD,  Dept. of Physics, UT Austin, Texas, US
content:
    -load data files from setted directory
    -calling rev_scopeanalyzes.py to load bunch of functions to do peak
    detection, pulse width calculation, etc.
    -plot the peaks arrival time (commented out by default) and pulse 
    length for each data set
    -save plots to desired directory
Email: yulu@utexas.edu
'''

from rev_scopeanalyzes import *
from warnings import warn

data_folder = '/home/superlu/Documents/Python/CircuitTesting/20160307/'
data_save_folder = data_folder + 'results/'

No = linspace(1,9,9)
L_trap = 4.6
C = array([4,4,6,8,10,12,16,32,60])
L = array([0,0,0,0,2,4,8,16,30]) + L_trap
R = 0.15
T = pi * sqrt(C * L) / sqrt(1 - (R/2*sqrt(C/L))**2)

def generate(group):
    
    plt.figure(int(group))
    
    '''
    # This part is to see if all boards has the save peak arriving time
    # The result is that they all have exactly the same arriving time
    # So I just comment out this part and leave it in case needed

    plt.subplot(2,1,1) # plot the peak arriving time
    for i in range(0,3):
        name = data_folder + str(group)+str(i+1)+'C2.txt'
        data = load_PD_data(name)
        idx = find_peak_idx(data)
        if len(idx)>9: # increase the stddiv if find >14 peaks
            warn("more than 09 peaks detected")
            idx = find_peak_idx(data,4)

        if len(idx)!=9: # discard this data sets if still fails
            warn("Data too noisy, discard one set of data")
            print("Data too noisy, discard one set of data")
            continue
        No = linspace(1,len(idx),len(idx))
        plt.plot(No, data[idx,0]*1e6,'*')

    plt.xlim([-1,len(idx)+1])
    plt.ylabel("Peak arriving time (us)")
    plt.grid(True)
    plt.title("Pulse arriving time and Pulse width of BD No." + group)
    
    
    plt.subplot(2,1,2) # plot the pulse duration for each pulse
    '''
    print("[Loading data group No." + group + "]")
    print('--------------------------------------------')
    for i in range(0,3):
        name= data_folder + str(group)+str(i+1)+'C2.txt'
        print('Loading file', name, '...')
        data = load_PD_data(name)
        base, diff = find_base_level(data)
        idx = find_peak_idx(data,2)
        
        if len(idx)>9:
            warn("more than 09 peaks detected")
            print("Fixing extral peaks ...")
            idx = find_peak_idx(data,3)
        
        if len(idx)>9:
            warn("more than 14 peaks detected")
            print("Fixing extral peaks ...")
            idx = find_peak_idx(data,4)
    
        if len(idx)!=9:
            warn("Data too noisy, discard one set of data")
            print("Data too noisy, discard one set of data")
            continue
    
        pulse = find_pulse_width(data,idx,base,diff)
        No = linspace(1,len(idx),len(idx))
        plt.plot(No, array(pulse)*1e6,'o')
    plt.plot(linspace(1,9,9),T,'r^')    
    plt.xlim([-1,10])
    plt.xlabel("Peak No.")
    plt.ylabel("Pulse width (us)")
    plt.grid(True)
    plt.title("Pulse width of BD No." + group)

    plt.savefig(data_save_folder + 'pulseBD'+group+'.png')
    #plt.show()
    print('--------------------------------------------\n\n')

def main():
    for i in range(0,10):
        if i == 9:
            group = str(i+1)
        else:
            group = '0' + str(i+1)
        generate(group)
    plt.show()
    print("Plots saved in " + data_save_folder)

main()
