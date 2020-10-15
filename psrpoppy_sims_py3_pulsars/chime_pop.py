import sys
sys.path.append('/home/adam/anaconda3/envs/CHIME/lib/python3.8/psrpoppy')
from psrpoppy import populate,dosurvey
from matplotlib import pyplot as plt
import numpy as np
#pop = populate.generate(10,['PMSURV'])
#pop.write(sys.argv[1])
pop = np.load('regular_pulsar',allow_pickle=1)
surveyPopulations = dosurvey.run(pop, ['CHIME'],alpha=-2,br_mu=3,br_sigma=6)
#dosurvey.write(surveyPopulations)
