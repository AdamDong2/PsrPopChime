import numpy as np
import matplotlib.pyplot as plt
import sys
a = np.load(sys.argv[1],allow_pickle=1)
ndet=a[0]
params=a[1]

sigma_array = list(param['beta_sp'] for param in params)
sigma_std_arr = list(param['beta_sp_std'] for param in params)
plt.figure()
plt.xlabel('sigma')
plt.ylabel('sigma_std')
plt.scatter(sigma_array,sigma_std_arr,c=ndet)
bar=plt.colorbar()
bar.set_label('ndet')
plt.show()
