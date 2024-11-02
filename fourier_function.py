# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 11:56:22 2024

@author: Constanza
"""

### Fourier series function for modulation calculation ###

import numpy as np
from scipy.fft import fft


def fourier(x,y): 
    fft_values = fft(y)
    a0 = 2 * fft_values[0].real / len(x)
    a1 = 2 * fft_values[1].real / len(x)
    b1 = - 2 * fft_values[1].imag / len(x)
    
    A0 = (a0/2)
    A1 = (a1**2+b1**2)**(1/2)
    F1 = np.mod(np.arctan2(b1, a1), 2 * np.pi)
    
    t0 = A0
    t1 = A1 * np.cos(x*np.pi/180 - F1)  

    return (A0,A1,t0,t1)