import sys
sys.path.append('/home/adam/anaconda3/envs/CHIME/lib/python3.8/psrpoppy')
from psrpoppy import populate,dosurvey
from matplotlib import pyplot as plt
import numpy as np
pop = populate.generate(1024,['PMSURV'])
#pop.write(sys.argv[1])
#pop = np.load('regular_pulsar',allow_pickle=1)
surveyPopulations = dosurvey.run(pop, ['CHIME'])
#dosurvey.write(surveyPopulations)
