from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import random

def gen_nos(hist,bins):
    cdf = np.cumsum(hist)
    cdf = cdf / cdf[-1]
    value_bins = np.searchsorted(cdf, random.random(), side='left')
    random_from_cdf = bins[value_bins]
    return(random_from_cdf)
