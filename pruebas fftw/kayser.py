
import matplotlib.pyplot as plt

import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
plt.figure()
window = np.kaiser(51, 14)

A = fft(window, 2048) / 25.5
mag = np.abs(fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(mag)
response = np.clip(response, -100, 100)
plt.plot(freq, response)

plt.title("Frequency response of Kaiser window")

plt.ylabel("Magnitude [dB]")

plt.xlabel("Normalized frequency [cycles per sample]")
plt.axis('tight')
plt.show()
