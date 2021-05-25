from sklearn.model_selection import GridSearchCV 
from get_distribution import sample_point
import numpy as np
from multiprocessing import Pool
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import os
from datetime import datetime
def grid_search(fn,inputs):
    mp=1
    #define parameter space
    #this one uses a log normal distribution for the single burst luminosities, this makes things easier to handle
    #take it as a multiple of the mean luminosity
    my_parameters = np.load(inputs,allow_pickle=1).tolist()
    my_parameters=my_parameters["100"]
    br_mu=[2.7]
    br_sigma=[0.34]
    #easiest to just combine the arrays into one large dict
    param_dict=[]
    now = datetime.now()
    dt_str = now.strftime("%Y%m%d%H%M%S")+'/'
    os.mkdir(dt_str)
    for my_inputs in my_parameters:
        for j in range(len(br_mu)):
            for k in range(len(br_sigma)):
                params = {'beta_sp':my_inputs[0],'beta_sp_std':my_inputs[1],'br_mu':br_mu[j],'br_sigma':br_sigma[k],'obs':270,'avg':1,'surv':['PMSURV_EDIT'],'save_folder':dt_str}
                param_dict.append(params)
    #for loop over everything
    if mp: 
        with Pool(40) as p:
            ndets_error=np.array(p.map(sample_point,param_dict))
        np.save(fn,(ndets_error,param_dict))
    else:
        ndets_error=[]
        for params in param_dict:
            ndets_error.append(sample_point(params))

def plotting(fn):
    ndets_error,alpha_arr,br_mu,br_sigma = np.load(fn,allow_pickle=1)
    print(ndets_error[0:500])
    ndets_error=ndets_error.reshape((len(alpha_arr),len(br_mu),len(br_sigma)))
    print(ndets_error[:,1,:])
    print(ndets_error.shape)
    ndets_min = np.zeros((len(alpha_arr),len(br_mu)))
    br_sig_min = np.zeros((len(alpha_arr),len(br_mu)))
    chime_pop_min=np.zeros((len(alpha_arr),len(br_mu)))
    #reorganise everything
    params_dict=[]
    for i in range(len(alpha_arr)):
        for j in range(len(br_mu)):
            ndets_min[i,j] = np.min(ndets_error[i,j,:])
            br_sig_min[i,j] = br_sigma[np.argmin(ndets_error[i,j,:])]
            params = {'alpha':alpha_arr[i],'br_mu':br_mu[j],'br_sigma':br_sig_min[i,j],'obs':0,'avg':1,'surv':['CHIME']}
            params_dict.append(params)
    '''
    with Pool(10) as p:
        chime_dets = np.array(p.map(sample_point,params_dict))
    chime_pop_min= chime_dets.reshape((len(alpha_arr),len(br_mu)))
    np.savez('chime_results_'+fn,ndets=ndets_min,chime=chime_pop_min) 
    '''
    X,Y = np.meshgrid(br_mu,alpha_arr)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X,Y,ndets_min,antialiased=False)
    ax.set_xlabel('P')
    ax.set_ylabel(r'$\beta$')
    ax.set_zlabel(r'$\Delta$ Detections')
    #ax.set_zlim([0,120])
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X,Y,br_sig_min,antialiased=False)
    ax.set_xlabel('P')
    ax.set_ylabel(r'$\beta$')
    ax.set_zlabel(r'P $\sigma$')
    '''
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X,Y,chime_pop_min,antialiased=False)
    ax.set_xlabel('IBR')
    ax.set_ylabel(r'$\alpha$')
    ax.set_zlabel('CHIME Detections')
    '''
    #plt.figure()
    #index = np.argmin(ndets_min)
    #plt.scatter(ndets_min[index],chime_dets[index])
    #plt.xlabel('pkmbs dets')
    #plt.ylabel('chime dets')

    plt.show()

    



import sys
grid_search(sys.argv[1],sys.argv[2])
#plotting(sys.argv[1]+'.npy')
