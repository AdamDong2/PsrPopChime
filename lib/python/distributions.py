
#using tranverse sampling methods
#using tranverse sampling methods
#using tranverse sampling methods#!/usr/bin/python

import sys
import math
import random
import numpy as np
def drawhalflnorm(mean,sigma,size=1):
    dist = np.random.normal(mean, sigma,(size))
    #redraw these 
    ind = np.argwhere(dist<0)
    for my_indices in ind:
        val=-1
        while val<0:
            val = np.random.normal(mean,sigma)
        dist[my_indices]=val
    return 10**dist

def drawlnorm(mean, sigma,size=1):
    """Draw a random number from a log-normal distribution"""

    return 10.0**np.random.normal(mean, sigma,(size))

def powerlaw(alpha,xmin,xmax,size=1):
    cdf = np.random.rand(size)
    logx=np.log10(cdf*(xmax**(alpha+1)-xmin**(alpha+1))+xmin**(alpha+1))/(alpha+1)
    x=10**logx
    #x = xmin*(10**(np.log10(cdf)/(alpha+1)))
    return x

def powerlawnp(alpha,xmax,xmin,size=1):
    '''draw a random number from power law distribution'''
    #we need to modify the alpha parameter because the default power is alpha-1
    power = -1*alpha + 1
    return_val = (xmax-xmin)*(-np.random.power(power,(size))+1)+xmin
    return return_val

def power_law_dual(xmin,xmax,xtransition,nbreak,power1,power2):
    logmin = math.log10(xmin)
    logmax= math.log10(xmax)
    logtransition = math.log10(xtransition)
    c1 =math.log10(nbreak)-power1*math.log10(xtransition) 
    c2 = math.log10(nbreak)-power2*math.log10(xtransition)
    nmax = 10.0**(power2*logmin + c2)
    #using inverse sampling methods
    samplen=random.random()*nmax
    if samplen<=nbreak:
        #use the lower power law
        x = 10**((math.log10(samplen)-c1)/power1)
    else:
        #use the upper power law
        x = 10**((math.log10(samplen)-c2)/power2)
    return x



def power_law_orig(minval, maxval, power):
    """Draw a value randomly from the specified power law"""

    logmin = math.log10(minval)
    logmax = math.log10(maxval)

    c = -1.0 * logmax * power
    nmax = 10.0**(power*logmin + c)

    # slightly worried about inf loops here...
    while True:
        log = random.uniform(logmin, logmax)
        n = 10.0**(power*log + c)

        if nmax*random.random() <= n:
            break

    return 10.0**log

'''
def power_law_dual(xmin,xmax,power):
    logmin = math.log10(xmin)
    logmax= math.log10(xmax)
    c =power*math.log10(xmin) 
    nmax = 10.0**(power*logmin)
    #using inverse sampling methods
    samplen=random.random()*nmax
    x = 10**((math.log10(samplen)-c)/power)
    return x
'''
def draw1d(dist):
    """Draw a bin number form a home-made distribution
        (dist is a list of numbers per bin)
    """
    # sum of distribution
    total = float(sum(dist))
    # cumulative distn
    cumulative = [sum(dist[:x+1])/total for x in range(len(dist))]

    rand_num = random.random()
    for i, c in enumerate(cumulative):
        if rand_num <= c:
            return i


def draw_double_sided_exp(scale, origin=0.0):
    """Exponential distribution around origin, with scale height scale."""
    if scale == 0.0:
        return origin

    rn = random.random()
    sign = random.choice([-1.0, 1.0])

    return origin + sign * scale * math.log(rn)

def uniform(low,high):
	"""Draw a random number from a uniform distribution between low and high"""
	return 10 ** random.uniform(np.log10(low),np.log10(high))
