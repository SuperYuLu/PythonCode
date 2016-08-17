#beamTemp.py
import os
import numpy as np
import matplotlib.pyplot as plt
import re
from scipy.optimize import curve_fit
#nozzleTemp = 77 #108 #[k] -165 C
nozzleTemp = 100 #-173C
upperBound = 1200
lowerBound = 750

def save_plots(fig):
    if not os.path.exists(savePath):
        os.mkdir(savePath)
        print('***Path ' + savePath, 'created \n\n')

    fig.savefig(savePath + saveName  + '.png', dpi = 300)
    print('***Plots saved in :' + savePath + '\n')


def find_bounds_idx(filename):
    times = np.loadtxt(filename, skiprows = 22)[:,0]
    lb = np.argmin(abs(times*1e6 - lowerBound))
    ub = np.argmin(abs(times*1e6 - upperBound))
    return (lb, ub)

    
def calcuTemp(data): #2D array
    idxMax = data[:,1].argmax()
    tArrive = data[idxMax, 0]
    halfMax = data[idxMax, 1]/2
    lowerHalfIdx = abs(data[:idxMax,1] - halfMax).argmin()
    higherHalfIdx = idxMax + abs(data[idxMax :, 1] - halfMax).argmin()
    FWHM = data[higherHalfIdx, 0 ] - data[lowerHalfIdx,0]
    speedRatio = 2*np.sqrt(2*np.log(2)) * tArrive / FWHM
    temp = nozzleTemp / ( 1 + 0.4 * speedRatio **2)
    return temp,idxMax,halfMax

def gaus(x, a, x0, sigma):
    return a * np.exp(-(x-x0)**2 / (2 * sigma **2))



def run():
    if os.path.exists(path+dataFile):
        lb, ub = find_bounds_idx(path + dataFile)
        print("[loading " + dataFile + "]")
        data = np.loadtxt(path + dataFile, skiprows = 22)[lb:ub, :]
        T,idxMax,halfMax = calcuTemp(data)
    
        n = len(data[:,0])
        mean = sum(data[:,0]*data[:,1])/n
        sigma = np.sqrt(sum(data[:,1] * (data[:,0] - mean)**2)/n)
        popt, pcov = curve_fit(gaus, data[:,0], data[:,1], p0 = [1, mean, sigma])
        FWHM_gaus = abs(popt[2]) * 2.355 # using gaussian fit
        tArrive_gaus = popt[1] #arriving time [s]
        speedRatio_gaus = 2 * np.sqrt(2*np.log(2)) * tArrive_gaus / FWHM_gaus
        T_gauss = nozzleTemp / ( 1 + 0.4 * speedRatio_gaus **2)

        f = plt.figure(1)
        ax = f.add_subplot(111)
        ax.plot(data[:,0]*1e6, data[:,1], 'bo')
        ax.plot(data[:,0]*1e6, gaus(data[:,0], *popt), 'g-')
        ax.plot([data[idxMax,0]*1e6,data[idxMax,0]*1e6], [halfMax*2.2,0],'r-')
        ax.plot([data[0,0]*1e6, max(data[:,0])*1e6], [halfMax,halfMax], 'r-')
        ax.set_title('RGA signal of He beam')
        ax.set_xlabel('Time [us]')
        ax.set_ylabel('RGA signal (arb unit)')
        ax.set_ylim(ymin = -0.5)
        #ax.text(0.7 * max(data[:,0]) * 1e6, 0.8 * max(data[:, 1]), \
        ax.text( 750,-0.5, \
                "File:" + dataFile + '\n' + \
                "Nozzle temp:" + str(nozzleTemp) + '[k]\n' + \
                "Beam temperature(w/o fit): " + str(T*1e3) + '[mk]\n' + \
                "Beam temperature(w/ fit): " + str(T_gauss *1e3) + '[mk]\n')
        if save:
            save_plots(f)
        plt.show()
    else:
        print("File not found! (flash drive mounted ?)")
        
run()


