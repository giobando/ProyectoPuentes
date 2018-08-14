import numpy as np
import pyfftw
import matplotlib.pyplot as plt
#from scipy.fftpack import fft, ifft, fftfreq, fftshift
#from grafica import test_fftw
import multiprocessing as mp
from datosAlmacen.sd_card import sd_card
from constantes.const import DIRECC_TO_SAVE
from constantes.const import NUM_SAMPLES_TO_FOURIER

class fourier:
    cantidadMuestras = NUM_SAMPLES_TO_FOURIER      # muestras analizadas por fft
    sampleFrec = 1000.0           # Sampling rate
    NyquistFreq = sampleFrec / 2  # Nyquist frequency

    _threads = mp.cpu_count()
    sensorName = ""
    testName = ""
    spectrumFile = ""  # archivo para guardar la frecuencia y fourier
    peakFile = ""

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

        # Creando archivo de picos de frecuencia
        self.peakFile = carpetaNueva + "/"
        self.peakFile += "sensor_" + self.sensorName + "_Peaks.csv"
        saveMuestra = sd_card(self.peakFile)
        txt = "FrecuenciaX(Hz);%Magnitud_X(g);"
        txt += "FrecuenciaY(Hz);%Magnitud_Y(g);"
        txt += "FrecuenciaZ(Hz);%Magnitud_Z(g);"
        txt += "FrecuenciaRMS(Hz);%Magnitud_RMS(g)\n"
        saveMuestra.escribir(txt)

    ''' Almacena los spectrum en un csv. '''
    def saveSpectrumCSV(self, frequencyDataList, fourierDataList_x,
                        fourierDataList_y, fourierDataList_z,
                        fourierDataList_rms):
        # Calcula y Almacena los picos maximos
        indexX = self.get_PeakFFT(fourierDataList_x)
        indexY = self.get_PeakFFT(fourierDataList_y)
        indexZ = self.get_PeakFFT(fourierDataList_z)
        indexRMS = self.get_PeakFFT(fourierDataList_rms)

        diccX = {"x": frequencyDataList[indexX],
                 "y": fourierDataList_x[indexX]}
        diccY = {"x": frequencyDataList[indexY],
                 "y": fourierDataList_y[indexY]}
        diccZ = {"x": frequencyDataList[indexZ],
                 "y": fourierDataList_z[indexZ]}
        diccRMS = {"x": frequencyDataList[indexRMS],
                   "y": fourierDataList_rms[indexRMS]}
        self.savePeakCSV(diccX, diccY, diccZ, diccRMS)

        # Almacena todos los datos calculados de fourier
        saveMuestra = sd_card(self.spectrumFile)
        for line in range(len(fourierDataList_x)):
            lineTxt = str(frequencyDataList[line]) + ";"
            lineTxt += str(fourierDataList_x[line]) + ";"
            lineTxt += str(fourierDataList_y[line]) + ";"
            lineTxt += str(fourierDataList_z[line]) + ";"
            lineTxt += str(fourierDataList_rms[line]) + "\n"
            saveMuestra.escribir(lineTxt)

    ''' Almacena los picos mas altos de cada spectrum en un csv. '''
    def savePeakCSV(self, diccX, diccY, diccZ, diccRMS):
        saveMuestra = sd_card(self.peakFile)
        lineTxt = str(diccX["x"]) + ";" + str(diccX["y"]) + ";"
        lineTxt += str(diccY["x"]) + ";" + str(diccY["y"]) + ";"
        lineTxt += str(diccZ["x"]) + ";" + str(diccZ["y"]) + ";"
        lineTxt += str(diccRMS["x"]) + ";" + str(diccRMS["y"]) + "\n"

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
        mag = np.abs(complexList) / float(self.cantidadMuestras)
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
                             arrowprops=dict(facecolor='red',
                                             arrowstyle="wedge,tail_width=0.3",
                                             alpha=0.7))
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('% Magnitud (g)')
        plt.title('Frequency Domain (' + tituloGrafica + ')  sin hamming')
        plt.show()

# PARA CORRER!!!!!!!!
# obtener datos del sensor

# Preparamos para Fourier
#f = fourier()
#ss = 1
#valuelist =  z[ss*f.cantidadMuestras: (ss+1)*f.cantidadMuestras]
#
#titulo= "z"
#dataFourierComplex = f.get_complexFFTW(valuelist)
#ejey = f.get_MagnitudeFFT(dataFourierComplex)
#ejex = f.getFrequency()
#f.graficarFourier(ejex, ejey, titulo)
