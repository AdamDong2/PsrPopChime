import matplotlib.pyplot as plt
import numpy as np
import sys
from psrpoppy import galacticops as go
import pickle
sys.path.append('/home/adam/anaconda3/envs/psrpoppy3/lib/python3.7/psrpoppy/')
l=np.linspace(0,360,1000)
b=np.linspace(-90,90,1000)
ras=[]
decs=[]
for i in range(len(l)):
    ra,dec = go.lb_to_radec(l[i],0)
    ras.append(ra)
    decs.append(dec)

filenames = sys.argv
with open(filenames[1],'rb') as surv:
    survey = pickle.load(surv)
with open(filenames[2],'rb') as my_pop:
    pop = pickle.load(my_pop)

def plot_surv_coord(survey,s=5,fig_num=1,plot_gal_plane=True,label=''):
    ra_deg = []
    dec_deg = []
    gl=[]
    gb=[]
    gains =[]
    tobs=[]
    br=[]
    spindex=[]
    lum_1400=[]
    period=[]
    dm=[]
    for pulsar in survey.population:
        dm.append(pulsar.dm)
        ra, dec = go.lb_to_radec(pulsar.gl, pulsar.gb)
        gl.append(pulsar.gl)
        gb.append(pulsar.gb)
        ra_deg.append(ra)
        dec_deg.append(dec)
        gains.append(pulsar.gain)
        tobs.append(pulsar.tobs)
        br.append(pulsar.br)
        spindex.append(pulsar.spindex)
        lum_1400.append(pulsar.lum_1400)
        period.append(np.log10(pulsar.period))
    plt.figure(fig_num)
    plt.scatter(ra_deg,dec_deg,marker='.',s=s,label=label)
    plt.scatter
    plt.xlabel('ra')
    plt.ylabel('dec')
    plt.legend()
    if plot_gal_plane:
        plt.scatter(ras,decs,c='black',marker='.',label='galactic plane')

    plt.figure(fig_num+1)
    plt.scatter(gl,gb,marker='.',s=s,label=label)
    plt.xlabel('gl')
    plt.ylabel('gb')
    plt.legend()

    plt.figure(fig_num+3)
    values,base=np.histogram(lum_1400,bins=1000)
    cumulative = np.cumsum(values[::-1])
    plt.plot(base[:-1],cumulative[::-1],label=label)
    plt.xlabel('lum 1400 (mJy kpc^2)')
    plt.ylabel('# of pulsars')
    plt.yscale('log')
    plt.xscale('log')
    plt.legend()
    '''
    plt.figure(fig_num+3)
    plt.hist(lum_1400,1000,label=label)

    plt.legend()
    '''
    plt.figure(fig_num+4)
    plt.hist(spindex,100,label=label)
    plt.xlabel('spectral index')
    plt.ylabel('# of pulsars')
    plt.legend()
    plt.figure(fig_num+7)
    plt.hist(period,100,label=label)
    plt.xlabel('log 10(period)')
    plt.ylabel('# of pulsars')
    plt.legend()
    try:
        plt.figure(fig_num+5)
        plt.hist(gains,bins=100,label=label)
        plt.title('gains')
        plt.xlabel('gains K/Jy')
        plt.ylabel('# of pulsars')
        plt.legend()

        plt.figure(fig_num+6)
        plt.hist(tobs,label=label,bins=100)
        plt.title('observation time')
        plt.xlabel('t_obs s')
        plt.ylabel('# of pulsars')
        plt.legend()
    except Exception as e:
        pass
    plt.figure(fig_num+8)
    plt.hist(dm,label=label,bins=100)
    plt.ylabel('dm')

    return gains,tobs


pop_gains,pop_tobs = plot_surv_coord(pop,0.5,1,False,'Synthesized population')
surv_gains,surv_tobs = plot_surv_coord(survey,1,1,True,'CHIME survey')

plt.show()
