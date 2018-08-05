# -*- coding: utf-8 -*-
#!/usr/bin/python

import math
import time
import numpy

class transformadaFourier:
    TargetSampleNumber= 32768   # Cantidad muestras para calcular fourier
    TargetRate= 45.0            # Frecuencia Muestreo
    carpetaDir = ""

    def __init__(self,FrecMuestreo, numeroMuestrasFFT, saveDireccion):
        self.TargetRate = FrecMuestreo
        self.TargetSampleNumber = numeroMuestrasFFT
        self.carpetaDir = saveDireccion

    def calcularFourier(self, datalist):
        # 1. Complejo de fourier
        fourier = numpy.fft.fft(datalist)

        # Para guardar:
        print "Save FFTData.txt file"
        archivo = open("FFTData.txt","w")

        # 2. magnitud
        fftData = numpy.abs(fourier[0:len(fourier)/2+1])/self.TargetSampleNumber

        # 3. frecuencia
        frequency = []
#        archivo.write("Frequency\tFFT\n")

        # 4. magnitud maxima de vibracion
        Peak=0
        PeakIndex=0;

        for
        loop in range(self.TargetSampleNumber/2 +1):
            # 3.1 Frecuencias
            frequency.append( loop * self.TargetRate/ self.TargetSampleNumber)

            # 5. guardamos
            archivo.write("{0},{1}\n".format(frequency[loop],fftData[loop]))
            if loop>0:
                if fftData[loop] > Peak :      # 4. obtenemos el pico maximo
                    Peak=fftData[loop]
                    PeakIndex=loop
        print "Peak at {0}Hz = {1}".format(frequency[PeakIndex],Peak)

    # grafica con cada grupo de datos calculado
    def graficarFourier(self):
        pass


#    def __init__(self):
