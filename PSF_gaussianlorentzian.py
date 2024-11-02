# -*- coding: utf-8 -*-
"""
Created on Tue Nov 14 12:55:45 2023

@author: ckettmayer
"""

### Gaussian lorentzian PSF 3D ###

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl


def I_gausslor(x,y,z,xs,ys,zs,I0,l,w):        
    return ( (2*I0) / (np.pi*(1+ ((z-zs)**2*l**2)/(np.pi**2 *w**4) )) * np.exp(- 2* ((x-xs)**2+(y-ys)**2)/(w**2*(1+((z-zs)*l/(np.pi**2 *w**2))**2)) ) )


l = 780 #wave lenght

w = 300 #instrumental waist

I0 = 1 #intensity amplitude


xs, ys, zs = 0 , 0 , 0  # centered scanner 


N = 100
s = 4*w
x = np.linspace(-s, s, N)
y = np.linspace(-s, s, N)
z = np.linspace(-s, s, N)

# 3D mesh
X, Y, Z = np.meshgrid(x, y, z)

I = I_gausslor(X, Y, Z, xs, ys, zs, I0, l, w)


# PLOT

fig, axes = plt.subplots(1, 4, figsize=(12, 4), gridspec_kw={'width_ratios': [1, 1, 1, 0.05], 'wspace': 0.7})

norm = mpl.colors.Normalize(vmin=0, vmax=np.amax(I))  #normalized colormap
sm = mpl.cm.ScalarMappable(cmap='inferno', norm=norm)
sm.set_array([])

# XY plane
axes[0].imshow(I[:, :, 50], extent=[x.min(), x.max(), y.min(), y.max()], cmap='inferno', norm=norm)  #uso el colormap cm con la norma norm
axes[0].set_title('XY plane (Z=0)')
axes[0].set_xlabel('X (nm)')
axes[0].set_ylabel('Y (nm)')
axes[0].grid(False)

# XZ plane
axes[1].imshow(I[50, :, :].T, extent=[z.min(), z.max(), x.min(), x.max()], cmap='inferno', norm=norm)  
axes[1].set_title('XZ plane (Y=0)')
axes[1].set_xlabel('X (nm)')
axes[1].set_ylabel('Z (nm)')
axes[1].grid(False)

# YZ plane
axes[2].imshow(I[:, 50, :].T, extent=[z.min(), z.max(), y.min(), y.max()], cmap='inferno', norm=norm)
axes[2].set_title('YZ plane (X=0)')
axes[2].set_xlabel('Y (nm)')
axes[2].set_ylabel('Z (nm)')
axes[2].grid(False)


axes[3].set_position([0.87, 0.28, 0.015, 0.4])
cbar = plt.colorbar(sm, cax=axes[3], label='I (a.u.)', aspect=10)
cbar.set_label('Intensity (a.u.)')    


fig.suptitle(r'$\lambda$='+str(l)+'nm, w$_0$='+str(w)+'nm')








