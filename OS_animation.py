# -*- coding: utf-8 -*-
"""
Created on Thu Dec 14 14:39:02 2023

@author: ckettmayer
"""

### Orbital scanning animation ###


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from intensity_functions import Iorb_gauss
from intensity_functions import Iorb_donut



# Instrumental parameters

I0 = 1    # Intensity

w0 = 300  # Instrumental waist

N = 64   # Points per orbit

A = 150   # Orbit radius
theta = np.linspace(0, 2*np.pi, N)

r = 100   # Particle radial position
phi = np.pi/2     # Particle angular position





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


l = 350         # max particle distance from origin

# Create a polar mesh for PSF plot
xplot = np.linspace(-l, l, 100)
yplot = np.linspace(-l, l, 150)
X, Y = np.meshgrid(xplot, yplot)
R, Phi = np.sqrt(X**2 + Y**2), np.arctan2(Y, X)

# Intensity colormap
colors = Iorb(A,theta,r,phi,I0,w0)
cm = 'viridis'
norm = mpl.colors.Normalize(vmin=0, vmax=I0)  
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])



# Custom colormap white-red for PSF
color_max = 'red'  
color_min = 'white'
cmap_segments = {
    'red': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],    
    'green': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],  
    'blue': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]    
}
custom_cmap = mcolors.LinearSegmentedColormap('custom_colormap', cmap_segments, 256)


s = 500

# Update function for animation
def update(frame):
    ax1.cla()

    theta_m = theta[frame%N] 
    ax1.plot(theta, theta*0+A, color='grey', linestyle= 'dashed')
    ax1.scatter(Phi, R, c=Iorb(R, Phi, A, theta_m, I0, w0), marker='o', s=10, cmap = custom_cmap.reversed(), zorder=1)    #PSF
    ax1.scatter(phi, r, color='y', marker='*', s=400, edgecolors='k', zorder=3)                                           #particle    
    ax2.scatter(theta_m, A, c=Iorb(A, theta_m, r, phi, I0, w0), marker='o', s=s, cmap=cm, norm=norm, alpha=1)           #orbit
    
    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])
    ax1.set_ylim(0, l)
    ax2.set_ylim(0, l)



fig = plt.figure(figsize=(12, 6))
ax1 = fig.add_subplot(121,projection='polar')
ax2 = fig.add_subplot(122, projection='polar')

ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])
ax1.set_ylim(0, l)
ax2.set_ylim(0, l)


# Creates the animation
animation = FuncAnimation(fig, update, frames=100, interval=50)

# Saves the animation
# animation.save('orbital_animation.gif', writer='pillow', fps=30)

plt.show()
