###http://pyfftw.readthedocs.io/en/latest/source/tutorial.html#quick-and-easy-the-pyfftw-interfaces-module
##https://docs.scipy.org/doc/scipy-0.18.1/reference/tutorial/fftpack.html
##from scipy.fftpack import fft
# esta utiliza la ventana de hamming para la grafica

import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
import math

from grafica import test_fftw

class fourier:
  # obtener datos de vibracion

  numMuestras = 32768   # muestras analizadas por fft
  window = np.hamming(numMuestras)

  # Sampling rate
  sampleFrec = 50
  
  # Frequency resolution
  resolutionFreq = float(sampleFrec) / float(numMuestras)
  
  # Nyquist frequency
  NyquistFreq = sampleFrec / 2
  
  # Half of frequency vector
  def getFrequency(self):
    if (self.numMuestras % 2 == 0):
        return np.linspace(0, self.NyquistFreq, self.numMuestras / 2 + 1)
    else:
        return np.linspace(0, self.NyquistFreq, (self.numMuestras + 1) / 2)
 
  ''' recibe 3 arrays, en este caso de vibraciones obtenidas del sensor
   retorna 3 arrays listo para el grafico de hamming windows
   en teoria el array debe de ser en float '''
  def getData_to_HammingW(self, ax, ay, az):
    #para trabajar con las cantidades de muestras que se indica
    ax = ax[0: self.numMuestras]
    ay = ay[0: self.numMuestras]
    az = az[0: self.numMuestras]

    # para convertir a flotante
    ax = np.asfarray(ax,float) 
    ay = np.asfarray(ay,float) 
    az = np.asfarray(az,float)
    
    aRms = [math.sqrt(math.pow(x,2) +math.pow(y,2) + math.pow(z,2)) for (x, y, z) in zip(ax, ay, az)]   

    # para obtener valores para el hamming
    ax = np.multiply(ax, self.window)
    ay = np.multiply(ay, self.window)
    az = np.multiply(az, self.window)
    aRms = np.multiply(aRms, self.window)
    
    return aRms, ax, ay, az
##    return aRms

  # extract magnitude and only take half(fft is mirrored)
  # utilizado para graficar la magnitud en la funcion plotFourier
  def extractMagnitude(self, dataFourier):
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
    
  # recibe como parametro un array con datos listos con la ventana de hamming.
  # grafica fourier con eje logaritmos
  def plotFourier(self, hammingData):
    plt.ion()
    
    while (True):
##      vibrationFourier = fft(hammingData)
      vibrationFourier = fft(hammingData, self.numMuestras)
      
      # extract magnitude and only take half(fft is mirrored)
      mag = self.extractMagnitude(vibrationFourier)
      
      plt.clf()
      freq = self.getFrequency()
      plt.semilogx(freq, mag, linewidth=2)

      axes = plt.gca()
      axes.grid()
      plt.pause(2) # seconds
      plt.show()

# obtener datos del sensor
datos = test_fftw("sensor1")
x, y, z = datos.getArrayMediciones()

#alisto los datos para la ventana de hamming
f = fourier()
arms, ax, ay, az= f.getData_to_HammingW(x, y, z)

# grafico la aceleracion arms
f.plotFourier(ay)


