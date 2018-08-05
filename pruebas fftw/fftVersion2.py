# http://ericstrong.org/fast-fourier-transforms-in-python/
#este funciona, se debe de escoger bien los valores de N, frecu muestreo y demas para poder visualizar una grfica
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
from scipy import pi
import math

from grafica import test_fftw

class fourier:
  dataFiles = None

  # Sampling rate in Hz
  frecuenciaMuestreo = 150.0
  start_time = 0
  end_time = 2

  # este siempre debe de ir en flotante y debe ser igual a la cantidad de muestras
  # a anaizar, preferiblemente potencia de dos
  N = 16384.0  #(end_time - start_time)* frecuenciaMuestreo # tamano de los datos

  # Constant time
  constanteTiempo = 1 / frecuenciaMuestreo # inverse of the sampling rate, sample time
  cantidadMuestras = constanteTiempo * frecuenciaMuestreo # cantidad de datos

  # Nyquist Sampling Criteria
  ejeX = np.linspace(0.0, 1.0/(2.0* constanteTiempo), int(N / 2)) # frecuencias

  fig = plt.figure()
  grafica = fig.add_subplot(111)

  def __init__(self,nombreSensor):
    arch_acc = nombreSensor + "_Aceleracion.txt"
    self.dataFiles = arch_acc

  def getArrayMediciones(self):
    try:
      arch = open(self.dataFiles, 'r')
      graph_data = arch.read()
      lines = graph_data.split('\n')
      arch.close()
      ejeXs = []
      ejeYs = []
      ejeZs = []
      ejeAccRms = []
      ejeTime = []

      #archivo para guardar una variable
      for line in lines:
        if len(line) > 1:
          x, y, z, accRms, t = line.split(',')
          ejeXs.append(x)
          ejeYs.append(y)
          ejeZs.append(z)
          ejeAccRms.append(accRms)
          ejeTime.append(t)

      return {"x":ejeXs, "y":ejeYs, "z":ejeZs, "rms":ejeAccRms, "time":ejeTime}

    except IOError:
      print("error", IOError)

  # grafica fourier
  def plot_to_Fourier(self, vib_data, titulo):
    # FFT algorithm
    data_fourier = fft(vib_data) # "raw" FFT with both + and - frequencies
    ejeY = 2 / self.N * np.abs(data_fourier[0 : np.int(self.N / 2)]) # positive freqs only

    # Plotting the results
    plt.plot(self.ejeX[1:], ejeY[1:])
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain ('+titulo+') \n (without Hamming windows)')
    plt.show()

# obtener datos del sensor
f = fourier("sensor1")
mediciones = f.getArrayMediciones()

ejeGraficarTitle = "y" #rms, x,y, z
ejeGraficar = mediciones[ejeGraficarTitle]

# grafico la aceleracion arms
f.plot_to_Fourier(ejeGraficar[0:int(f.N)], ejeGraficarTitle)
