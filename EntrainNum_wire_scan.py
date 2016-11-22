#EntrainNum_wire_scan.py
#Last updated: 2016/11/21
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import  scipy.integrate as integrate
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
fit = False
specialNote = 'None' #Put note on the plotted graph; shoud be overwrite
#Add \n when lengh exceed 22 characters 

# [20161117]
#_____________________________________________________________________________________
# [250v, 100us pusle len]
path = '/mnt/ExpData/20161117_hafnium/pulse-length-scan-250V-100us-wirescan/'
config = '20161117_config_100us-wirescan.txt'
specialNote = 'hafnium 250v 100us oven 600C'
lowerBound = 600
upperBound = 1200
fit = True
#result: 6.06E11 scan region too narrow, bean super wide

# [250v, 40us pulse len]
# path = '/mnt/ExpData/20161117_hafnium/pulse-length-scan-250V-40us-wirescan/'
# config = '20161117_config_40us-wirescan.txt'
# specialNote = 'hafnium 250v 40us oven 600C'
# lowerBound = 850
# upperBound = 950
# fit = True
# result: 4.83E09 entrainment data looks noisy

# [20161007]
#_____________________________________________________________________________________
#[600v para-scan]
# path = '/mnt/ExpData/20161007_600V-param-scan/origin-8s-100-50/'
# config = '20161007_config_wire_scan.txt'
# specialNote = 'not yet figured out'
# lowerBound = 500
# upperBound = 700
# fit = True
# Result: 1.35E11 entrainment data not quite smooth

#[600v correct pressure use me]
# path = '/mnt/ExpData/20161007_600V-param-scan/origin-8s-100-50-correct-pressure-use-me/'
# config = '20161007_config_wire_scan.txt'
# specialNote = 'not yet figured out'
# lowerBound = 500
# upperBound = 650
# fit = True
# result 9.79E10 entrainment data not smooth 

# [20161004]
#_____________________________________________________________________________________
# path = '/mnt/ExpData/20161004_600V/wire_scan_130us/'
# config = '20161004_config_wire_scan_130us.txt'
# specialNote = '130us pulse, 600v, what ribbon ?????'
# lowerBound = 400
# upperBound = 700
# fit = True
# result: messy data 1.18E11

# [20160920]voltage ???
#_____________________________________________________________________________________
#[330us - 5s] 
# path = '/mnt/ExpData/20160920_keyhole-ribbon/330us-5s/'
# config = '20160920_config_wirescan.txt'
# specialNote = 'Keyhole ribbon of Nichrome(?)'
# fit = True
# lowerBound = 700
# upperBound = 900
# resule: 1.42E11 

#[330us - 5s gain 5000000]
# path = '/mnt/ExpData/20160920_keyhole-ribbon/330us-5s_gain_5000000/'
# config = '20160920_config_wirescan.txt'
# specialNote = 'Keyhole ribbon of Nichrome(?)'
# fit = True
# lowerBound = 700
# upperBound = 900
# result: 1.07E11

#[400us - 7.5s gain 2000000]
# path = '/mnt/ExpData/20160920_keyhole-ribbon/400us-7.5s_gain_2000000/'
# config = '20160920_config_wirescan.txt'
# specialNote = 'Keyhole ribbon of Nichrome(?)'
# fit = True
# lowerBound = 500
# upperBound = 900
# result: original data shows negative value, upside down

# [20160907]
#_____________________________________________________________________________________
# path = '/mnt/ExpData/20160907_parameter_scan/'
# config = ????


# [20160817]
#_____________________________________________________________________________________
#[pure oven 600C]
#path = '/mnt/ExpData/20160817_5mill-800C-8s/pureOven/'
#config = '20160817_config_ref0-ribbon-oven-direct.txt'
#specialNote = 'Pure oven 600C'
#upperBound = 590
#result 3.41E10
#[ribbon delay opt] valve delay 40us, pulse 86us 8s 600C 290 psi
# path = '/mnt/ExpData/20160817_5mill-800C-8s/delayOptribbon/'
# config = '20160817_config_ref0-ribbon-oven-delayopt.txt'
# specialNote = 'vlave delay 40us, 5mil Nichrom 86us, 8s'
# upperBound = 650
#result: 3.50E11 At wire scan starting point, entrain num doesn't go to 0


# [20160815] Trying to finish last time what we didn't finish, 300V 80us 8s 5 mil
#_____________________________________________________________________________________
# nichorm ribbon, (The same ribbon as previous two day, man this ribbon is strong) 
# then trying to optimize it. this time we used 2000v CEM voltage instead of 1650 to
# make HE RGA signal nicer. 

#[ no opt, 300V 80us, 5mil, no delay, 600C]
#path = '/mnt/ExpData/20160815_5mill-8sec/noOpt/'
#config = '20160815_config_wirescan_oven_ribbon_start_.txt'
#specialNote= '5mil Nichrom, 80us, 8s, no delay,600Coven'
# result: 3.41E11


#[Delay optimized 40 us] 
#path = '/mnt/ExpData/20160815_5mill-8sec/delayopt/'
#config = '20160815_config_wirescan_oven_ribbon_delayopt.txt'
#specialNote = "5mil Nichrom, 80us, 8s, 40us delay"
#upperBound = 650
#lowerBound = 500
# result = 3.57E11


# [20160811] Same ribbon as yesterday, this time we keep oven temp at 600C, originally
#_____________________________________________________________________________________
# pulse len 75 us delay 35us, later we tried optimized with longer period 8s. Then even
# later we also tried increase the pulse len to 88us, but we can not finish a full wire
# scan due to the fuse broken 3 times. Then we gave up since its too late.

# -[only oven at 600C] we moved ribbon delay far behind nozzle, so there could only be
# pure oven entrainment signal
#path = '/mnt/ExpData/20160811_5mill-ribbon-600C/onlyOven/'
#config = '20160811_config_wirescan_ribbon_oven_deopt.txt'
#specialNote = 'pure oven at 600C'
# result: 1.18E11

# -[Oven and ribbon] pulse len 75 us, nozzle pulse delay 35 us, 300 psi
#path = '/mnt/ExpData/20160811_5mill-ribbon-600C/delayOpt/'
#config = '20160811_config_wirescan_ribbon_oven_opt.txt'
#specialNote = 'oven 600C, 5mil 1/4" ribbon, 75us, 5s'
#lowerBound = 500
#upperBound = 660
#result = 3.06E11

# -[oven and ribbon pulsen and period optimization] period to 8us, pulselen ref to labview
# figure
#path = '/mnt/ExpData/20160811_5mill-ribbon-600C/pulseLenPeriodOpt/'
#config = '20160811_config_wirescan_ribbon_oven_opt_long.txt'
#specialNote = 'oven 600C, 5mil Nichrom, 8s period'
#lowerBound = 500
#upperBound = 630
# result: 1.97E11, fuse broken at about middle of wire scan, then only remain oven entrain

# [oven and ribbon, pulse 86us, 8s period, half finished wirescan]
# path = '/mnt/ExpData/20160811_5mill-ribbon-600C/pulseLenPeriodOpt_unfinished/'
# config = '20160811_config_wirescan_ribbon_oven_opt_long3.txt'
# specialNote = '5 mil Nichrom, 8s period, 86us pulse len'
# lowerBound = 500
# upperBound = 630
# fit = True
# result: 5.19E11, wire scan not fully finished, shoud be more !!!!!!!!



#______________________________________________________________________________________
# [20160810] Today we tried optimize the pulse delay with nichrom ribbon 5 mil but 1/4"
#wide

# -[pure oven 550C]
#path = '/mnt/ExpData/20160810_5mill-ribbon/pureOven550C/'
#config = '20160810_config_wirescan_oven_ribbon_delay-deopt.txt'
#specialNote = "pure oven at 550C 300psi nozzle"
#result: 2.39E10

# [oven + ribbon, pulse len 75us, 5s, no optimization (no nozzle delay)]
#path = '/mnt/ExpData/20160810_5mill-ribbon/noOptimization/'
#config = '20160810_config_wirescan_oven_ribbon.txt'
#specialNote = '5mil Nichrom, 75us, 5s, no nozzle delay'
# result: 8.19E10

# [oven + ribbon, pulse len 75us, 5s, optimized, nozzle delay 45 us]
#path = '/mnt/ExpData/20160810_5mill-ribbon/optimizedDelay/'
#config = '20160810_config_wirescan_oven_ribbon_delay-opt.txt'
#specialNote = '5mil nichrom, 75us, 5s, nozzle delay 45us'
#lowerBound = 560
#upperBound = 650
# result: 1.25E11 ribbon has only 1/4" width, to keep same resistance
#______________________________________________________________________________________

#[20160728 Nichrome ribbon with graphite paste, 70+us, oven 550C] [best data right now]
#Did not take pure entrainment
#path = '/mnt/ExpData/20160728_ribbon-during-oven-heating/'
#config = '20160728_config_wirescan_ribbon_correct_range.txt'
#specialNote = 'Nichrom ribbon 70us/3s\n  with graphite paste' 
#result: 1.92E11 (best data of ribbon entrainment at this moment)

#[20160728 similar above, SRS overload at peak, just for test]
#path = '/mnt/ExpData/20160728_ribbon-during-oven-heating/overload_gain_scan_ribbon/'
#config = '20160728_config_wirescan_ribbon.txt'
#specialNote = 'SRS overload at peak'
#result: 1.78E11, does not catch the whole beam

#[20160718oven_550C]
#Only capillary oven entrainment, got circuit issue when doing ribbon entrainment
#path = '/mnt/ExpData/20160718_nichrome_2mil_550C/'
#config = '20160718_config_wirescan_549C.txt'
#specialNote = 'Pure capillary oven'
#Result: 1.11E10 (wire scan data noisy, has negative values)



#[20160712oven_550C]
#From today we changed the capillary oven, to similar one but with longer capillary 
#path = '/mnt/ExpData/20160712_nichrome_2mil_550C/'
#config = '20160712_config_scan_oven_549C.txt'
#specialNote = 'Pure capillary oven'
#Result: 1.11E10 (wire scan data noisy, has negative values)

#[20160623 oven 550C]
#pure capillay oven entrainment
#path = '/mnt/ExpData/20160623_nicr-ribbon/'
#config = '20160623_config_ref_3in_ribbon_off_start_wirescan.txt'
#specialNote = 'Pure capillary oven'
#Result: 1.03E10 

#[20160616_super-nice-data oven at different 550, 600C]

#--[oven_550C]
#path = '/mnt/ExpData/20160616_super-nice-data/oven_550C/'
#config = '20160616_config_ref_3in_ribbon_off_wirescan.txt'
#specialNote = 'Pure capillary oven'
#Result: 1.07E10 (wire scan data very noisy)

##--[oven_580C]
#path = '/mnt/ExpData/20160616_super-nice-data/oven_580C/'
#config = '20160616_config_ref_3in_ribbon_off_wirescan_oven_580.txt'
#specialNote = 'Pure capillary oven'
#Result: 1.71E10 (wire scan data noisy, has negative values)

##--[oven_600C]
#path = '/mnt/ExpData/20160616_super-nice-data/oven_600C/'
#config = '20160616_config_ref_3in_ribbon_off_oven_600.txt'
#specialNote = 'Pure capillary oven'
#Result: 3.56E10 (wire scan data noisy, has negative values)

##--[20160616 ribbion far from optimization]
#path = '/mnt/ExpData/20160616_super-nice-data/'
#config = '20160616_config_ref_3in_ribbon_on_40mus_delay_no.txt'
#specialNote = 'Nichrom ribbon 40us(?)'
#Result: 1.38E10 (only for half wire scan)
## -- end 

#[20160610_nicr_best-of direct capillary oven at 550 C]
#path = '/mnt/ExpData/20160610_nicr-best-of/'
#config = '20160610_config_ref_3in_no_ribbon_wirescan.txt'
#specialNote = 'Pure capillary oven'
#Result: 5.49E09

#[20160608_Direct capillary oven at 547C, P=254 psi]
#path = '/mnt/ExpData/20160608_wirescan/'
#config = '20160608_config_ref_3in_no_ribbon_wirescan.txt'
#specialNote = 'Pure capillary oven'

#Result: 6.94E09 wire scan not finished 


# [20160606_Direct capillary oven at 552C, P=247 psi]
#path = '/mnt/ExpData/20160606_oven-ribbon/'
#config = '20160606_config_oven_wirescan.txt'
#specialNote = 'Pure capillay oven'
# Result: 8.5E09

# [20160602_Nichrome Ribbon no optimization,oven at 545C, P=250psi]
#path = '/mnt/ExpData/20160602_ribbon_nichrome/'
#config = '20160602_config_ribbon_54us_6s.txt'
#specialNote = 'Nichrom ribbon 54us/6s'
# Result: 1.37E11

# [20160531 Laser Ablation without heating beam, best in laser ablation 2nd round ?] 
# path = '/mnt/ExpData/20160531_Autoscan2/'
# config = '20160531_config_ref_3in_laser_on_wirescan.txt'
# specialNote = 'Laser ablation no heating beam'
# lowerBound = 550
# upperBound = 700

# Result: 6.08E09 config gain possibly wrong, using another config give factor of 2

# [20160527 Laser Ablation autoscan]
# path = '/mnt/ExpData/20160527_autoscan/'
# config = '20160527_config_autoscan.txt'
# lowerBound = 550
# upperBound = 700
# Result: 2.24E10


# [20160526 Laser Ablation autoscan]
# path = '/mnt/ExpData/20160526_autoscan/'
# config = '20160526_config_autoscan.txt'
# lowerBound = 550
# upperBound = 700
# *Wirescan only went half way* Result: 8.37E09



# [20160426 laser ablation liquid pool wire scan]
#path = '/mnt/ExpData/20160426_liquid_pool_wire_scan/to_be_imported/'
#config = '20160426_config_wire_scan_3.78125in.txt' # This data set has multiple config files
#lowerBound = 550
#upperBound = 700
#specialNote = 'laser ablation liquid pool'
# *Wire scan data has many big jumps* not finish full wire scan Result: 3.03E10

# [20160311 laser ablation fresh lithium] what target ?
#path = '/mnt/ExpData/20160311_fresh_lithium/to_be_imported_to_python/'
#config = '20160311_config_3.7640in.txt'
#lowerBound = 550
#upperBound = 700
#specialNote = 'laser ablation'
# *sampling rate is kind of small, data is a little bit noisy. 
#Result: 6.26E09 (not right, need gaussain fit, too big steps)

# [20151222 laser ablation]
# has seperate config files, so gain may diff
#path = '/mnt/ExpData/20151222_Wire_Scan/'
#config = '20151222_config_position3.1655in.txt'
#lowerBound = 550
#upperBound = 700
#specialNote = 'laser ablation' 


#_____________________________________________________________________________________

loc2 = path + config

save = False
savePath1 = path + 'result/'
savePath2 = '/home/superlu/Documents/Python/Entrainment/entrainResult/'

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
        
def gaus(x, a, x0, sigma):
        return a * np.exp(-(x - x0)**2 / (2 * sigma**2))
    
def gauss_fit(entrainNum):
    idxMax = entrainNum[:,1].argmax()
    mean = entrainNum[idxMax,0]
    a = entrainNum[idxMax,1]
    halfMax = entrainNum[idxMax,1]/2
    lowerHalfIdx = abs(entrainNum[:idxMax, 1] - halfMax).argmin()
    higherHalfIdx = idxMax + abs(entrainNum[idxMax :, 1] - halfMax). argmin()
    HWHM = (entrainNum[higherHalfIdx,0] - entrainNum[lowerHalfIdx,0])/2
    # n = entrainNum.shape[0]
    # mean = sum(entrainNum[:,0] * entrainNum[:,1]) / n
    # sigma = sum(entrainNum[:,1] * (entrainNum[:,0] - mean)**2 ) / n
    # a = max(entrainNum[:,1])
    popt, pcov = curve_fit(gaus, entrainNum[:,0], entrainNum[:,1],p0 = [a, mean,HWHM])
    return popt

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
    if fit == True:
        popt = gauss_fit(entrainNum)
        ax2.plot(entrainNum[:,0], gaus(entrainNum[:,0],*popt),'r-',label = 'gaussian fit')
        #inteSum = sum(gaus(entrainNum[:,0], *popt))
        #inte = integrate.quad(lambda x:gaus(x, *popt), entrainNum[0,0], entrainNum[-1,0])[0]
        #print('Entrainment Number w/ fit: %.2E' %inteSum)
        #print('\n')
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
    plt.show()
    if save:
        save_plots([fig1, fig2])

    

run()

