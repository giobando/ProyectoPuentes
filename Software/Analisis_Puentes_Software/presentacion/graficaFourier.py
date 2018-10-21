# -*- coding: utf-8 -*-
# http://ericstrong.org/fast-fourier-transforms-in-python/
#este funciona, se debe de escoger bien los valores de N, frecu muestreo y demas para poder visualizar una grfica
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
from scipy import pi
import math


from grafica import test_fftw

class graficarFourier:
  dataFiles = None

  # Sampling rate in Hz
  frecuenciaMuestreo = 1000.0
  start_time = 0
  end_time = 2

  # este siempre debe de ir en flotante y debe ser igual a la cantidad de muestras
  # a anaizar, preferiblemente potencia de dos
  N = 8192.0  #(end_time - start_time)* frecuenciaMuestreo # tamano de los datos

  # Constant time
  constanteTiempo = 1 / frecuenciaMuestreo # inverse of the sampling rate, sample time
  cantidadMuestras = constanteTiempo * frecuenciaMuestreo # cantidad de datos

  # Nyquist Sampling Criteria
  ejeX = np.linspace(0.0, 1.0/(2.0* constanteTiempo), int(N / 2)) # frecuencias

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
      return ejeXs,ejeYs,ejeZs, ejeAccRms, ejeTime

    except IOError:
      print("error", IOError)

  # grafica fourier
  def plot_to_Fourier(self, vib_data):
    # FFT algorithm
    data_fourier = fft(vib_data) # "raw" FFT with both + and - frequencies
    ejeY = 2 / self.N * np.abs(data_fourier[0 : np.int(self.N / 2)]) # positive freqs only

    # Plotting the results
    plt.plot(self.ejeX, ejeY)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain')
    plt.show()

#------------------------------------------------------------
#             esta parte es para ver si funciona:
#------------------------------------------------------------
# Frequency domain peaks
#peak1_hz = 60 # Hz where the peak occurs
#peak1_mag = 25 # magnitude of the peak
#peak2_hz = 270 # Hz where the peak occurs
#peak2_mag = 2 # magnitude of the peak
#
## Noise control
#noise_loc = 0 # the Gaussian noise is mean-centered
#noise_mag = 0.5 # magnitude of added noise
#
## Vibration data generation
#N= 2 * 1000
#time = np.linspace(0, 2, N)
#vib_data = peak1_mag*np.sin(2*pi*peak1_hz*time) + peak2_mag*np.sin(2*pi*peak2_hz*time) + np.random.normal(0, noise_mag, N)
#peak2_mag2 = 8 # magnitude of the peak
#vib_data2 = peak1_mag*np.sin(2*pi*peak1_hz*time) + peak2_mag2*np.sin(2*pi*peak2_hz*time) + np.random.normal(0, noise_mag, N)
#
#
#x = vib_data
#y = vib_data
#z = vib_data2

### Data plotting
##plt.plot(time[0:100], vib_data[0:100])
##plt.xlabel('Time')
##plt.ylabel('Vibration (g)')
##plt.title('Time Domain (Healthy Machinery)')
##plt.show()




# obtener datos del sensor
#f = graficarFourier("sensor1")
#x,y,z,accrms,t = f.getArrayMediciones()
#
#
## grafico la aceleracion arms
#f.plot_to_Fourier(z)

