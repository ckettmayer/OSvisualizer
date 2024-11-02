# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 11:40:22 2023

@author: ckettmayer
"""

### Interactive orbital scanning visualizer ###

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
from matplotlib.widgets import Slider
from intensity_functions import Iorb_gauss
from intensity_functions import Iorb_donut
from fourier_function import fourier
# import addcopyfighandler



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

l = 400         # max particle distance from origin



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

    


# PLOTS    

fig = plt.figure(figsize=(6, 8))

gs = fig.add_gridspec(3, 1, height_ratios=[2,0.7,0.4], hspace=0.3, wspace=10)


# Sliders for r, phi and A
ax_parameter_r = plt.axes([0.17, 0.15, 0.65, 0.03], facecolor='lightgoldenrodyellow')   #[left, bottom, width, height]
slider_r = Slider(ax_parameter_r, 'r', 0, l, valinit=r)  #select initial values

ax_parameter_phi = plt.axes([0.17, 0.1, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_phi = Slider(ax_parameter_phi, r'$\varphi$', 0, 360, valinit= 90)    # slider values are showed in degrees, but calculations are done in radians

ax_parameter_A = plt.axes([0.17, 0.05, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider_A = Slider(ax_parameter_A, 'A', 50, l, valinit=A)   




# POLAR PLOT
       
fig.suptitle(f'I0 = {I0}, w0 = {w0} nm, N = {N}')

ax1 = fig.add_subplot(gs[0], projection='polar')

# Polar mesh for PSF plot
xplot = np.linspace(-1.5*l,1.5*l,100)
yplot = np.linspace(-1.5*l,1.5*l, 150)
X, Y = np.meshgrid(xplot, yplot)

R, Phi = np.sqrt(X**2 + Y**2), np.arctan2(Y, X)


# Custom colormap white-red for PSF
color_max = 'red'  
color_min = 'white'
cmap_segments = {
    'red': [(0.0, 1.0, 1.0), (1.0, 1.0, 1.0)],  
    'green': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)], 
    'blue': [(0.0, 0.0, 0.0), (1.0, 1.0, 1.0)]  
}
custom_cmap = mcolors.LinearSegmentedColormap('custom_colormap', cmap_segments, 256)


# Colormap for intensity
colors = Iorb(A,theta,r,phi,I0,w0)
cm = 'viridis'
norm = mpl.colors.Normalize(vmin=0, vmax=I0)  
sm = mpl.cm.ScalarMappable(cmap=cm, norm=norm)
sm.set_array([])


ax1.scatter(Phi, R, c=Iorb(R, Phi, A, phi, I0, w0), marker='o', s=10, cmap = custom_cmap.reversed(), zorder=1)     #PSF   
ax1.scatter(theta, theta*0+A, c=colors, marker='o', s=100, cmap=cm, norm=norm, alpha=1)                            #orbit
ax1.scatter(phi, r, color='y', marker='*', s=250, edgecolors='k', zorder=3)                                        #particle


ax1.set_ylim(0, l+50)
ax1.set_yticks(np.linspace(0, 400, 5)) 




# INTENSITY AND MODULATION PLOT

ax2 = fig.add_subplot(gs[1])
ax2.scatter(theta*180/np.pi, Iorb(A,theta,r,phi,I0,w0), c=colors, marker='o', s=100, cmap=cm, norm=norm,  zorder=2)

ax2.grid()
ax2.set_xlabel(r'$\theta$ ($^{\circ}$)')
ax2.set_ylabel('I (a.u.)')
ax2.set_ylim(-0.1*I0, I0+0.1*I0)
ax2.set_xticks(np.linspace(0,360,9)) 


x = theta*180/np.pi
y = Iorb(A,theta,r,phi,I0,w0)
t0,t1 = fourier(x,y)[2], fourier(x,y)[3]

ax2.plot(x,x*0+t0, color='k')         # 0th order fourier 
ax2.plot(x,t0+t1, color='b')          # 1st order fourier 
mod = fourier(x,y)[1]/fourier(x,y)[0]   # Calculate and show modulation as A1/A0
ax2.text(0.95, 0.92, f'Mod = {mod:.2f}',
         transform=ax2.transAxes,  
         fontsize=12, 
         bbox=dict(facecolor='white', edgecolor='black', linewidth=0.5), 
         verticalalignment='top', 
         horizontalalignment='right')


# Update function for updating plots based on slider values
def update(val):
    ax1.clear()
    ax2.clear()
    ax2.grid()
    
    r = slider_r.val
    phi = slider_phi.val
    A = slider_A.val
    
    colors = Iorb(A,theta,r,phi*np.pi/180,I0,w0)
    ax1.scatter(Phi, R, c=Iorb(R, Phi, A, phi*np.pi/180, I0, w0), marker='o', s=10, cmap = custom_cmap.reversed(), zorder=1)    #PSF
    ax1.scatter(theta, theta*0+A, c=colors, marker='o', s=100, cmap=cm, norm=norm, alpha=1)   #orbit
    ax1.scatter(phi*np.pi/180, r, color='y', marker='*', s=250, edgecolors='k', zorder=3)    #particle
    
    ax2.scatter(theta*180/np.pi, colors, c=colors, marker='o', s=100, cmap=cm, norm=norm, zorder=2)
    
    x = theta*180/np.pi
    y = Iorb(A,theta,r,phi*np.pi/180,I0,w0)
    t0,t1 = fourier(x,y)[2], fourier(x,y)[3]
    ax2.plot(x,x*0+t0, color='k')      # 0th order fourier 
    ax2.plot(x,t0+t1, color='b')       # 1st order fourier  
    mod = fourier(x,y)[1]/fourier(x,y)[0] # Calculate and show modulation as A1/A0
    
    ax2.text(0.95, 0.92, f'Mod = {mod:.2f}',
             transform=ax2.transAxes,  
             fontsize=12, 
             bbox=dict(facecolor='white', edgecolor='black', linewidth=0.5), 
             verticalalignment='top', 
             horizontalalignment='right')
    
    ax1.set_ylim(0, l+50)
    ax1.set_yticks(np.linspace(0, 400, 5)) 


    ax2.set_xlabel(r'$\theta$ ($^{\circ}$)')
    ax2.set_ylabel('I (a.u.)')
    ax2.set_ylim(-0.1*I0, I0+0.1*I0)
    ax2.set_xticks(np.linspace(0,360,9)) 
    
    fig.canvas.draw_idle()
    
       
cbar = fig.colorbar(sm, ax=ax1, pad=0.1, shrink=0.5)
cbar.set_label('Intensity (a.u.)')    


slider_r.on_changed(update)
slider_phi.on_changed(update)
slider_A.on_changed(update)

