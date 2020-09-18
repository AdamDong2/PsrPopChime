import pylab as plt
import numpy as np
import non_linear_fitting as nlf


def plot_these(x,y,fit=False,func=None,p0=None,label1=None,label2=None,show=True,print_res=False):
    #this is to get same bin width for the two histograms
    bins=np.histogram(np.hstack((x,y)), bins=int(np.sqrt(len(x))))[1]
    ydata1,bins1=np.histogram(x,bins=bins)
    area1=sum(np.diff(bins1)*ydata1)
    ydata2,bins2=np.histogram(y,bins=bins)
    area2=sum(np.diff(bins2)*ydata2)
    xdata1=(bins1[:-1] + bins1[1:]) / 2
    xdata2=(bins2[:-1] + bins2[1:]) / 2

    #plot the two histograms first
    plt.hist(y,bins=bins,histtype='stepfilled',label=label2,alpha=.5,normed=0)
    plt.hist(x,bins=bins,histtype='step',label=label1,color='k',normed=0)
    plt.ylabel("# Pulses")
    #plt.show()
    #If it fits, it fits! 
    if fit is True:
        try:
            #So this fits histograms with denisty=1
            #later we multiply with area during plot to bring things at same scale
            par1, err1=nlf.fit_this(x, x,func,p0=p0,histdata=True,density=1)
            plot_func=getattr(nlf, func)
            par3, err3=nlf.fit_this(y,y,func,p0=p0,histdata=True,density=1)
            #plt.figure()
            #plot the fits
            plt.plot(xdata1,area1*plot_func(xdata1,*par1),'b',linewidth=2,label=label1)
            plt.plot(xdata1,area2*plot_func(xdata1,*par3),'r',linewidth=2,label=label2)

            #print injeted mu, recovered mu, err mu and sigma
            if print_res is True:
                print(p0[1],par3[1],err3[1],p0[2],par3[2],err3[2])
        except RuntimeError:
            pass
    plt.xlabel("Luminosity")
    plt.grid()
    if label2 is not None and label1 is not None:
        plt.legend()
    if show is True:
        plt.show()
