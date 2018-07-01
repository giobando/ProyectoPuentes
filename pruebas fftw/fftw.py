###http://pyfftw.readthedocs.io/en/latest/source/tutorial.html#quick-and-easy-the-pyfftw-interfaces-module
##import pyfftw
##import numpy
##a = pyfftw.empty_aligned(128, dtype='complex128', n=16)
##a[:] = numpy.random.randn(128) + 1j*numpy.random.randn(128)
##b = pyfftw.interfaces.numpy_fft.fft(a)
##c = numpy.fft.fft(a)
##numpy.allclose(b, c)

##https://docs.scipy.org/doc/scipy-0.18.1/reference/tutorial/fftpack.html
##from scipy.fftpack import fft
##N = 600
##T = 1 / 800.0  
##import numpy as np
##x = np.linspace(0.0, N*T, N)
##y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
##yf = fft(y)
####xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
##xf = np.linspace(0.0, 1.0/(T), N/2) # este define el tamano de la ventana FFT
##import matplotlib.pyplot as plt
###para el grafica, claramente debe de ser la misma cantidad de x y en y.
### se dividio el x entre 2 ya que y si se mantiene toda la cantidad se muestra
### repetido la frecuencia.
##plt.plot(xf, 2.0/N * np.abs(yf[0:N/2]))
##plt.grid()
##plt.show()

import numpy as np
from scipy.fftpack import fft, ifft, fftfreq, fftshift
import matplotlib.pyplot as plt

from grafica import test_fftw

##x = np.array([1.0, 2.0, 1.0, -1.0, 1.5])
# obtener una lista
y = test_fftw("sensor1")
y = y.graficarfftw()

N = 32768
T = 1 / 550.0

##x = [1, 2 ,1,-1,1.5]
# calculo de fourier y frecuencia.
yf = fft(y[:N])
xf = fftfreq(N, T) #xf = np.linspace(0.0, 1.0/(2.0*T), N)

# para centrar la lista de frecuencias y fourier
xf = fftshift(xf)
yplot = fftshift(yf)


#plt.plot(xf, 2.0/N * y[0:N])
plt.plot(xf, 2.0/N * np.abs(yf[0:N]))
plt.grid()
plt.show()

##yinv = ifft(y)
##yinv
##array([ 1.0+0.j,  2.0+0.j,  1.0+0.j, -1.0+0.j,  1.5+0.j])
