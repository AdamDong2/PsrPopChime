import sys
sys.path.append('/home/adam/Documents/PSRPOPPY/PsrPopChime/lib/python')
import populate,dosurvey
from matplotlib import pyplot as plt
import numpy as np
pop = populate.generate(112000,siDistPars=[-1, 2])
pop.write(sys.argv[1])
'''
pop = np.load(sys.argv[1],allow_pickle=1)
surveyPopulations = dosurvey.run(pop, ['CHIME'],alpha=-4,br_mu=1.2,br_sigma=5,rratssearch=1)
survpop=surveyPopulations[0][1]
pulsars = survpop.population
si = list(psr.spindex for psr in pulsars)
print(len(si))
plt.hist(si,bins=100)
plt.xlabel('Spectral Index')
plt.ylabel('number')
plt.show()
'''
#print(surveyPopulations.__dict__)
#dosurvey.write(surveyPopulations)
