import numpy as np
import pyfftw
import matplotlib.pyplot as plt
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import math
from grafica import test_fftw
import multiprocessing as mp

class fourier:
  cantidadMuestras = 2**15      # muestras analizadas por fft
  sampleFrec = 1000.0           # Sampling rate
  NyquistFreq = sampleFrec / 2  # Nyquist frequency
  carpetaDireccionSave = ""
  _threads = mp.cpu_count()

  def set_dirSaveData(self, direccion):
    self.carpertaDireccionSave = direccion

  def get_dirSaveData(self):
    return self.carpetaDireccionSave

  def get_complexFFTW(self, dataListVibration):       # Paso 1. Complex Fourier
    aux = pyfftw.pyfftw.zeros_aligned(self.cantidadMuestras,
                             dtype='float64',
                             n=16)
    aux[:] = dataListVibration
    result = pyfftw.interfaces.numpy_fft.fft(aux,
                                             threads = self._threads)
    pyfftw.interfaces.cache.enable()
    return result

  def get_MagnitudeFFT(self, dataFourierComplexList): # Paso 2. Magnitud FFT
    complexList = dataFourierComplexList[0: len(dataFourierComplexList)/2 + 1]
    mag = np.abs(complexList) / float(self.cantidadMuestras)
    mag = mag[0:(self.cantidadMuestras / 2 + 1)]
    mag[0:-2] = 2.0 * mag[0:-2]
    # probar este>
##    mag =  2 / self.cantidadMuestras * np.abs(dataFourierComplexList[0 : np.int(self.cantidadMuestras / 2)]) 
    return mag  
    
  def getFrequency(self):                             # Paso 3. Half of frequency vector 
    return np.linspace(0, self.NyquistFreq, self.cantidadMuestras / 2 + 1)

  def get_PeakFFT(self, dataMagFourierList):  
    peakIndex = 0
    peak = 0
    
##    for loop in range(self.cantidadMuestras/2 +1):
##      if(save):
##        pass
####        FO.write("{0}\t{1}\n".format(frecuencyList[loop], dataMagFourierList[loop])) # 3. guardamos la frecuencia calculada con el fourier
##      if loop>0:
##         if dataMagFourierList[loop] > peak :         # 4. obtenemos el pico maximo 
##           peak = dataMagFourierList[loop]
##           peakIndex = loop
    peakIndex = np.argmax(dataMagFourierList)
    
    return peakIndex
  
  def graficarFourier(self, ejex, ejey, tituloGrafica): # Paso 5. Graficar Fourier    
##    plt.clf()      
    ejex = ejex[150:]
    ejey = ejey[150:]
    index = self.get_PeakFFT(ejey)
    maxValueFourier = ejey[index]
    maxValueFrec = ejex[index]

    index100Hz = (self.cantidadMuestras / 2 + 1) / 2 # 100 hz
    plt.plot(ejex[0: index100Hz], ejey[0: index100Hz], linewidth=0.3)
    plt.grid()
    plt.annotate("{f:0.2f} Hz".format(f=maxValueFrec), xy=(maxValueFrec, maxValueFourier),
                 xycoords='data',
                 xytext=(maxValueFrec+20, maxValueFourier-maxValueFourier*30/1000),
                 #ha='right', va="center",
                 bbox=dict(facecolor='blue', boxstyle="round", alpha=0.1),
                 arrowprops=dict(facecolor='red',arrowstyle="wedge,tail_width=0.3", alpha=0.7)                 
            )
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('% Magnitud (g)')
    plt.title('Frequency Domain (' + tituloGrafica + ')  ')
    plt.show()

# obtener datos del sensor
datos = test_fftw("1")
mediciones = datos.getArrayMediciones()
x = mediciones["x"]
y = mediciones["y"]
z = mediciones["z"]
rms = mediciones["rms"]
t = mediciones["time"]

# Preparamos para Fourier
f = fourier()
ss = 0
valuelist =  x[ss*f.cantidadMuestras: (ss+1)*f.cantidadMuestras] #z[0:f.cantidadMuestras] #

titulo= "x"
dataFourierComplex = f.get_complexFFTW(valuelist)      
ejey = f.get_MagnitudeFFT(dataFourierComplex)
ejex = f.getFrequency()
f.graficarFourier(ejex, ejey, titulo)


