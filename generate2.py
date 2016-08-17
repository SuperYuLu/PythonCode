#generate2.py

from rev_scopeanalyzes import *
from warnings import warn

def generate():
    
    ave=ndarray((10,14))
    stddiv= ndarray((10,14))
    fig, ax = plt.subplots()
    for j in range(0,10): # generate the group name
        if j < 9 :
            group = '0' + str(j+1)
        else:
            group = str(j+1)
        pulse = {}
        for i in range(0,3):
            
            name='./20160126/'+group+str(i+1)+'.CSV'
            data = load_PD_data(name,2)
            base, diff = find_base_level(data)
            idx = find_peak_idx(data)
            if len(idx)>14:
                warn("more than 14 peaks detected")
                idx = find_peak_idx(data,4)
            '''
        if len(idx)>14:
            warn("more than 14 peaks detected")
            idx = find_peak_idx(data,5)
        '''
            if len(idx)!=14:
                warn("Data too noisy, discard one set of data")
                continue
            pulse[i] = find_pulse_width(data,idx,base,diff)
        for k in range(0,14):
            ave[j,k] = average([pulse[0][k],pulse[1][k],pulse[2][k]])*1e6
            stddiv[j,k] = std([pulse[0][k],pulse[1][k],pulse[2][k]])*1e6

        No = linspace(1,14,14)
        ax.errorbar(No, ave[j,:], yerr = stddiv[j,:], fmt = 'o',label=str(j+1))
    legend = ax.legend(loc = 'upper left', shadow = True)
    plt.title('Pulse duration analyzes of 10 boards, each with 14 pulses')
    plt.xlabel('No. of pulses')
    plt.ylabel('Pulse duration (us)')
    
    plt.show()
