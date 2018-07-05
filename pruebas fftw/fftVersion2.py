# http://ericstrong.org/fast-fourier-transforms-in-python/
#este funciona, se debe de escoger bien los valores de N, frecu muestreo y demas para poder visualizar una grfica
import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt
from scipy import pi
import math


from grafica import test_fftw

class fourier:

  # Sampling rate in Hz
  frecuenciaMuestreo = 1000.0
  start_time = 0
  end_time = 2
  N = (end_time - start_time)* frecuenciaMuestreo # tamano de los datos

  # Constant time 
  constanteTiempo = 1 / frecuenciaMuestreo # inverse of the sampling rate, sample time
  cantidadMuestras = constanteTiempo * frecuenciaMuestreo # cantidad de datos
  
  # Nyquist Sampling Criteria
  ejeX = np.linspace(0.0, 1.0/(2.0* constanteTiempo), int(N / 2)) # frecuencias
   
  ''' Calcula la aceleracion Rms'''
  def getArms(self, ax, ay, az):
    # para convertir a flotante
    ax = np.asfarray(ax,float) 
    ay = np.asfarray(ay,float) 
    az = np.asfarray(az,float)
    
    return [math.sqrt(math.pow(x,2) +math.pow(y,2) + math.pow(z,2)) for (x, y, z) in zip(ax, ay, az)]   

  # grafica fourier
  def plot_to_Fourier(self, vib_data):
##    plt.ion()
    
##    while (True):
      # FFT algorithm
    fourier = fft(vib_data) # "raw" FFT with both + and - frequencies
    ejeY = 2 / self.cantidadMuestras * np.abs(fourier[0 : np.int(self.N / 2)]) # positive freqs only

    # Plotting the results
##    plt.clf()
    plt.plot(self.ejeX, ejeY)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Vibration (g)')
    plt.title('Frequency Domain (Healthy Machinery)')
    plt.show()

#------------------------------------------------------------       
#             esta parte es para ver si funciona:
#------------------------------------------------------------    
# Frequency domain peaks
peak1_hz = 60 # Hz where the peak occurs
peak1_mag = 25 # magnitude of the peak
peak2_hz = 270 # Hz where the peak occurs
peak2_mag = 2 # magnitude of the peak

# Noise control
noise_loc = 0 # the Gaussian noise is mean-centered
noise_mag = 0.5 # magnitude of added noise

# Vibration data generation
N= 2 * 1000
time = np.linspace(0, 2, N)
vib_data = peak1_mag*np.sin(2*pi*peak1_hz*time) + peak2_mag*np.sin(2*pi*peak2_hz*time) + np.random.normal(0, noise_mag, N) 
peak2_mag2 = 8 # magnitude of the peak
vib_data2 = peak1_mag*np.sin(2*pi*peak1_hz*time) + peak2_mag2*np.sin(2*pi*peak2_hz*time) + np.random.normal(0, noise_mag, N) 


x = vib_data
y = vib_data
z = vib_data2

### Data plotting
##plt.plot(time[0:100], vib_data[0:100])
##plt.xlabel('Time')
##plt.ylabel('Vibration (g)')
##plt.title('Time Domain (Healthy Machinery)')
##plt.show()




# obtener datos del sensor
##datos = test_fftw("sensor1")
##x, y, z = datos.getArrayMediciones()
#alisto los datos para la ventana de hamming
f = fourier()
arms = f.getArms(x, y, z)

# grafico la aceleracion arms
f.plot_to_Fourier(x)
