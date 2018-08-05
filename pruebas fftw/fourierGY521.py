import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
import math

from grafica import test_fftw

class fourier:
  cantidadMuestras =16384      # muestras analizadas por fft
  window = np.hamming(cantidadMuestras)
  sampleFrec = 150                    # Sampling rate
  resolutionFreq = float(sampleFrec) / float(cantidadMuestras) # Frequency resolution
  NyquistFreq = sampleFrec / 2        # Nyquist frequency

  carpetaDireccionSave = ""

  def set_dirSaveData(self, direccion):
    self.carpertaDireccionSave = direccion

  def get_dirSaveData(self):
    return self.carpetaDireccionSave
     
  ''' recibe: list de vibraciones float obtenidas del sensor
      retorna: arrays para el grafico '''
  def getData_to_HammingW(self, vibrationList):       # Paso 1. Se obtiene dato con hamming data    
##    dataList = vibrationList[0:self.cantidadMuestras]    
    dataList = np.asfarray(vibrationList, float)      # String -> flotante    
    dataList = np.multiply(dataList, self.window)     # Valores Hamming windows
    return dataList

  def get_MagnitudeFFT(self, dataFourierComplexList): # Paso 2. Calcular Magnitud FFT
    if (self.cantidadMuestras % 2 == 0):
      mag = np.abs(dataFourierComplexList) / float(self.cantidadMuestras)
      mag = mag[0:(self.cantidadMuestras / 2 + 1)]
      mag[0:-2] = 2.0 * mag[0:-2]
      #phase = unwrap(angle(Y(1:N / 2 + 1)))
      return mag      
    else:
      mag = np.abs(dataFourierComplexList) / float(self.cantidadMuestras)
      mag = mag[0:(self.cantidadMuestras + 1) / 2]
      mag[1:-2] = 2 * mag[1:-2]
      #phase = unwrap(angle(Y(1:(N + 1) / 2)));
      return mag
    
  def getFrequency(self):                             # Paso 3. Half of frequency vector 
    if (self.cantidadMuestras % 2 == 0):
        return np.linspace(0, self.NyquistFreq, self.cantidadMuestras / 2 + 1)
    else:
        return np.linspace(0, self.NyquistFreq, (self.cantidadMuestras + 1) / 2)

  def get_PeakFFT(self, dataMagFourierList, frecuencyList, save=True):          # retorna el index del mayor dato
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
  
  def graficarFourier(self, hammingDataList, tituloGrafica):      # Paso 4. Graficar Fourier
    plt.ion()

    dataFourierComplex = fft(hammingDataList, self.cantidadMuestras)      
    magList = self.get_MagnitudeFFT(dataFourierComplex)
    frecuencyList = self.getFrequency()      
##    indexMaxValue = self.get_PeakFFT(magList, frecuencyList)##    print "Peak at {0}Hz = {1}".format(frecuencyList[indexMaxValue],magList[indexMaxValue])
    plt.clf()      
    plt.plot(frecuencyList[2:], magList[2:], linewidth=2)
##      plt.ylim(ymax = 0.002)
      
    axes = plt.gca()
    axes.grid()
    plt.pause(2) # seconds
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain (' + tituloGrafica + ') w/Hamming')
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
eje = y
valuelist = f.getData_to_HammingW(eje[0:f.cantidadMuestras])
print("listo")
# grafico la aceleracion arms
titulo= "arms"
f.graficarFourier(valuelist, titulo)


