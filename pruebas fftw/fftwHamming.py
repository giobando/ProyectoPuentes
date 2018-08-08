###http://pyfftw.readthedocs.io/en/latest/source/tutorial.html#quick-and-easy-the-pyfftw-interfaces-module
##https://docs.scipy.org/doc/scipy-0.18.1/reference/tutorial/fftpack.html
##from scipy.fftpack import fft
# esta utiliza la ventana de hamming para la grafica

import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
import math
import time 

from grafica import test_fftw

class fourier:
  numMuestras = 16384 #32768     # muestras analizadas por fft
  window = np.hamming(numMuestras)
  sampleFrec = 1000              # Sampling rate
  resolutionFreq = float(sampleFrec) / float(numMuestras) # Frequency resolution
  NyquistFreq = sampleFrec / 2  # Nyquist frequency
     
  ''' recibe: list de vibraciones float obtenidas del sensor
      retorna: arrays para el grafico '''
  def getData_to_HammingW(self, ax, ay, az,aRms):       # Paso 1. Se obtiene dato con hamming data
    # Se toma una cantidad de datos para fourier
    ax = ax[0: self.numMuestras]
    ay = ay[0: self.numMuestras]
    az = az[0: self.numMuestras]
    aRms = aRms[0: self.numMuestras]

    # String -> flotante
    ax = np.asfarray(ax,float) 
    ay = np.asfarray(ay,float) 
    az = np.asfarray(az,float)
    aRms = np.asfarray(aRms, float)

    # Valores Hamming windows
    ax = np.multiply(ax, self.window)
    ay = np.multiply(ay, self.window)
    az = np.multiply(az, self.window)
    aRms = np.multiply(aRms, self.window)    
    return aRms, ax, ay, az

  def get_MagnitudeFourier(self, dataFourier):          # Paso 2. Calcular Magnitud
    if (self.numMuestras % 2 == 0):
      mag = np.abs(dataFourier) / float(self.numMuestras)
      mag = mag[0:(self.numMuestras / 2 + 1)]
      mag[0:-2] = 2.0 * mag[0:-2]
      #phase = unwrap(angle(Y(1:N / 2 + 1)))
      return mag      
    else:
      mag = np.abs(dataFourier) / float(self.numMuestras)
      mag = mag[0:(self.numMuestras + 1) / 2]
      mag[1:-2] = 2 * mag[1:-2]
      #phase = unwrap(angle(Y(1:(N + 1) / 2)));
      return mag
  
  def getFrequency(self):                             # Paso 3. Half of frequency vector 
    if (self.numMuestras % 2 == 0):
        return np.linspace(0, self.NyquistFreq, self.numMuestras / 2 + 1)
    else:
        return np.linspace(0, self.NyquistFreq, (self.numMuestras + 1) / 2)    
  
  def graficarFourier(self, hammingData, titulo):      # Paso 4. Graficar Fourier
##    plt.ion()
    
##    while (True):
    vibrationFourier = fft(hammingData, self.numMuestras)      
    mag = self.get_MagnitudeFourier(vibrationFourier)
##      self.get_PeakFourier(mag)
    
##    plt.clf()
    freq = self.getFrequency()
    plt.plot(freq,mag, linewidth=2)
##      plt.ylim(ymax = 0.002)
    
    axes = plt.gca()
    axes.grid()
##    plt.pause(2) # seconds
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain (' + titulo + ') \n with Hamming')
    plt.show()

# obtener datos del sensor
datos = test_fftw("sensor1")
mediciones = datos.getArrayMediciones()
x = mediciones["x"]
y = mediciones["y"]
z = mediciones["z"]
rms = mediciones["rms"]
t = mediciones["time"]

# Preparamos para Fourier
f = fourier()
arms, ax, ay, az= f.getData_to_HammingW(x, y, z, rms)

# grafico la aceleracion arms
titulo= "az"
f.graficarFourier(rms,titulo)


