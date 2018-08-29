# -*- coding: utf-8 -*-

from datosAlmacen.sd_card import sd_card
from constantes.const import DIRECC_TO_SAVE
from constantes.const import NUM_SAMPLES_TO_FOURIER
import numpy as np
import pyfftw
import matplotlib.pyplot as plt
import multiprocessing as mp

'''
Calcula fourier y almacena en csv
No es capaz de visualizar las graficas, sin embargo la funcion para
hacerlo esta programada
'''


class fourier:
    cantidadMuestras = NUM_SAMPLES_TO_FOURIER   # muestras analizadas por fft
    sampleFrec = 1000.0           # Sampling rate
    NyquistFreq = sampleFrec / 2  # Nyquist frequency

    _threads = mp.cpu_count()
    sensorName = ""
    testName = ""
    spectrumFile = ""  # archivo para guardar la frecuencia y fourier
    peakFile = ""
    direc = DIRECC_TO_SAVE

    def __init__(self, sensorName, testName):
        self.sensorName = sensorName
        self.testName = testName

        # creando carpeta y archivo para almacenar datos
        self.crearArchivo()

    def crearArchivo(self):
        # creando carpeta para almacenar archivo
        saveMuestra = sd_card('')
        carpetaNueva = DIRECC_TO_SAVE + self.testName + "/Espectros"
        saveMuestra.crearCarpeta(carpetaNueva)

        # Creando archivo de spectrum
        self.spectrumFile = carpetaNueva + "/"
        self.spectrumFile += "sensor_" + self.sensorName + "_Frecuencias.csv"
        saveMuestra = sd_card(self.spectrumFile)
        txt = "Frecuencia(Hz);%Magnitud_X(g)"
        txt += ";%Magnitud_Y(g);%Magnitud_Z(g);%Magnitud_RMS(g)\n"
        saveMuestra.escribir(txt)

    ''' Almacena los spectrum en un csv. '''
    def saveSpectrumCSV(self, frequencyDataList, fourierDataList_x,
                        fourierDataList_y, fourierDataList_z,
                        fourierDataList_rms):

        # Almacena todos los datos calculados de fourier
        saveMuestra = sd_card(self.spectrumFile)
        for line in range(len(fourierDataList_x)):
            lineTxt = str(frequencyDataList[line]) + ";"
            lineTxt += str(fourierDataList_x[line]) + ";"
            lineTxt += str(fourierDataList_y[line]) + ";"
            lineTxt += str(fourierDataList_z[line]) + ";"
            lineTxt += str(fourierDataList_rms[line]) + "\n"
            saveMuestra.escribir(lineTxt)

    # Paso 1. Complex Fourier
    def get_complexFFTW(self, dataListVibration):
        aux = pyfftw.pyfftw.zeros_aligned(self.cantidadMuestras,
                                          dtype='float64',
                                          n=16)
        aux[:] = dataListVibration
        result = pyfftw.interfaces.numpy_fft.fft(aux,
                                                 threads=self._threads)
        pyfftw.interfaces.cache.enable()
        return result

    # Paso 2. Magnitud FFT
    def get_MagnitudeFFT(self, dataFourierComplexList):
        cantidad = len(dataFourierComplexList)
        complexList = dataFourierComplexList[0: cantidad / 2 + 1]

        mag = np.abs(complexList)
        maxIndex = self.get_PeakFFT(mag)

        mag = mag / mag[maxIndex]
        mag = mag[0:(self.cantidadMuestras / 2 + 1)]
        mag[0:-2] = 2.0 * mag[0:-2]
        # probar este>
    ##    mag =  2 / self.cantidadMuestras * np.abs(dataFourierComplexList[0 : np.int(self.cantidadMuestras / 2)])
        return mag

    # Paso 3. Half of frequency vector
    def getFrequency(self):
        return np.linspace(0, self.NyquistFreq, self.cantidadMuestras / 2 + 1)

    def get_PeakFFT(self, dataMagFourierList):
        peakIndex = 0
        peakIndex = np.argmax(dataMagFourierList)
        return peakIndex

    # Paso 5. Graficar Fourier
    def graficarFourier(self, ejex, ejey, tituloGrafica):
        ejex = ejex[150:]
        ejey = ejey[150:]
        index = self.get_PeakFFT(ejey)
        maxValueFourier = ejey[index]
        maxValueFrec = ejex[index]

        index100Hz = (self.cantidadMuestras / 2 + 1) / 4  # 100 hz
        plt.plot(ejex[0: index100Hz], ejey[0: index100Hz], linewidth=0.3)
        plt.grid()
        plt.annotate("{f:0.2f} Hz".format(f=maxValueFrec),
                     xy=(maxValueFrec, maxValueFourier), xycoords='data',
                     xytext=(maxValueFrec+20,
                             maxValueFourier-maxValueFourier*30/1000),
                             bbox=dict(facecolor='blue',
                                       boxstyle="round",
                                       alpha=0.1),
                             arrowprops=dict(facecolor = 'red',
                                             arrowstyle="wedge,tail_width=0.3",
                                             alpha=0.7))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('% Magnitud (g)')
        plt.title('Frequency Domain (' + tituloGrafica + ')  sin hamming')
        plt.show()


# Preparamos para Fourier
#def getArrayMediciones(arch_acc):
#    try:
#        arch = open(arch_acc, 'r')
#        graph_data = arch.read()
#        lines = graph_data.split('\n')
#        arch.close()
#        ejeXs = []
#        ejeYs = []
#        ejeZs = []
#        ejeRMS = []
#        ejefrec = []
#
#        for line in lines:  # archivo para guardar una variable
#            if len(line) > 1:
#                frec, x, y, z, rms = line.split(';')
#                ejeXs.append(x)
#                ejeYs.append(y)
#                ejeZs.append(z)
#                ejefrec.append(frec)
#                ejeRMS.append(rms)
#        return {"x": ejeXs, "y": ejeYs, "z": ejeZs, "rms": ejeRMS, "frec": ejefrec}
#    except IOError:
#        print("error!!", IOError)
#
#
#def get_PeakFFT(dataMagFourierList):
#        peakIndex = 0
#        dataMagFourierList = list(np.float_(dataMagFourierList))
#        peakIndex = np.argmax(dataMagFourierList)
#        return peakIndex
#
#def graficarFourier(ejex, ejey, tituloGrafica, numGrafica):
#        index = get_PeakFFT(ejey)
#        maxValueFourier = ejey[index]
#        maxValueFrec = ejex[index]
#
#        fig = plt.figure()
#        plt.plot(ejex, ejey, linewidth=0.3)
#        plt.grid()
#        labelY = "{:.5f}".format(float(maxValueFourier))
#        labelX = "{:.1f}".format(float(maxValueFrec))
#        label = "("+labelX+", "+labelY+")"
#        maxValueFourier = float(maxValueFourier)
#
#        plt.annotate(label,
#                     xy=(maxValueFrec, maxValueFourier), xycoords='data',
#                     xytext=(float(labelX)+50 , maxValueFourier-maxValueFourier*30/1000), # (x,y)
#                             bbox=dict(facecolor='blue', boxstyle="round", alpha=0.1),
#                             arrowprops=dict(facecolor='red',
#                                             arrowstyle="wedge,tail_width=0.3",
#                                             alpha=0.7))
#        plt.xlabel('Frequency (Hz)')
#        plt.ylabel('% Magnitud (g)')
#        plt.title('Frequency Domain (' + tituloGrafica + ') MPU,'+numGrafica)
#        imagenName = tituloGrafica+'_'+numGrafica+'.jpg'
#        fig.savefig(imagenName)
#
#
#testName = "16agostoSinIman"
#nombreSensor = "1"
#dire = "../AlmacenPruebas/"
#x = dire + testName + "/Espectros/"
#arch_acc = x+"sensor_"+nombreSensor + "_Frecuencias.csv"
#
#muestras = 16385
#
#index = 0
#
#while(index < 5):
#    mediciones = getArrayMediciones(arch_acc)
#    ejeY = mediciones["x"]
#    ejeX = mediciones["frec"]
#    inicio = 1 + index*muestras
#    fin = (index + 1)*muestras
#    ejeY = ejeY[inicio: fin]
#    ejeX = ejeX[inicio: fin]
#
#    titulo = "x"
#    numGrafica = str(index)
#    graficarFourier(ejeX, ejeY, titulo, numGrafica)
#    index += 1
