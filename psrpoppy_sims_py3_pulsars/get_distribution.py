import sys
sys.path.append('/home/adam/anaconda3/envs/CHIME/lib/python3.8/psrpoppy')
from psrpoppy import populate,dosurvey
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import norm
def get_distibution(alpha,br_mu,br_sigma,val):
    pop = np.load('regular_pulsar',allow_pickle=1)
    ndet = []
    for i in range(100):
        det = dosurvey.run(pop,alpha=alpha,br_mu=br_mu,br_sigma=br_sigma, surveyList=['PMSURV'])
        ndet.append(det[0][3].ndet)
    mu,scale=norm.fit(ndet)
    return norm.logpdf(mu,scale=scale)  
#dosurvey.write(surveyPopulations)
