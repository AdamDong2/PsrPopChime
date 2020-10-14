import numpy as np
import matplotlib.pyplot as plt
import sys
fn = sys.argv[1]

trace= np.load(fn,allow_pickle=1)
keys = trace[0].keys()

for key in keys:
    my_key=[]
    for val in trace:
        if key=='alpha':
            val[key]=np.log10(val[key])
        my_key.append(val[key])
    plt.figure()
    plt.hist(my_key,bins=100)
    plt.title(key)
plt.show()
