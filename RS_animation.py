# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 16:12:28 2023

@author: ckettmayer
"""

### Raster scanning animation ###


import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.animation import FuncAnimation
from intensity_functions import Iras_gauss
from intensity_functions import Iras_donut


# Instrumental parameters

I0 = 1    # Intensity

w0 = 150  # Instrumental waist


# Particle position
x = 300
y = 300


# Choose the PSF shape: 'g' for Gaussian (central max) or 'd' for Donut (central min)
# psf_shape = 'g'
psf_shape = 'd'

M = 12       # Number of pixels in raster scan (between 5 and 30)



psf_functions = {
    'g': Iras_gauss, 
    'd': Iras_donut  
}

if psf_shape.lower() in psf_functions:
    Iras = psf_functions[psf_shape.lower()]
else:
    raise ValueError("Invalid PSF shape. Use 'g' for Gaussian or 'd' for Donut.")

A = 500

xs, ys = A/2 , A/2




# Create a polar mesh for PSF plot
xplot = np.linspace(0,A,100)
yplot = np.linspace(0,A,100)
X, Y = np.meshgrid(xplot, yplot)


# Intensity colormap
colors = Iras(xs,ys,x,y,I0,w0)
cm = 'viridis'
norm = mpl.colors.Normalize(vmin=0, vmax=I0)  #modifico la normalización de los colores para que vaya entre dos valores fijos
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])



#Custom colormap white-red for PSF
color_max = 'red'  
color_min = 'white'
cmap_segments = {
    'red': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],    
    'green': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)],  
    'blue': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]    
}
custom_cmap = mcolors.LinearSegmentedColormap('custom_colormap', cmap_segments, 256)




S = A / M   

s = 20000 * np.exp(-0.37*M) - 17 * M + 615

# Update function for animation
def update(frame):
    ax1.cla()
      
    xp = S * (frame % M) + S/2
    yp =  A - (frame // M) * S  - S/2

    ax1.scatter(X, Y, c=Iras(xp,yp,X,Y,I0,w0), marker='o', s=10, cmap = custom_cmap.reversed(), zorder=1)    # PSF
    ax1.scatter(x, y, color='y', marker='*', s=500, edgecolors='k', zorder=3)                                # Particle
    ax2.scatter(xp, yp, c=Iras(xp,yp,x,y,I0,w0), cmap = cm, norm = norm, marker='s', s=s)                    # Pixel
    
    ax1.set_ylim(0,A)
    ax1.set_xlim(0,A)

    ax1.set_xticks([])
    ax1.set_yticks([])
    ax2.set_xticks([])
    ax2.set_yticks([])

    ax1.set_aspect('equal')
    ax2.set_aspect('equal')
    
    

# PLOT

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

ax1.set_ylim(0,A)
ax1.set_xlim(0,A)
ax2.set_ylim(0,A)
ax2.set_xlim(0,A)

ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])

ax1.set_aspect('equal')
ax2.set_aspect('equal')



# Creates the animation
animation = FuncAnimation(fig, update, frames=M*M, interval=100)

# Saves the animation
# animation.save('raster_animation.gif', writer='pillow', fps=30)

plt.show()







