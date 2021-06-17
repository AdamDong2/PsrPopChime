import pymc3 as pm
observed = 247
with pm.model():
    alpha=pm.Normal('alpha',mu=-3,sd=1)
    br = pm.Normal('br',mu=0.5,sd=0.1)


