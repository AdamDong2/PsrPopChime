import sys
sys.path.append('/home/adam/Documents/PSRPOPPY/PsrPopChime/lib/python')
import populate
import dosurvey
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
import theano.tensor as tt
from theano.compile.ops import as_op
from multiprocessing import Pool
def dosurvey_wrapper(val,save_folder='pmsurv_sp/'):
    pop = val['pop']
    surveyList = val['surveyList']
    beta_sp = val['beta_sp']
    beta_sp_std = val['beta_sp_std']
    br_mu = val['br_mu']
    br_sigma = val['br_sigma']
    rratssearch = val['rratssearch']
    det= dosurvey.run(pop,surveyList=surveyList,beta_sp=beta_sp,beta_sp_std=beta_sp_std,br_mu=br_mu,br_sigma=br_sigma,rratssearch=rratssearch,nostdout=True)
    save_str = save_folder+str(br_mu)+'_'+str(br_sigma)+'_'+str(beta_sp)+'_'+str(beta_sp_std)
    np.save(save_str,det)
    return_obj = det[0][3].ndet
    del det
    return return_obj
'''
global dist
dist = 100
pop = np.load('test',allow_pickle=1)
global pop_arr
pop_arr = np.array([])
for i in range(dist):
    pop_arr=np.append(pop_arr,np.copy(pop))
'''
def sample_point(val):
    #unwrap
    pop = np.load('112_pop',allow_pickle=1)
    #pop = np.load('224000_pulsars',allow_pickle=1)
    surv=val['surv']
    average=val['avg']
    beta_sp = val['beta_sp']
    beta_sp_std = val['beta_sp_std']
    br_mu= val['br_mu']
    br_sigma = val['br_sigma']
    obs= val['obs']
    try:
        save_folder = val['save_folder']
    except:
        save_folder='pmsurv_sp'
    my_vals= {'pop':pop,'surveyList':surv,'beta_sp':beta_sp,'beta_sp_std':beta_sp_std,'br_mu':br_mu,'br_sigma':br_sigma,'rratssearch':True}
    #do simulation
    ndet=[]
    for i in range(average):
        ndet.append(dosurvey_wrapper(my_vals,save_folder=save_folder))
    ndet_avg = np.mean(ndet)
    ndet_error = ndet_avg-obs
    del pop
    print(str(val)+': '+str(ndet_error))
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
    np.save(fn,{'alpha':alpha,'br_mu':br_mu,'br_sigma':br_sigma,'val':val,'ndet':ndet,'mu':mu,'scale':scale})
    return np.array(norm.logpdf(val,loc=mu,scale=scale))
#dosurvey.write(surveyPopulations)
