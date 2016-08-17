#fieldAnalyze.py

import numpy as np
import matplotlib.pyplot as plt
import os

def load_data(filename):
    data = np.loadtxt(filename, skiprows = 5,usecols=(2,3))
    print('Data file: ', filename, ' loaded')
    return data

def find_position(filename):
    idx1 = filename.index('_')
    idx2 = filename.index('_',idx1+1)
    idx3 = filename.index('_',idx2+1)
    if filename[idx1+1] == '-':
        p1 = -int(filename[idx1+2:idx2])
    else:
        p1 = int(filename[idx1+1:idx2])
    if filename[idx2+1] == '-':
        p2 = -int(filename[idx2+2:idx3])
    else:
        p2 = int(filename[idx2+1:idx3])
    position = (p1 - p2) * 0.005 #step size: 0.005 mm/step
    return position

def peak_average(data,peakIdx,intensity):
    peaks = []
    base = []
    searchRange = 20
    for idx in peakIdx:
        for i in range(int(idx-searchRange*3),int(idx-searchRange/2)):
            base.append(data[i])
        for i in range(int(idx+searchRange/2),int(idx+searchRange*3)):
            base.append(data[i])
        baseline = float(sum(base)/len(base))
        peak = baseline
        for i in range(int(idx-searchRange/2),int(idx+searchRange/2)):
            if data[idx] > baseline:
                if data[i] > peak:
                    peak = data[i]
                else:
                    continue
            if data[idx] < baseline:
                if data[i] < peak:
                    peak = data[i]
                else:
                    continue
        if baseline < 0.5 * intensity: #Sig from prependicular polar dir
            peaks.append(peak-baseline)
        else:
            peaks.append(peak) #Sig from initial polarization dir
    peak_mean = abs(np.mean(peaks))
    peak_std = np.std(peaks)
#    intensity = intensity *2.38/0.75 # Consider the difference of gain

    if baseline < 0.5 * intensity:
        theta = np.arcsin(np.sqrt(peak_mean/(intensity-baseline)))
        theta_std = 1/(2*intensity*np.sqrt(peak_mean/intensity*(1-peak_mean/intensity))) * peak_std
    else:
        theta = np.arccos(np.sqrt(peak_mean/baseline))
        theta_std = -1/(2*intensity*np.sqrt(peak_mean/intensity*(1-peak_mean/intensity))) * peak_std
    B = abs(theta/(134*0.0029))
    B_std = abs(theta_std/(134*0.0029))
    return (B, B_std)

            
def print_test_voltage(voltage):
    datadir = coildir + voltage 
    files = os.listdir(datadir)
    peak_pos_value = np.zeros([len(files),3]) #position, value, std
    peak_pos_value_sorted = np.zeros([len(files),3])
    peakidx = np.loadtxt(coildir + '/peakidx.txt')
    for i in range(0,len(files)):
        data = load_data(datadir + '/' + files[i])
        intensity = np.average(data[:,0])
        peak_pos_value[i,0] = find_position(files[i])
        peak_pos_value[i,1], peak_pos_value[i,2]= peak_average(data[:,1], peakidx,intensity)
    peak_pos_value_sorted[:,:] = sorted(peak_pos_value, key = lambda x: x[0])
    front_max_idx = np.argmax(peak_pos_value_sorted[:,1])
    front_max = peak_pos_value_sorted[front_max_idx,1]
    back_max = max(peak_pos_value_sorted[front_max_idx+10:,1])
    plt.figure(1)
    plt.errorbar(peak_pos_value_sorted[:,0],peak_pos_value_sorted[:,1],yerr=peak_pos_value_sorted[:,2],fmt='s-',label = 'I='+str(int(voltage[:-1])*np.sqrt(C/L))+'A')
    return (front_max, back_max)


     
coildir = '/home/superlu/Documents/Python/TGGCrystalTest/42R05NEW/'
C = 32.0 #uF
L = 21.0 #uH
voltages = [115, 165, 220, 260, 320]
currents = voltages * np.sqrt(C/L)
print(currents)
field_max = np.zeros([len(voltages),2]) #Front end max, back end max

for i in range(0,len(voltages)):
    field_max[i,0],field_max[i,1] =  print_test_voltage(str(voltages[i])+'v')


plt.figure(1)
plt.title("Magnetic Field measurement with TGG crystal, parallel poloriaztion")
plt.xlabel("Position (mm)")
plt.ylabel("Field (T)")
plt.legend()

plt.figure(2)
plt.plot(currents, field_max[:,0], 'rs', label = "Coil field front peak")
plt.plot(currents, field_max[:,1],'b^', label = "Coil field back peak")
plt.title("Coil field peak value under different currents" )
plt.xlabel("Currents [A]")
plt.ylabel("Field [T]")
plt.legend(loc = 4)

plt.show()
