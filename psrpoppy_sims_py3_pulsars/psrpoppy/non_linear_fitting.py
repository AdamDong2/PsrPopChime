#!/usr/bin/env python3

import numpy as np
from scipy.optimize import curve_fit

def gaussian(x,amp,mu,sig):
    return(amp*np.exp(-0.5*((x-mu)/sig)**2))

def gaussian_normed(x,mu,sig):
    amp=1/(sig*np.sqrt(2*np.pi))
    return(amp*np.exp(-0.5*((x-mu)/sig)**2))

def lnorm(x,amp,mu,sig):
    return(10**(amp*np.exp(-0.5*((x-mu)/sig)**2)))

def lnorm_b(x,amp,mu,sig):
    b=10
    m=mu*np.log(b)
    V=(sig*np.log(b))**2
    return(amp*np.exp(-((np.log(x)-m)**2)/(2*V)))

def lnorm_e(x,amp,mu,sig):
    return(amp*np.exp(-0.5*((np.log(x)-mu)/sig)**2)/x)

def fit_this(xdata,ydata,func,p0=None,histdata=False,bins=None,density=1):
    if density==0:
        density=0
    if histdata is True:
        if bins is None:
            ydata,bins=np.histogram(ydata,bins=int(np.sqrt(len(ydata))),density=density)
        else:
            ydata,bins=np.histogram(ydata,bins=bins,density=density)
        xdata=(bins[:-1] + bins[1:]) / 2
    if p0 is None:
        p0 = [1.0, 0.0, 1.0]
    if func=="gaussian":
        coeff, var_matrix = curve_fit(gaussian,xdata,ydata, p0=p0)
    elif func=="lnorm":
        coeff, var_matrix = curve_fit(lnorm,xdata,ydata, p0=p0)
    elif func=="lnorm_e":
        coeff, var_matrix = curve_fit(lnorm_e,xdata,ydata, p0=p0)
    elif func=="lnorm_b":
        coeff, var_matrix = curve_fit(lnorm_b,xdata,ydata, p0=p0)
    return(coeff,np.sqrt(np.diag(var_matrix)))
