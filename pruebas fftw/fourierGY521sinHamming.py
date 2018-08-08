import numpy as np
import pyfftw
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import math
from grafica import test_fftw

class fourier:
  cantidadMuestras =32768       # muestras analizadas por fft
  sampleFrec = 1000.0           # Sampling rate
  NyquistFreq = sampleFrec / 2  # Nyquist frequency
  carpetaDireccionSave = ""
  _threads = 4

  def set_dirSaveData(self, direccion):
    self.carpertaDireccionSave = direccion

  def get_dirSaveData(self):
    return self.carpetaDireccionSave

  def get_complexFFTW(self, dataListVibration):       # Paso 1. Complex Fourier
##    out = pyfftw.empty_aligned(self.cantidadMuestras, dtype='float32')
##    fft = pyfftw.builders.fft(out)#, planner_effort = 'FFTW_MEASURE', threads = self._threads)
##    out[:] = dataListVibration
##    result = fft()
##    
    result = np.fft.fft(dataListVibration)
    return result

  def get_MagnitudeFFT(self, dataFourierComplexList): # Paso 2. Magnitud FFT
    mag = np.abs(dataFourierComplexList[0:len(dataFourierComplexList)/2+1]) / float(self.cantidadMuestras)
##    mag = mag[0:(self.cantidadMuestras / 2 + 1)]
##    mag[0:-2] = 2.0 * mag[0:-2]
    # probar este>
##    mag =  2 / self.cantidadMuestras * np.abs(dataFourierComplexList[0 : np.int(self.cantidadMuestras / 2)]) 
    return mag  
    
  def getFrequency(self):                             # Paso 3. Half of frequency vector 
    return np.linspace(0, self.NyquistFreq, self.cantidadMuestras / 2 + 1)

  def get_PeakFFT(self, dataMagFourierList, frecuencyList, save=True):  
    peakIndex = 0
    peak = 0
    
    for loop in range(self.cantidadMuestras/2 +1):
      if(save):
        pass
##        FO.write("{0}\t{1}\n".format(frecuencyList[loop], dataMagFourierList[loop])) # 3. guardamos la frecuencia calculada con el fourier
      if loop>0:
         if dataMagFourierList[loop] > peak :         # 4. obtenemos el pico maximo 
           peak = dataMagFourierList[loop]
           peakIndex = loop
    
    return peakIndex
  
  def graficarFourier(self, ejex, ejey, tituloGrafica):      # Paso 5. Graficar Fourier    
##    plt.clf()      
    plt.plot(ejex, ejey, linewidth=2)
##      plt.ylim(ymax = 0.002)      

    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain (' + tituloGrafica + ')')
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
ss = 63288
valuelist =  z[ss:ss+f.cantidadMuestras] #z[0:f.cantidadMuestras] #

titulo= "z"
dataFourierComplex = f.get_complexFFTW(valuelist)      
ejey = f.get_MagnitudeFFT(dataFourierComplex)
ejex = f.getFrequency()
##    indexMaxValue = self.get_PeakFFT(magList, frecuencyList)##    print "Peak at {0}Hz = {1}".format(frecuencyList[indexMaxValue],magList[indexMaxValue])   
f.graficarFourier(ejex, ejey, titulo)


