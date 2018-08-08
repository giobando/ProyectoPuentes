# -*- coding: utf-8 -*-
import numpy as np
import pyfftw
import matplotlib.pyplot as plt
from grafica import test_fftw
from scipy.fftpack import fft, ifft, fftfreq, fftshift
from datosAlmacen.sd_card import sd_card

class fourier:
    cantidadMuestras = 16384      # muestras analizadas por fft
    sampleFrec = 150              # Sampling rate
    NyquistFreq = sampleFrec / 2  # Nyquist frequency
    carpetaDireccionSave = ""
    _threads = 4
    sensorName = ""
    testName = ""

    def __init__(self, sensorName, testName):
        self.sensorName = sensorName
        self.testName = testName

    '''
    Encargado de almacenar cada muestra en un txt.
    Recibe
        + aceleracion en cada eje
        + aceleraciron RMS calculado
        + Tiempo que se toma la muestra
        + medida del giroscopio
        + inclinacion de la aceleracion   '''
    def saveTXT(self, frequencyData, fourierData):
        # creando carpeta
        saveMuestra = sd_card(self.sensorName)
        carpetaNueva = self.nameTest
        direcCarpeta = "../Analisis_Puentes_Software/AlmacenPruebas/"
        saveMuestra.crearCarpeta(direcCarpeta + carpetaNueva)

        # Creando archivo
        arch_Acc = direcCarpeta + self.nameTest + "/" + "sensor_"+self.sensorName + "_Frecuencias.txt"
        saveMuestra = sd_card(arch_Acc)

        # guardando aceleraciones en txt
        lineTxt = ""
        lineTxt = str(frequencyData) + "," + str(fourierData) + "\n"
        saveMuestra.escribir(lineTxt)
        saveMuestra.cerrar()

    def set_dirSaveData(self, direccion):
        self.carpertaDireccionSave = direccion

    def get_dirSaveData(self):
        return self.carpetaDireccionSave

    # Paso 1. Complex Fourier
    def get_complexFFTW(self, dataListVibration):
#        aux = pyfftw.empty_aligned(self.cantidadMuestras, dtype='float64')
#        dataListFourier = pyfftw.builders.fft(aux,
#                                              planner_effort='FFTW_MEASURE',
#                                              threads=self._threads)
#        return dataListFourier()
        dataListFourier = fft(dataListVibration)
        return dataListFourier

    # Paso 2. Magnitud FFT
    def get_MagnitudeFFT(self, dataFourierComplexList):
        mag = np.abs(dataFourierComplexList) / float(self.cantidadMuestras)
        mag = mag[0:(self.cantidadMuestras / 2 + 1)]
        mag[0:-2] = 2.0 * mag[0:-2]
#        probar este>
#        mag = np.abs(dataFourierComplexList[0:np.int(self.cantidadMuestras/2)])
#        mag = 2 / self.cantidadMuestras * mag
        return mag

    # Paso 3. Half of frequency vector
    def getFrequency(self):
        return np.linspace(0, self.NyquistFreq, self.cantidadMuestras / 2 + 1)

    def get_PeakFFT(self, dataMagFourierList, frecuencyList, save=True):
        peakIndex = 0
        peak = 0

        for loop in range(self.cantidadMuestras / 2 + 1):
            if(save):
                pass
                # 3. guardamos la frecuencia calculada con el fourier
#                FO.write("{0}\t{1}\n".format(frecuencyList[loop],
#                         dataMagFourierList[loop]))

            if loop > 0:
                if dataMagFourierList[loop] > peak: # 4. Pico maximo
                    peak = dataMagFourierList[loop]
                    peakIndex = loop
        return peakIndex

    # Paso 5. Graficar Fourier
    def graficarFourier(self, ejeX, ejeY, tituloGrafica):
#        plt.clf()
        plt.plot(ejex, ejey, linewidth=2)
#        plt.ylim(ymax = 0.002)

        axes.grid()
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Vibration (g)')
        plt.title('Frequency Domain (' + tituloGrafica + ')')
        plt.show()


#
## obtener datos del sensor
#datos = test_fftw("sensor1")
#mediciones = datos.getArrayMediciones()
#x = mediciones["x"]
#y = mediciones["y"]
#z = mediciones["z"]
#rms = mediciones["rms"]
#t = mediciones["time"]
#
## Preparamos para Fourier
#f = fourier()
#eje = y
#valuelist = eje[0:f.cantidadMuestras]
#
#titulo= "y"
#dataFourierComplex = f.get_complexFFTW(valuelist)
#ejey = f.get_MagnitudeFFT(dataFourierComplex)
#ejex = f.getFrequency()
###    indexMaxValue = self.get_PeakFFT(magList, frecuencyList)##    print "Peak at {0}Hz = {1}".format(frecuencyList[indexMaxValue],magList[indexMaxValue])
#f.graficarFourier(ejex, ejey, titulo)


