from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt
import numpy as np

window = np.bartlett(51)
##plt.plot(window)
##
##plt.title("Bartlett window")
##
##plt.ylabel("Amplitude")
##
##plt.xlabel("Sample")
##
##plt.show()
##plt.figure()


A = fft(window, 2048) / 25.5
mag = np.abs(fftshift(A))
freq = np.linspace(-0.5, 0.5, len(A))
response = 20 * np.log10(mag)
response = np.clip(response, -100, 100)
plt.plot(freq, response)

plt.title("Frequency response of Bartlett window")

plt.ylabel("Magnitude [dB]")

plt.xlabel("Normalized frequency [cycles per sample]")

plt.axis('tight')

plt.show()