import sys
sys.path.append('/home/adam/anaconda3/envs/CHIME/lib/python3.8/psrpoppy')
from psrpoppy import populate,dosurvey
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
import theano.tensor as tt
from theano.compile.ops import as_op
from multiprocessing import Pool
def dosurvey_wrapper(val):
    pop = val['pop']
    surveyList = val['surveyList']
    alpha = val['alpha']
    br_mu = val['br_mu']
    br_sigma = val['br_sigma']
    rratssearch = val['rratssearch']
    det= dosurvey.run(pop,surveyList=['PMSURV'],alpha=alpha,br_mu=br_mu,br_sigma=br_sigma,rratssearch=True,nostdout=True)
    return_obj = det[0][2].ndet
    del det
    return return_obj

global dist
dist = 100
pop = np.load('regular_pulsar',allow_pickle=1)
global pop_arr
pop_arr = np.array([])
for i in range(dist):
    pop_arr=np.append(pop_arr,np.copy(pop))

def sample_point(val):
    #unwrap
    pop = np.load('regular_pulsar',allow_pickle=1)

    alpha = val['alpha']
    br_mu= val['br_mu']
    br_sigma = val['br_sigma']
    obs= val['obs']
    my_vals= {'pop':pop,'surveyList':['PMSURV'],'alpha':alpha,'br_mu':br_mu,'br_sigma':br_sigma,'rratssearch':True}
    #do simulation
    ndet_error=np.abs(dosurvey_wrapper(my_vals)-obs)
    del pop
    return ndet_error


@as_op(itypes=[tt.dscalar,tt.dscalar,tt.dscalar,tt.dscalar], otypes=[tt.dscalar])
def get_distribution(alpha,br_mu,br_sigma,val):

    mp_arr=np.empty(dist,dtype=dict)
    for i in range(dist):
        my_vals= {'pop':pop_arr[i],'surveyList':['PMSURV'],'alpha':alpha,'br_mu':br_mu,'br_sigma':br_sigma,'rratssearch':True}
        mp_arr[i]=my_vals
    #mp_arr = np.full((100),my_vals,dtype=dict)
    
    with Pool(25) as p:
        ndet = p.map(dosurvey_wrapper,mp_arr)    
    '''
    ndet=[]
    for i in range(dist):
        ndet.append(dosurvey_wrapper(mp_arr[0]))
        print(i)
    '''
    mu,scale=norm.fit(ndet)
    fn = str(alpha)+'_'+str(br_mu)+'_'+str(br_sigma)+'_'+str(val)
    print('savinddg')
    np.save(fn,{'alpha':alpha,'br_mu':br_mu,'br_sigma':br_sigma,'val':val,'ndet':ndet,'mu':mu,'scale':scale})
    print(mu)
    print(scale)
    return np.array(norm.logpdf(val,loc=mu,scale=scale))
#dosurvey.write(surveyPopulations)
