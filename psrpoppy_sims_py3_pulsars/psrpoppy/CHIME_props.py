import numpy as np
import galacticops as go
def calc_gain(pulsar):                        
          ra, dec = go.lb_to_radec(pulsar.gl, pulsar.gb)      
                                           
          dec_chime = 49.31                            
          diff=dec-49.31                         
          G_0 = np.abs(1.44*np.cos(np.radians(diff)))    
          return G_0                                                
def calc_tobs(pulsar):                                         
          ra, dec = go.lb_to_radec(pulsar.gl, pulsar.gb)    
          t_obs = 60*np.abs(10/np.cos(np.radians(dec)))                                     
          #stacked searching                    
          #t_obs = 365*60*np.abs(10/np.cos(np.radians(dec)))                     
          return t_obs  
