#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt


##np.hamming(12)
##
##array([ 0.08      ,  0.15302337,  0.34890909,  0.60546483,  0.84123594,
##        0.98136677,  0.98136677,  0.84123594,  0.60546483,  0.34890909,
##        0.15302337,  0.08      ])

from numpy.fft import fft, fftshift
window = np.hamming(51)
##plt.plot(window)
##
##plt.title("Hamming window")
##plt.ylabel("Amplitude")
##plt.xlabel("Sample")
##plt.show()

plt.figure()
A = fft(window, 2048) / 25.5
mag = np.abs(fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(mag)
response = np.clip(response, -100, 100)
plt.plot(freq, response)
plt.title("Frequency response of Hamming window")
plt.ylabel("Magnitude [dB]")
plt.xlabel("Normalized frequency [cycles per sample]")
plt.axis('tight')
plt.show()
