#!/usr/bin/env python

import sys
import argparse
import math
import random
import distributions
from population import Population
from pulsar import Pulsar
from survey import Survey
from CHIME_props import calc_gain
from CHIME_props import calc_tobs
if sys.version_info[0] < 3:
    import cPickle
else:
    import pickle as cPickle

class Detections:
    """Just a simple object to store survey detection summary"""
    def __init__(self,
                 ndet=None,
                 ndisc=None,
                 nsmear=None,
                 nout=None,
                 nbr=None,
                 ntf=None):
        self.ndet = ndet
        self.ndisc = ndisc
        self.nsmear = nsmear
        self.nout = nout
        self.nbr = nbr
        self.nfaint = ntf


def loadModel(popfile='populate.model', popmodel=None):
    """Loads in either a model from disk (popfile, cPickle),
       or pass in a model from memory (popmodel)"""
    if popmodel is None:
        with open(popfile, 'rb') as f:
            pop = cPickle.load(f)
    else:
        pop = popmodel

    return pop


def write(surveyPops,
          extension='.results',
          nores=False,
          asc=False,
          summary=False):
    """Write a survey results population to a binary file."""

    for surv, survpop, detected in surveyPops:
        # create an output file, if required
        if not nores:
            if surv is not None:
                s = ''.join([surv, extension])

                survpop.write(s)
            else:
                s = 'allsurveys.results'
                survpop.write(s)

        # Write ascii file if required
        if asc and surv is not None:
            survpop.write_asc(surv + '.det')

        if summary and surv is not None:
            # Write a summary file for the survey (if true)
            filename = ''.join([surv, '.summary'])
            s = 'Detected {0}'.format(detected.ndet)
            s = '\n'.join([s, 'Ndiscovered {0}'.format(detected.ndisc)])
            s = '\n'.join([s, 'Nsmear {0}'.format(detected.nsmear)])
            s = '\n'.join([s, 'Nfaint {0}'.format(detected.nfaint)])
            s = '\n'.join([s, 'Nout {0}'.format(detected.nout)])
            s = '\n'.join([s, 'Nbr {0}'.format(detected.nbr)])
            s = ''.join([s, '\n'])

            with open(filename, 'w') as output:
                output.write(s)


def run(pop,
        surveyList,
        beta_sp=0,
        beta_sp_std=0,
        br_mu=0,
        br_sigma=0,
        nostdout=False,
        allsurveyfile=False,
        scint=False,
        accelsearch=False,
        jerksearch=False,
        rratssearch=False,
        rrat_distribution='lnorm',
        giantpulse=False,
        dos=0):

    """ Run the surveys and detect the pulsars."""

    # print the population
    if not nostdout:
        print("Running doSurvey on population...")
        print(pop)

    # loop over the surveys we want to run on the pop file
    surveyPops = []
    for surv in surveyList:
        s = Survey(surv,dos=dos)
        s.discoveries = 0
        if not nostdout:
            print("\nRunning survey {0}".format(surv))

        # create a new population object to store discovered pulsars in
        survpop = Population()
        allpop = Population()
        # HERE SHOULD INCLUDE THE PROPERTIES OF THE ORIGINAL POPULATION

        # counters
        nsmear = 0
        nout = 0
        ntf = 0
        ndet = 0
        nbr = 0
        # loop over the pulsars in the population list
        #do this if BR is different from period
        if rratssearch:
            #should really draw the burst rate in the generate population stage
            #br = distributions.augmenteddrawlnorm(br_mu,br_sigma,len(pop.population))
            br = distributions.drawlnorm(br_mu,br_sigma,len(pop.population))

        
        #plot burst rates
        plot=0
        if plot:
            import distributions as dist
            import matplotlib.pyplot as plt
            import numpy as np
            dist.plot_loghist(br,1000)
            plt.show()
        
        '''
        import matplotlib.pyplot as plt
        lum = list(psr.lum_inj_mu for psr in pop.population)
        import distributions as dist
        dist.plot_loghist(lum,1000)
        plt.show()
        ''' 
        for i,psr in enumerate(pop.population):
            # pulsar could be dead (evolve!) - continue if so
            #print('hi')
            if psr.dead:
                continue
            #draw burst rate
            psr.br = br[i]
            #ADAM EDIT: If the survey is CHIME/FRB, need to set custom gain and t_obs
            if s.surveyName == 'CHIME':
                s.gain = calc_gain(psr)
                #days on sky * transit time
                s.tobs = s.dos*calc_tobs(psr)
            psr.gain = s.gain
            psr.tobs = s.tobs
            # is the pulsar over the detection threshold?
            snr = s.SNRcalc(psr,pop,beta_sp,beta_sp_std,accelsearch=accelsearch,jerksearch=jerksearch,rratssearch=rratssearch,giantpulse=giantpulse,rrat_distribution=rrat_distribution)
            #print snr
            # add scintillation, if required
            # modifying S/N rather than flux is sensible because then
            # a pulsar can have same flux but change S/N in repeated surveys
            if scint:
                snr = s.scint(psr, snr)

            if snr > s.SNRlimit:
                ndet += 1
                psr.snr = snr
                survpop.population.append(psr)

                # check if the pulsar has been detected in other
                # surveys
                if not psr.detected:
                    # if not, set to detected and increment
                    # number of discoveries by the survey
                    psr.detected = True
                    s.discoveries += 1
            if snr>0:
                #all pulsars that could have possibly been detected
                psr.snr=snr
                allpop.population.append(psr)

            elif snr == -1.0:
                nsmear += 1
            elif snr == -2.0:
                nout += 1
            elif snr == -3.0:
                nbr += 1
            else:
                ntf += 1

        # report the results
        if not nostdout:
            print("Total pulsars in model = {0}".format(len(pop.population)))
            print("Number detected by survey {0} = {1}".format(surv, ndet))
            print("Of which are discoveries = {0}".format(s.discoveries))
            print("Number too faint = {0}".format(ntf))
            print("Number smeared = {0}".format(nsmear))
            print("Number out = {0}".format(nout))
            if rratssearch:
                print("Number didn't burst = {0}".format(nbr))
            if giantpulse:
                print("Number who don't exhibit giant pulses = {0}".format(nbr))
            print("\n")

        d = Detections(ndet=ndet,
                       ntf=ntf,
                       nsmear=nsmear,
                       nout=nout,
                       nbr=nbr,
                       ndisc=s.discoveries)
        surveyPops.append([surv, survpop,allpop, d])
    #survpop is only of detected pulsars. we should do one for all pulsars
    '''
    s_max=[]
    import distributions as dist
    import matplotlib.pyplot as plt
    import numpy as np

    for psr in survpop.population:
        s_max.append(psr.S_max_dect)
    dist.plot_loghist(s_max,1000)
    plt.show()
    '''

    if allsurveyfile:
        allsurvpop = Population()
        allsurvpop.population = [psr for psr in pop.population if psr.detected]
        surveyPops.append([None, allsurvpop, None])

    return surveyPops


if __name__ == '__main__':
    """ 'Main' function; read in options, then survey the population"""
    # Parse command line arguments

    parser = argparse.ArgumentParser(
        description='Run a survey on your population model')
    parser.add_argument(
        '-f', metavar='fname', default='populate.model',
        help='file containing population model (def=populate.model')

    parser.add_argument(
        '-surveys', metavar='S', nargs='+', required=True,
        help='surveys to use to detect pulsars (required)')

    parser.add_argument(
        '--noresults', nargs='?', const=True, default=False,
        help='flag to switch off pickled .results file (def=False)')
    parser.add_argument(
        '--singlepulse', nargs='?', const=True, default=False,
        help='Rotating Radio Transients uses single pulse snr')

    parser.add_argument(
        '--asc', nargs='?', const=True, default=False,
        help='flag to create ascii population file (def=False)')

    parser.add_argument(
        '--summary', nargs='?', const=True, default=False,
        help='flag to create ascii summary file (def=False)')

    parser.add_argument(
        '--nostdout', nargs='?', const=True, default=False,
        help='flag to switch off std output (def=False)')

    parser.add_argument(
        '--allsurveys', nargs='?', const=True, default=False,
        help='write additional allsurv.results file (def=False)')

    parser.add_argument(
        '--scint', nargs='?', const=True, default=False,
        help='include model scintillation effects (def=False)')

    parser.add_argument(
        '--accel', nargs='?', const=True, default=False,
        help='use accel search for MSPs (def=False)')

    parser.add_argument(
        '--jerk', nargs='?', const=True, default=False,
        help='use accel & jerk search for MSPs (def=False)')

    args = parser.parse_args()

    # Load a model population
    population = loadModel(popfile=args.f)
    # run the population through the surveys
    surveyPopulations = run(population,
                            args.surveys,
                            nostdout=args.nostdout,
                            allsurveyfile=args.allsurveys,
                            scint=args.scint,
                            accelsearch=args.accel,
                            jerksearch=args.jerk,
                            rratssearch=args.singlepulse)

    # write the output files
    write(surveyPopulations,
          nores=args.noresults,
          asc=args.asc,
          summary=args.summary)
