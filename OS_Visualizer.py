# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 17:25:31 2023

@author: ckettmayer
"""

### Orbital scanning visualizer ###

# import addcopyfighandler
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from intensity_functions import Iorb_gauss
from intensity_functions import Iorb_donut
from fourier_function import fourier


#%%

# Instrumental parameters
I0 = 1    # Intensity

w0 = 300  # Instrumental waist

N = 100   # Points per orbit

A = 150   # Orbit radius
theta = np.linspace(0, 2*np.pi, N)

r = 100   # Particle radial position
phi = np.pi/2     # Particle angular position
#Theta and phi variables are stored in radians, but are plotted in degrees

l = 200         # diameter of the max area in the polar plot


# Choose the PSF shape: 'g' for Gaussian (central max) or 'd' for Donut (central min)
psf_shape = 'g'
# psf_shape = 'd'





psf_functions = {
    'g': Iorb_gauss, 
    'd': Iorb_donut  
}

if psf_shape.lower() in psf_functions:
    Iorb = psf_functions[psf_shape.lower()]
else:
    raise ValueError("Invalid PSF shape. Use 'g' for Gaussian or 'd' for Donut.")
    
    

# intensity colormaps
colors = Iorb(A,theta,r,phi,I0,w0)
cm = 'viridis'
norm = mpl.colors.Normalize(vmin=0, vmax=I0) 
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])



# PLOT
fig = plt.figure(figsize=(6,7))
gs = fig.add_gridspec(2, 1, height_ratios=[2, 1], hspace=0.3, wspace=0.2)

fig.suptitle(f'I0={I0}, w0={w0}nm, N={N}, A={A}nm, r={r}nm, $\\varphi$={phi*180/np.pi:.0f}$^{{\circ}}$')


# Polar plot
ax1 = fig.add_subplot(gs[0], projection='polar')
ax1.scatter(theta, theta*0+A, c=colors, marker='o', s=100, cmap=cm, norm=norm)
ax1.scatter(phi,r, color='y', marker='*', s=250, edgecolors='k', zorder=3)

ax1.set_ylim(0, l)
ax1.set_yticks(np.linspace(0, l, 5)) 

cbar = fig.colorbar(sm, ax=ax1, pad=0.1, shrink=0.5)
cbar.set_label('Intensity (a.u.)')


#Intensity plot       
ax2 = fig.add_subplot(gs[1])
ax2.scatter(theta*180/np.pi, Iorb(A,theta,r,phi,I0,w0), c=colors, marker='o', s=100, cmap=cm, norm=norm,  zorder=2)


ax2.set_xlabel(r'$\theta$ ($^{\circ}$)')
ax2.set_ylabel('I (a.u.)')
ax2.set_ylim(0, I0+0.1*I0)
ax2.set_xticks(np.linspace(0,360,9)) 
ax2.grid()



