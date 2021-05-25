import numpy as np
import matplotlib.pyplot as plt
import sys

a = np.load(sys.argv[1],allow_pickle=1)
plt.plot(a[1],a[0])
plt.title('')
plt.xlabel('beta')
plt.ylabel('delta n detections')
plt.axhline(y=0, color='r', linestyle='--')
plt.show()

