import numpy as np
import matplotlib.pyplot as plt
import sys
a = np.load(sys.argv[1],allow_pickle=1)
ndet=a[0]
params=a[1]
sigma=a[2]
sigma_std=a[3]

sigma_array = list(param['beta_sp'] for param in params)
sigma_std_arr = list(param['beta_sp_std'] for param in params)
'''        
ndet = np.reshape(ndet,(len(sigma),len(sigma_std)))
sigma_array = np.reshape(sigma_array,(len(sigma),len(sigma_std)))
sigma_std_arr = np.reshape(sigma_std_arr,(len(sigma),len(sigma_std)))
mask = np.zeros_like(ndet,dtype=bool)
mask[ndet>500]=True
mask[ndet<-200]=True
ndet = np.ma.array(ndet,mask=mask)
plt.contourf(sigma_array,sigma_std_arr,ndet,levels=100,corner_mask=False)
bar=plt.colorbar()
cp=plt.contour(sigma_array,sigma_std_arr,ndet,levels=[-100,0,100],colors='white',linestyles='dashed')
ndet_paths = {"-100":cp.collections[0].get_paths()[0]._vertices,"0":cp.collections[1].get_paths()[0]._vertices,"100":cp.collections[2].get_paths()[0]._vertices}
np.save('paths',ndet_paths)
plt.clabel(cp,inline=True,fontsize=10)
bar.set_label('delta ndet')
plt.xlabel('Sigma')
plt.ylabel('Sigma_std')
plt.show()
'''

plt.plot(sigma,ndet)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('sigma')
plt.ylabel('delta_ndet')
plt.show()

