import sys
sys.path.append('/home/adam/Documents/PSRPOPPY/PsrPopChime/lib/python')
import populate
import dosurvey
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
def dosurvey_wrapper(val,save_folder='pmsurv_sp/'):
    pop = val['pop']
    surveyList = val['surveyList']
    beta_sp = val['beta_sp']
    beta_sp_std = val['beta_sp_std']
    br_mu = val['br_mu']
    br_sigma = val['br_sigma']
    rratssearch = val['rratssearch']
    try:
        dos = val['dos']
    except:
        dos = 0
    det= dosurvey.run(pop,surveyList=surveyList,beta_sp=beta_sp,beta_sp_std=beta_sp_std,br_mu=br_mu,br_sigma=br_sigma,rratssearch=rratssearch,nostdout=True,dos=dos)
    save_str = save_folder+str(br_mu)+'_'+str(br_sigma)+'_'+str(beta_sp)+'_'+str(beta_sp_std)
    np.save(save_str,det)
    return_obj = det[0][3].ndet
    del det
    return return_obj

def sample_point(val):
    #unwrap
    pop = np.load('PMSURV_POP',allow_pickle=1)
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
        save_folder='pmsurv_sp/'
    try:
        dos = val['dos']
    except:
        dos = 0
    my_vals= {'pop':pop,'surveyList':surv,'beta_sp':beta_sp,'beta_sp_std':beta_sp_std,
              'br_mu':br_mu,'br_sigma':br_sigma,'rratssearch':True,'dos':dos}
    #do simulation
    ndet=[]
    for i in range(average):
        ndet.append(dosurvey_wrapper(my_vals,save_folder=save_folder))
    ndet_avg = np.mean(ndet)
    ndet_error = ndet_avg-obs
    del pop
    print(str(val)+': '+str(ndet_error))
    return ndet_error