from sklearn.model_selection import GridSearchCV 
from get_distribution import sample_point
import numpy as np
from multiprocessing import Pool
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
from datetime import datetime
def grid_search(fn,inputs,dos):
    mp=1
    #define parameter space
    #this one uses a log normal distribution for the single burst luminosities, this makes things easier to handle
    #take it as a multiple of the mean luminosity
    my_parameters = np.load(inputs,allow_pickle=1).tolist()
    my_parameters=my_parameters["0"]
    br_mu=[2.7]
    br_sigma=[0.34]
    #easiest to just combine the arrays into one large dict
    param_dict=[]
    now = datetime.now()
    dt_str = now.strftime("%Y%m%d%H%M%S")+'_DOS_'+str(dos)+'_CHIME/'
    os.mkdir(dt_str)
    for my_inputs in my_parameters:
        for j in range(len(br_mu)):
            for k in range(len(br_sigma)):
                params = {'beta_sp':my_inputs[0],'beta_sp_std':my_inputs[1],'br_mu':br_mu[j],'br_sigma':br_sigma[k],'obs':0,'avg':1,'surv':['CHIME'],'save_folder':dt_str,'dos':dos}
                param_dict.append(params)
    #for loop over everything
    if mp: 
        with Pool(24) as p:
            ndets_error=np.array(p.map(sample_point,param_dict))
        np.save(fn,(ndets_error,param_dict))
    else:
        ndets_error=[]
        for params in param_dict:
            ndets_error.append(sample_point(params))

import sys
for i in np.array(range(90))+1:
    grid_search(sys.argv[1]+'_dos_'+str(i),sys.argv[2],i)
#plotting(sys.argv[1]+'.npy')
