#!/usr/bin/env python
from scipy.fftpack import fft, ifft
##import serial
import matplotlib.pyplot as plt
import numpy as np
import math

### SERIAL
##ser = serial.Serial()
##ser.port = "/dev/ttyACM0"  # may be called something different
##ser.baudrate = 115200  # may be different
##ser.open()

# DATA Nb POINTS
##nb_step = 200
cantidadMuestras = 3200 # Number of samples per second
data = [] * cantidadMuestras

# Sampling rate
fs = 800

# Frequency resolution
frecResolucion = float(fs) / float(cantidadMuestras)

# Nyquist frequency
frecNyquist = fs / 2

# Half of frequency vector
if (cantidadMuestras%2 == 0):
    frequencies = np.linspace(0, frecNyquist, cantidadMuestras/2+1)
else:
    frequencies = np.linspace(0, frecNyquist, (cantidadMuestras+1)/2)

window = np.hamming(cantidadMuestras)

def get_data():
    global data
##    global ser
    global cantidadMuestras
    global window
    data = [] * cantidadMuestras

    #obteniendo los valores de las aceleraciones.
    index = 0
##    while index < cantidadMuestras:
##        response = ser.readline()
##        data.extend(response.splitlines())
##        index = index + 1
##    splited_line = [x.split(',') for x in data]
    ax = 1 #[float(x[0]) for x in splited_line]
    ay = 2 #[float(x[1]) for x in splited_line]
    az = 3 #[float(x[2]) for x in splited_line]

    # calculando el vector de la aceleracion
    a = 4 #[math.sqrt(x ** 2 + y ** 2 + z ** 2) for (x, y, z) in zip(ax, ay, az)]
    
##    ax = np.multiply(ax, window)
##    ay = np.multiply(ay, window)
##    az = np.multiply(az, window)
##    a = np.multiply(a, window)
    return a, ax, ay, az

### MAIN LOOP
### leyendo aceleracion del dispositivo
####if ser.isOpen():
####    print "Port is open!"
##    print "Frequency resolution: ", frecResolucion, " Hz"
####    ser.write("FREQ " + str(fs) )
##
##    '''For the interactive mode, the plot gets updated as you go along.
##    For non-interactive, the plot doesn’t show up until you’ve finished everything.''' 
##    plt.ion()   # Turn interactive mode on
##    while (True):
##        _, _, a, _  = get_data()
##        fourier = fft(a)
##        
##        # extract magnitude and only take half(fft is mirrored)
##        if (cantidadMuestras%2 == 0):
##            Ymag = np.abs(fourier) / float(cantidadMuestras)
##            Ymag = Ymag[0:(cantidadMuestras / 2 + 1)]
##            Ymag[0:-2] = 2.0 * Ymag[0:-2]
##        # Yphase = unwrap(angle(Y(1:N / 2 + 1)))
##        else:
##            Ymag = np.abs(fourier) / float(cantidadMuestras)
##            Ymag = Ymag[0:(cantidadMuestras + 1) / 2] # extrae los "cantidadMuestras" del vector
##            Ymag[1:-2] = 2 * Ymag[1:-2]
##            #Yphase = unwrap(angle(Y(1:(N + 1) / 2)));
##
##        plt.clf()  # Clear Current Figure
##        plt.semilogx(frequencies, Ymag, linewidth=2)
##        axes = plt.gca() # Get Current Axis
##        axes.grid()
##        plt.pause(0.05)
##        plt.show()
##
##ser.close()
