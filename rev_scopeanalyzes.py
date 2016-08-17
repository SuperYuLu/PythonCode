#rev_scopedata.py
'''
rev_scopedata.py
version: 2.0
Author: Yu Lu, Raizen Lab, CNLD, Dept. of Physics, UT Austin, Austin, Texas
Content: Functions to detect multiple peaks from data directory,
         including find data base level, peak arrival idx, peak arrival time,
         peak pulse length.
Email: yulu@utexas.edu
'''

from numpy import *
import matplotlib.pyplot as plt
import scipy.optimize as sopt
from warnings import warn


def load_PD_data(filename):# read in data
    data=loadtxt(filename,skiprows = 5,delimiter=',',usecols=(0,1))
    print('Data set *',filename,'* loaded')
    return data

def find_base_level(data): #find base level & its vary range (2nd maj)
    hist = histogram(data[:,1],50) # 50 as bin num, has to be large to avoid error
    idx_1 = hist[0].argmax() 
    p=0
    idx_2 = 0
    for i in range(0,hist[0].size):
        if hist[0][i] == hist[0].max():
            continue
        else:
            if hist[0][i]>p:
                p= hist[0][i]
                idx_2 = i
    base = (hist[1][idx_1] + hist[1][idx_1 + 1])/2
    major_2 = (hist[1][idx_2] + hist[1][idx_2 +1])/2
    diff = abs (base - major_2)
    return (base, diff)


def find_peak_idx(data,nstddiv=2): # detect peak and return the idx
    mean = data[:,1].mean()
    std = sqrt(data[:,1].var())
    mask = abs(data[:,1] - mean) > (nstddiv * std) # mask the peak region
    
    is_peak = False # peak identifier
    peak_idx = []
    peak = -100
    non_peak_steps = 0
    for i in range(0,mask.size):
        if mask[i]: # within peak regin, find max value (peak)
            if is_peak == False and non_peak_steps > 100:
                is_peak = True
                non_peak_steps = 0
            if data[i,1] >peak: # import: >, since peak is point upward
                peak = data[i,1]
                idx = i    
        else: # on peak edge, change identifier and save the peak value detected
            if is_peak == True :
                is_peak = False
                peak_idx.append(idx)
                peak = -100
            else:
                non_peak_steps += 1
                #print("No. %s peak arriving time: %s us\n"%(len(peak_idx),data[idx,0]*1e6))
    print('Found ',len(peak_idx),' peaks\n')
    return peak_idx
                    
def find_signal_inten(data, peak_idx, base, diff): # find the magnitude of each peak
    intensity = []
    for idx in peak_idx:
        inten = abs(data[idx,1] - base) - diff
        intensity.append(inten)
        #print("No.%s signal intensity is %s [V] \n" %(len(intensity), inten))
    return intensity



def find_pulse_width(data,peak_idx,base,diff): # find pulse length
    #find pulse width according to its dist to base level 
    pulse = []
    for idx in peak_idx:
        edge = False # peak edge indicator 
        k=0
        while edge == False:
            k += 1
            check1 =  abs(data[idx+k,1] - base) <= diff*3
            check2 = abs(data[idx-k,1] - base) <= diff*3
            if check1 and check2:
                edge = True
                width = data[idx+k,0] - data[idx-k,0]
                pulse.append(width)
                #print("No.%s peak pulse width is:%s us\n"%(len(pulse),width*1e6)) 
                
    return pulse





