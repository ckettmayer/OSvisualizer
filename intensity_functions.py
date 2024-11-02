# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 11:54:06 2024

@author: ckettmayer
"""

### Intensity functions for different PSF shapes ###

import numpy as np


# ORBITAL SCANNING
# Intensity function for orbital scanning with a gaussian PSF
def Iorb_gauss(A,theta,r,phi,I0,w0):
    return(I0*np.exp(-(2/w0**2)*(A**2+r**2-2*A*r*np.cos(theta-phi))))

# Intensity function for orbital scanning with a donut PSF
def Iorb_donut(A,theta,r,phi,I0,w0):
    return(I0*2*np.e*(A**2+r**2-2*A*r*np.cos(theta-phi))/(w0**2)*np.exp(-(2/w0**2)*(A**2+r**2-2*A*r*np.cos(theta-phi))))


# RASTER SCANNING
# Intensity function for raster scanning with a gaussian PSF
def Iras_gauss(xs,ys,x,y,I0,w0):
    return(I0*np.exp(-(2/w0**2)*((x-xs)**2+(y-ys)**2)))

# Intensity function for raster scanning with a donut PSF
def Iras_donut(xs,ys,x,y,I0,w0):
    return(I0*2*np.e*((x-xs)**2+(y-ys)**2)/(w0**2)*np.exp(-(2/w0**2)*((x-xs)**2+(y-ys)**2)))