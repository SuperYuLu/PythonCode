#EntrainNum_wire_scan.py
#Last updated: 2016/08/01
import numpy as np
import matplotlib.pyplot as plt
import re
import os
#Global control

#[Bounds for oven/ribbon entrainment]
lowerBound = 500 # Lower bound for time window [us]
upperBound = 600 # higer bound for time windown [us]

# #[Bounds for laser ablation entrainment]
# lowerBound = 550
# upperBound = 700

detectProb = 0.3

specialNote = 'None' #Put note on the plotted graph; shoud be overwrite


#_____________________________________________________________________________________

loc2 = path + config

save = True
savePath1 = path + 'result/'
savePath2 = '/home/yulu/Documents/Python/Entrainment/entrainResult/'

volt = np.array([1.5, 2.5, 4.5, 6, 9, 11, 13])
temp = np.array([598, 871, 1135, 1314, 1505, 1607, 1733]) + 273
T = np.interp(12, volt, temp)-100 # don't understand righ now 

#Saha-Langmuir Law
I = 5.392 #[ev] -Ionization Potential of Li
Phi = 4.96 #[ev] -Work Function of Rhenium
k = 8.617e-5 #[ev/k] -Boltzmann const
e = 1.602e-19 # C -Charge of electron
Prob = 1/(1+2*np.exp((I-Phi)/(k*T))); #Saha-Langmuir Law, ionization prob.

def find_gain():
    gainf = 0 # Femto gain
    gains = 0 # SRS gain
    configFile = open(loc2, 'r')
    while (gains * gainf == 0):
        line = configFile.readline()
        if (line[0:10] == 'Femto Gain'):
            gainf = float(line[11:])
        elif (line[0:8] == 'SRS Gain'):
            gains = float(line[9:])
    configFile.close()
    return gainf * gains


def find_oven_temp():
    temp = 0
    configFile = open(loc2, 'r')
    while temp ==0:
        line = configFile.readline()
        if (line[7:15] == 'Oven Res'):
            temp = line[20:-1]
    if temp == 0:
        temp = '?'
    configFile.close()
    return temp


def list_position(path):
    pos = []
    for filename in os.listdir(path):
        if filename.find('WIRE'):
            p = re.findall('\d+[\.]\d+',filename)
            if (p and (not(p[0] in pos))):
                pos.append(p[0])
            else:
                continue
        else: continue
    pos.sort(key = float)
    print('Number of  wire scan positions: ', len(pos))
    return pos

def find_bounds_idx(filename):
    times = np.loadtxt(filename, skiprows = 22)[:,0]
    lb = np.argmin(abs(times*1e6 - lowerBound))
    ub = np.argmin(abs(times*1e6 - upperBound))
    return (lb, ub)

def save_plots(fig):
    if not os.path.exists(savePath1):
        os.mkdir(savePath1)
        print('***Path ' + savePath1, 'created \n\n')

    if not os.path.exists(savePath2):
        os.mkdir(savePath2)
        print('***Path ' + savePath2, 'created \n\n')
    date = re.findall('\d+', path)[0]
    i = 0
    for f in fig:
        i += 1
        f.savefig(savePath1 + date + 'plot' + str(i) + '.png',dpi = 300)
        print('***Plots saved in :' + savePath1 + '\n')
        f.savefig(savePath2 + date + 'plot' + str(i) + '.png', dpi = 300)
        print('***Plots saved in :' + savePath2 + '\n')

def run():
    pos = list_position(path)
    files = os.listdir(path)
    entrainNum = np.zeros([len(pos), 2])
    gain = find_gain()
    for i in range(0,len(pos)):
        if i == 0:
            for f in files:
                if f.find(pos[0])> 0:
                    lb, hb = find_bounds_idx(path+f)
                    break
        for f in files:
            if f.find(pos[i])>0:
                print('loading -->',  f)
                data = np.loadtxt(path+f, skiprows = 22)[lb:hb,:]
                fig1 = plt.figure(1)
                ax1 = fig1.add_subplot(111)
                ax1.plot(data[:,0]*1e6,data[:,1],'-', label = pos[i])
                entrainNum[i,0] = pos[i]
                entrainNum[i,1] = np.trapz(data[:,1],data[:,0])/(e*Prob*gain*detectProb)
                break
        
    totalNum = entrainNum[:,1].sum()
    
    print('Hot wire temp: ', T, ' C')
    print('Collection efficiency: ', detectProb)
    print('Ionization efficiency: ', Prob)
    print('Gain : ', gain)
    print('Oven Temp:' , find_oven_temp())
    #print('Oven Temp: ?')
    print('Entrainment Number: %.2E' %totalNum)

    
    ax1.set_title('Wire detector signal')
    ax1.set_xlabel('Time of flight [us]')
    ax1.set_ylabel('Signal')
    
    fig2 = plt.figure(2)
    ax2 = fig2.add_subplot(111)
    ax2.plot(entrainNum[:,0],entrainNum[:,1],'o')
    ax2.set_xlabel('Wire scan position [in]')
    ax2.set_ylabel('Entrained atom number')
    ax2.set_title('Entrainment with wire scan position')
    plt.xlim([3,5])
    ax2.text(0.9 * max(entrainNum[:,0]), 0.7 * max(entrainNum[:,1]), \
             'Date: ' + re.findall('\d+', path)[0] + '\n' + \
             'Oven temp: ' + str(find_oven_temp())[:5] + 'C\n' + \
             #'Oven temp: ? C' + \
             'Collection efficiency: ' + str(detectProb) + '\n' + \
             'Ionization efficiency: ' + str(Prob)[:5] + '\n' + \
             'DAQ gain: ' + str(gain) + '\n' + \
             'Note: ' + specialNote + '\n' + \
             'Entrainment Num: %.2E' %totalNum, \
             fontsize = 10)
    if save:
        save_plots([fig1, fig2])

    plt.show()

run()

