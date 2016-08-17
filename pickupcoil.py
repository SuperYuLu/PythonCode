import numpy as np
import os.path as pth
import scipy as scp
import matplotlib.pyplot as plt
import time

folder = '/home/superlu/Documents/Python/PickUpCoil/pickupcoil/' 

# =======================================================================================
# Functions to be used in other main funcitons 
def load_file(filename):
    return np.loadtxt(folder+filename)

def ave_single_holder(holder_num):
    peaks = []
    data = np.zeros([3,10,2])
    for i in range(1,4):
        filename = holder_num + '_peak_' + str(i) + '.txt'
        data[i-1,:,:] = load_file(filename)
    peaks = np.average(data,0)
    peak_std = np.std(data,0)
    return (peaks, peak_std)

def ave_single_holder_raw(holder_num):
    data = np.zeros([3,1200,3])
    data_averaged = np.zeros([1200, 3])
    for i in range(1,4):
        filename = holder_num + '_' + str(i) + '.txt'
        data[i-1,:,:] = np.genfromtxt(folder+filename, skip_header = 5)[:1200,2:5]
    data_averaged = np.average(data,0)
    return (data_averaged)
    
def find_peaks_single_holder(holder_num):
    data = ave_single_holder_raw(holder_num)
    peak_idx = np.linspace(100, 1000, 10) #estimate the arriving time idx
    search_range = 40
    max_peaks = np.zeros([3,10, 2]) # 3 pickup coils, 10 peaks, 2 for idx and value
    min_peaks = np.zeros([3,10, 2])
    for j in range(0,3):
        for k in range(0,10):
            maxpeak = minpeak = 0
            idx = round(peak_idx[k])
            for i in range(0,search_range):
                pos = int(idx - int(search_range/2) + i)
                if data[pos, j] > maxpeak:
                    maxpeak = data[pos,j]
                    maxidx = pos
                if data[pos, j] < minpeak:
                    minpeak = data[pos,j]
                    minidx = pos 
            max_peaks[j, k, 0] = maxidx
            max_peaks[j, k, 1] = maxpeak
            min_peaks[j, k, 0] = minidx
            min_peaks[j, k, 1] = minpeak
    return (max_peaks, min_peaks)
#====================================================================================================
# Main part for ploting 

def plot_peaks_holder(holder_num):
    peak_num = np.linspace(1,10,10)
    peaks,peak_std = ave_single_holder(holder_num)
    plt.errorbar(peak_num, peaks[:,0],yerr = peak_std[:,0],fmt = 'b*',label = 'high')
    plt.errorbar(peak_num, peaks[:,1],yerr = peak_std[:,1],fmt = 'r*',label = 'low')
    plt.title('Pick up coil signal of coil holder #' + holder_num)
    plt.xlim([0,11])
    plt.show()

def plot_peaks_dischargebd():
    peak_num_dischargebd = np.linspace(1,30,30)
    avaliable = True
    for i in range(1,17):
        for j in range(1,4):
            filename = folder + str((i-1)*3+j) + '_peak_' + str(j) + '.txt'
            if pth.isfile(filename):
                avaliable = True 
            else:
                avaliable = False
                print('Discharge board No.' + str(i) + ' data not complete')
                break
        if avaliable == True:
            for j in range(1,4):
                filename = folder + str((i-1)*3+j) + '_peak_' + str(j) + '.txt'
                if j == 1:
                    peaks, peak_std = ave_single_holder(str((i-1)*3+j))
                else:
                    pk, std = ave_single_holder(str((i-1)*3+j))
                    peaks = np.concatenate((peaks,pk),axis = 0)
                    peak_std = np.concatenate((peak_std,std),axis = 0)
                    #peaks = max(abs(peaks[:,0]),abs(peaks[:,1]))
            plt.figure(1)
            plt.errorbar(peak_num_dischargebd, peaks [:,0], yerr = peak_std[:,0], fmt = '-', label = 'Discharge BD No.' + str(i) + 'high', markersize = 8)
            plt.figure(2)
            plt.errorbar(peak_num_dischargebd, peaks[:,1],yerr = peak_std[:,1],fmt = '-',label = 'Discharge BD No.' + str(i) + 'low',markersize = 8)            
        else:
            continue
    plt.figure(1)
    plt.xlim([0,31])
    plt.title('Pickup coil signal max for all discharge boards')
    plt.legend(prop = {'size' : 6})
    plt.figure(2)
    plt.xlim([0,31])
    plt.title('Pickup coil signal min for all discharge boards')
    plt.legend(prop = {'size' : 6})
    
    plt.show()

def plot_peaks_all():
    peak_num = np.linspace(1,10,10)
    for i in range(1,49):
        filename = folder + str(i) + '_peak_' + str(1) + '.txt'
        if pth.isfile(filename):
            peaks,peak_std = ave_single_holder(str(i))
            plt.errorbar(peak_num, peaks[:,0],yerr = peak_std[:,0],fmt = '-',label = 'Holder #' + str(i) + 'high',markersize = 8)
            plt.errorbar(peak_num, peaks[:,1],yerr = peak_std[:,1],fmt = '-',label = 'Holder #' + str(i) + 'low',markersize = 8)
        else:
            print("There is no " + filename + " exist\n")
    plt.title('Pickup coil signal for all coil holders')
    plt.xlim([0,11])
    plt.show()
            
            
def plot_raw_all():
    time = np.linspace(0, (1200-1)*10, 1200) 
    for i in range(1,49):
        signal = ave_single_holder_raw(str(i))
        for j in range(0,3):
            plt.figure(j)
            plt.plot(time, signal[:,j], '-', label ='holder No.' + str(i)) #signal from 1st pickup coil 
            plt.legend(prop = {'size' : 6.8}, loc = 'center right')
            #plt.pause(5)
    for j in range(0,3):
        plt.figure(j)
        plt.title( "No." + str(j) + 'pickup coil signal for coil holder')
    plt.show()


def plot_raw_dischargebd():
    time = np.linspace(0, (3600-1)*10, 3600) 
    all_peaks_max = np.zeros([3,16,30])
    all_peaks_min = np.zeros([3,16,30])
    peak_max_ave_std = np.zeros([3,30,2]) # [pickup coil No., :, 0->ave of max for each of 30 coils, 1->coil max std]
    peak_min_ave_std = np.zeros([3,30,2])

    for i in range(1,17): # for discharge boards
        peak_max_idx = np.zeros(30, dtype = np.int) # 30: pickup coil number on certain dischargeBD
        peak_min_idx = np.zeros(30, dtype = np.int)
        for j in range(1,4): # coil holders on certain discharge boards
            if j == 1:
                signal = ave_single_holder_raw(str((i-1)*3+j))         
                maxpeaks, minpeaks = find_peaks_single_holder(str((i-1)*3+j))
            else:
                sig = ave_single_holder_raw(str((i-1)*3+j))
                maxp,minp = find_peaks_single_holder(str((i-1)*3+j))
                maxp[:,:,0] = maxp[:,:,0] + 1200 * (j-1) #[pickup coil No., :, 0->idx, 1->value] 
                minp[:,:,0] = minp[:,:,0] + 1200 * (j-1)
                maxpeaks = np.concatenate((maxpeaks, maxp), axis = 1 )
                minpeaks = np.concatenate((minpeaks, minp), axis = 1 )
                signal = np.concatenate((signal,sig),axis = 0)
        peak_max_ave_std[:,:,0] += maxpeaks[:, :, 1] 
        peak_min_ave_std[:,:,0] += minpeaks[:, :, 1] 
        all_peaks_max[:,i-1,:] = maxpeaks[:,:,1]
        all_peaks_min[:,i-1,:] = minpeaks[:,:,1]
        for k in range(0,30):
            peak_max_idx[k] = int(maxpeaks[0, k, 0])
            peak_min_idx[k] = int(minpeaks[0, k, 0])
        for s in range(0, 3):#coil holder number 
            plt.figure(s+1)
            plt.plot(time, signal[:,s], '-', label = 'Discharge BD No. ' + str(i) , markersize = 8)
            #plt.plot(time[peak_max_idx], maxpeaks[s,:,1],'ro')
            #plt.plot(time[peak_min_idx], minpeaks[s,:,1],'bo')
    peak_max_ave_std[:,:,0] = np.average(all_peaks_max[:,:,:], 1)
    peak_max_ave_std[:,:,1] = np.std(all_peaks_max[:,:,:],1)
    peak_min_ave_std[:,:,0] = np.average(all_peaks_min[:,:,:], 1)
    peak_min_ave_std[:,:,1] = np.std(all_peaks_min[:,:,:],1)
    for t in range(0,3):
        plt.figure(t+1)
        plt.errorbar(time[peak_max_idx], peak_max_ave_std[t,:,0], yerr = peak_max_ave_std[t,:,1],fmt = 'ro', label = 'Average and Std, Max')
        plt.errorbar(time[peak_min_idx], peak_min_ave_std[t,:,0], yerr = peak_min_ave_std[t,:,1],fmt = 'bo', label = 'Average and Std, Min')
        plt.title('No.' + str(t) +' Pickup coil raw signal for all discharge boards')
        plt.legend(prop = {'size' : 8}, loc = 'center right')
    plt.show()

def plot_raw_single(holdernum):
    time = np.linspace(0, (1200-1)*10, 1200) 
    signal = ave_single_holder_raw(str(holdernum))
    maxpeaks,minpeaks = find_peaks_single_holder(str(holdernum))
    max_peak_idx = np.zeros(10, dtype = np.int)
    min_peak_idx = np.zeros(10, dtype = np.int)

    for j in range(0,3):
        for i in range(0,10):
            max_peak_idx[i] = int(maxpeaks[j,i,0])
            min_peak_idx[i] = int(minpeaks[j,i,0])

        plt.figure(j)
        plt.plot(time, signal[:,j], '-', label ='holder No.' + str(holdernum)) #signal from 1st pickup coil 
        plt.plot(time[max_peak_idx], maxpeaks[j,:,1], 'ro')
        plt.plot(time[min_peak_idx], minpeaks[j,:,1], 'go')
        plt.legend(prop = {'size' : 6.8}, loc = 'center right')
    for j in range(0,3):
        plt.figure(j)
        plt.title( "No." + str(j) + 'pickup coil signal for coil holder')
    plt.show()
    


