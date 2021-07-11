import numpy as np
import matplotlib.pyplot as plt
import sys
ndet_min = []
ndet_max = []
filelist = sys.argv[1:]
dos = []

for file in filelist:
    a = np.load(file,allow_pickle=1)
    ndet=a[0]
    ndet_min.append(min(ndet))
    ndet_max.append(max(ndet))
    min_ind = np.where(ndet_min==ndet)
    max_ind = np.where(ndet_max==ndet)
    dos.append(a[1][1]['dos'])

#sort the arrays
ind_arr = np.argsort(dos)
dos = np.array(dos)[ind_arr]
ndet_min = np.array(ndet_min)[ind_arr]
ndet_max = np.array(ndet_max)[ind_arr]
mean = [np.mean([ndet_min[i],ndet_max[i]]) for i in range(len(dos))]
from scipy.optimize import curve_fit
def asinh(x,a,b):
    return(a*np.arcsinh(x)+b)
def logfit(x,a,b):
    return(a*np.log(x)+b)

poptasinh, pcov = curve_fit(asinh, dos, mean)
poptlog , pcov = curve_fit(logfit, dos, mean)

observations = np.load('observations.npz',allow_pickle=1)
cks = observations['ks']
cc = observations['clusters']
 
plt.figure()
plt.xlabel('observation time (days)')
plt.ylabel('Number of galactic single source emitters')
plt.fill_between(dos,ndet_min,ndet_max,facecolor='grey',interpolate=True)
plt.plot(dos,ndet_min)
plt.plot(dos,ndet_max)
plt.plot(dos,mean)
plt.plot(dos,asinh(dos,*poptasinh))
plt.plot(dos,logfit(dos,*poptlog))
plt.legend(['min','max','mean','sinh fit','log fit'])
plt.show()

plt.figure()
plt.xlabel('observation time (days)')
plt.ylabel('Number of galactic single source emitters')
plt.fill_between(dos,ndet_min,ndet_max,facecolor='grey',interpolate=True)
plt.plot(dos,ndet_min)
plt.plot(dos,ndet_max)
plt.plot(dos,mean)
plt.plot(np.linspace(1,len(cc),len(cc)),np.add(cc,cks))
plt.legend(['min','max','mean','observations'])
plt.show()
