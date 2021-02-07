import pymc3 as pm
import numpy as np
from get_distribution import get_distribution
import theano
import theano.tensor as tt
observed = 257  
#load the population
with pm.Model() as model:
    alpha=-1*pm.Lognormal('alpha',mu=2.3,sd=1)-2    
    br_mu = pm.Normal('br_mu',mu=1,sd=0.1)
    br_sigma = pm.Normal('br_sigma',mu=4,sd=0.01)
    def logp(alpha,br_mu,br_sigma,val):
        return get_distribution(alpha,br_mu,br_sigma,val)
    likelyhood = pm.DensityDist('likelyhood', logp, observed={'alpha':alpha, 'br_mu':br_mu,'br_sigma':br_sigma,'val':1.285})
    step = pm.Metropolis()
    trace = pm.sample(500,step,chains=1)
    np.save('my_trace',trace)
    pm.save_trace(trace,'my_trace_pm_2')
    
