#!/usr/bin/python
#Filename:Rydberg_YuLu

import numpy as np
import matplotlib.pyplot as plt
import os
import re

M=77/10
pixelx=16e-6/M
pixely=16e-6/M
pixelarea=pixelx*pixely
sigma0=2.905e-13
linestrength=1

os.chdir('/home/yulu/Documents/Py_Rydberg') #working directory

if os.path.exists('test_analysis'): #find datadirectory
    os.chdir('test_analysis')
    datapath=os.getcwd()
    filelist=os.listdir(datapath)
else:
    print"No directory 'test_analysis' found!"
    
datadoc=[]
for documents in filelist:
    f=True and re.findall('22.*',documents) or continue
    if os.path.exists(f[0]):
        datadoc.append(documents)
if not datadoc:
    print'No data documents find!'
    

#datadoc=re.findall('\d22_.*',filelist[:])

    
print'end'

