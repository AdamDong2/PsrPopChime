import numpy as np
import dist_gen as dg
import pylab as plt

hist=np.array([ 0.11182463,  0.14909951,  0.44729857,  0.55912316,  0.41002366,  0.33547392,  0.26092415])
bins=np.array([ 1.56584782,  2.0056465 ,  2.44544518,  2.88524386,  3.32504254, 3.76484123,  4.20463991,  4.64443859])
some=[]
for i in range(1000):
    some.append(dg.gen_nos(hist,bins))
plt.hist(some,bins=7,range=[1.5,4.7],normed=1)
plt.show()
