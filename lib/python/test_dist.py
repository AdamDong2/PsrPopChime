import matplotlib.pyplot as plt
import numpy as np
import distributions as d

a=[]
for i in range(int(1e6)):
    a.append(d.power_law_orig(1,100,-2.1))
b=d.powerlaw(-2.1,1,100,int(1e6))

plt.figure(1)
plt.hist(a,bins=100)
plt.xscale('log')
plt.yscale('log')
plt.figure(2)
plt.hist(b,bins=100)
plt.xscale('log')
plt.yscale('log')
plt.show()
