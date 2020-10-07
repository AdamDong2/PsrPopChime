import numpy as np

def calc_cf(in_dist,compare_dist,bins):
# Pass the distributions with  number of bins
    real,edges=np.histogram(compare_dist,bins=bins,density=1)
    model,edges=np.histogram(in_dist,bins=bins,range=[np.amin(compare_dist),np.amax(compare_dist)],density=1)
    ret_val=np.zeros(len(real))
    for i in xrange(len(model)):
        if model[i]==0:
            ret_val[i]=real[i]
        else:
            ret_val[i]= (real[i]-model[i])/model[i]
    return ret_val

def apply_cf(cf, dist):
#pass the hist values only
    ret_pop=np.zeros(len(dist))
    for i in xrange(len(dist)):
        if dist[i]==0:
            ret_pop[i]=cf[i]
        else:
            ret_pop[i]=dist[i] + dist[i]*cf[i]
    return (ret_pop)
