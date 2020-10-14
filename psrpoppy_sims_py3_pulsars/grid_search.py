from sklearn.model_selection import GridSearchCV 
from get_distribution import sample_point
import numpy as np
from multiprocessing import Pool
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


def grid_search():
    #define parameter space
    alpha_arr = np.linspace(-2.05,-20,40)
    br_mu = np.linspace(1,5,40)
    br_sigma = np.linspace(0.1,12,40)
    #easiest to just combine the arrays into one large dict
    param_dict=[]
    for i in range(len(alpha_arr)):
        for j in range(len(br_mu)):
            for k in range(len(br_sigma)):
                params = {'alpha':alpha_arr[i],'br_mu':br_mu[j],'br_sigma':br_sigma[k],'obs':125}
                param_dict.append(params)
    #for loop over everything
        
    with Pool(40) as p:
        ndets_error=np.array(p.map(sample_point,param_dict))
    np.save('errors',(ndets_error,alpha_arr,br_mu,br_sigma))
    
    ''' 
    ndets_error=[]
    for params in param_dict:
        ndets_error.append(sample_point(params))
    '''    
def plotting():
    ndets_error,alpha_arr,br_mu,br_sigma = np.load('grid_searchnpys/errors_5.npy',allow_pickle=1)
    print(ndets_error[0:500])
    ndets_error=ndets_error.reshape((len(alpha_arr),len(br_mu),len(br_sigma)))
    print(ndets_error[:,1,:])
    print(ndets_error.shape)
    ndets_min = np.zeros((len(alpha_arr),len(br_mu)))
    br_sig_min = np.zeros((len(alpha_arr),len(br_mu)))
    #reorganise everything
    for i in range(len(alpha_arr)):
        for j in range(len(br_mu)):
            ndets_min[i,j] = np.min(ndets_error[i,j,:])
            br_sig_min[i,j] = br_sigma[np.argmin(ndets_error[i,j,:])]

    X,Y = np.meshgrid(br_mu,alpha_arr)
    print(X)
    print(Y)
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X,Y,ndets_min,antialiased=False)
    ax.set_xlabel('br')
    ax.set_ylabel('alpha')
    ax.set_zlabel('delta ndets')

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(X,Y,br_sig_min,antialiased=False)
    ax.set_xlabel('br')
    ax.set_ylabel('alpha')
    ax.set_zlabel('br_sig min')
    plt.show()

#grid_search()
plotting()
