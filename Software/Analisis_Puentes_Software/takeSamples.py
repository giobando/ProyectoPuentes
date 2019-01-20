# -*- coding: utf-8 -*-
from datosAlmacen.sd_card import sd_card
from dispositivo.gestorSensor import gestorSensor
from herramientas.transformadaFourier import fourier

# CONSTANTES
from constantes.const import ZERO_EJE_Z
from constantes.const import ACCE_MINIMA
from constantes.const import DIRECC_TO_SAVE

from constantes.const import NAME_SENSOR_PORT1
from constantes.const import NAME_SENSOR_PORT2

from constantes.const import NUMBER_PORTSENSOR1
from constantes.const import NUMBER_PORTSENSOR2
from constantes.const import NAME_NODE
from constantes.const import ADDRESS_REG_accA as PORT1
from constantes.const import ADDRESS_REG_accB as PORT2
from constantes.const import NUM_SAMPLES_TO_FOURIER
from constantes.const import CALIBRATED
from constantes.const import oldSensibilidad

import math
import time
import smbus

import threading


class test:

    sensorObject = None
    nameTest = None
    temperatura = -1
    duration = -1       # if -1: continue time.
    gUnits = True       # it is indicate "g" units
    frecuencia = None
    aceleracionMinima = 0

    arch_Acc = ""       # ARchivo para guardarfz Aceleraciones
    arch_Gyro = ""      # ARchivo para guardar gyroscopio

    spectrum = None


    def setNameTest(self, nameTest):
        self.nameTest = nameTest

    def setSensorObject(self, sensorObject):
        self.sensorObject = sensorObject

    def setDuration(self, duration):
        self.duration = duration

    def setFrec(self, frec):
        self.frecuencia = frec

    def setgUnits(self, gUnits):
        self.gUnits = gUnits

    '''
    Recibe:
        + nameTest: nombre de la prueba
        + sensorObject: Objecto mpu6050
        + duration: tiempo en segundos
        + gUnits: True: para unidades en g, False: para unidades en m/s2 '''
    def __init__(self):
        # definicion del valor minimo depende de las unidades
        self.defineMinValue_to_aceleration()

#        # creando carpeta para almacenar datos
#        saveMuestra = sd_card('')
#        carpetaNueva = self.nameTest
#        saveMuestra.crearCarpeta(DIRECC_TO_SAVE + carpetaNueva)
#
#        # Creando Archivos para los datos
#        self.arch_Acc = DIRECC_TO_SAVE + self.nameTest + "/"
#        self.arch_Acc += "nodo_" + str(NAME_NODE)
#        self.arch_Acc += "-sensor_" + self.sensorObject.sensorName
#        self.arch_Acc +=  "_Aceleracion.csv"
#        self.arch_Gyro = DIRECC_TO_SAVE + self.nameTest + "/"
#        self.arch_Gyro += "nodo_" + str(NAME_NODE)
#        self.arch_Gyro += "-sensor_" + self.sensorObject.sensorName + "_Gyro.csv"


    def defineMinValue_to_aceleration(self):
        if(ZERO_EJE_Z and self.gUnits):
            self.aceleracionMinima = ACCE_MINIMA
        elif (ZERO_EJE_Z and not self.gUnits):
            self.aceleracionMinima = ACCE_MINIMA
        elif(not ZERO_EJE_Z and self.gUnits):  # i.e cercano a 1g
            self.aceleracionMinima = ACCE_MINIMA + 1
        elif (not ZERO_EJE_Z and not self.gUnits):
            self.aceleracionMinima = ACCE_MINIMA * 9.8 + 9.8

    '''Calcula el vector aceleracion.
        Recibe:
            + Aceleracion de los 3 ejes, No importa en que unidades este.'''
    def calc_Acc_RMS(self, ax, ay, az):
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    def get_unitAcc(self):
        if(self.gUnits):
            return "g"
        else:
            return "m/s"

    "Crea archivos con encabezados para aceleracion y gyroscopio"
    def crearArchivos(self):
        # creando carpeta para almacenar datos
        saveMuestra = sd_card('')
        carpetaNueva = self.nameTest
        saveMuestra.crearCarpeta(DIRECC_TO_SAVE + carpetaNueva)

        # Creando Archivos para los datos
        self.arch_Acc = DIRECC_TO_SAVE + self.nameTest + "/"
        self.arch_Acc += "nodo_" + str(NAME_NODE)
        self.arch_Acc += "-sensor_" + self.sensorObject.sensorName
        self.arch_Acc +=  "_Aceleracion.csv"
        self.arch_Gyro = DIRECC_TO_SAVE + self.nameTest + "/"
        self.arch_Gyro += "nodo_" + str(NAME_NODE)
        self.arch_Gyro += "-sensor_" + self.sensorObject.sensorName + "_Gyro.csv"

        accUnits = self.get_unitAcc()
        saveMuestra = sd_card(self.arch_Acc)
        txt = "ax("+accUnits+");ay("+accUnits+");az("+accUnits+");"
        txt += "accRMS(" + accUnits + ");time(s)\n"
        saveMuestra.escribir(txt)

        saveMuestra = sd_card(self.arch_Gyro)
        txt = "gx(degree/s);gy(degree/s);gz(degree/s);inclinacionX;"
        txt += "inclinacionY;time(s)\n"
        saveMuestra.escribir(txt)

    '''Encargado de las muestras, recibe:
        + frec: frecuencia de muestreo en Hz (limite max 1000Hz, mas de esto no
          es posible a menos que se use FIFO que proporciona el sensor)'''
    def calcularFourier(self, xList, yList, zList, rmsList, contadorEspectros):
        # Complex Number fourier
        x = self.spectrum.get_complexFFTW(xList)
        y = self.spectrum.get_complexFFTW(yList)
        z = self.spectrum.get_complexFFTW(zList)
        rms = self.spectrum.get_complexFFTW(rmsList)

        # Magnitud number fourier
        magx = self.spectrum.get_MagnitudeFFT(x)
        magy = self.spectrum.get_MagnitudeFFT(y)
        magz = self.spectrum.get_MagnitudeFFT(z)
        magrms = self.spectrum.get_MagnitudeFFT(rms)
        frec = self.spectrum.getFrequency()

        self.spectrum.crearArchivoEspectro(contadorEspectros)
        self.spectrum.saveSpectrumCSV(frec, magx, magy, magz, magrms)
#        fourier.graficarFourier(frec, x, "ejeX")

    def makeTest(self, save=False):
        countSamples = 0
        self.crearArchivos()
        self.spectrum = fourier(self.sensorObject.sensorName, self.nameTest)
        contadorEspectros = 0
        rmsOld = 0  # para comparar y no guardar datos repetidos.
        start = time.time()
        finalTime = 0

        while(finalTime < self.duration or self.duration == -1):
            sampleACC = self.sampleAceleracion(finalTime)
            rmsSample = sampleACC['rms']  # gyro=self.sampleGyro(finalTime,save)

            if(rmsSample >= self.aceleracionMinima or self.duration > 0):
                # Inicia guardar los datos
                numSampleToFourier = 0
                sampleToFourierX = []
                sampleToFourierY = []
                sampleToFourierZ = []
                sampleToFourierRMS = []

                if(self.duration == -1):
                    self.sensorObject.set_frecMuestreoAcc(1000)
                    self.frecuencia = 1000

                while(numSampleToFourier < NUM_SAMPLES_TO_FOURIER and
                      finalTime <= self.duration):
                    sampleACC = self.sampleAceleracion(finalTime)
                    rmsSample = sampleACC['rms']

                    if(rmsOld != rmsSample):
                        # Para evitar valores repetidos, se compara con el anterior.
                        self.saveSampleACC(sampleACC["x"], sampleACC["y"],
                                           sampleACC["z"], rmsSample,
                                           sampleACC["time"])
                        rmsOld = rmsSample
                        sampleToFourierX.append(sampleACC["x"])
                        sampleToFourierY.append(sampleACC["y"])
                        sampleToFourierZ.append(sampleACC["z"])
                        sampleToFourierRMS.append(sampleACC["rms"])

                        numSampleToFourier += 1
                    finalTime = time.time() - start

                # Calculando Fourier EN PARALELO
                if(numSampleToFourier == NUM_SAMPLES_TO_FOURIER):
                    hiloFourier = threading.Thread(target= self.calcularFourier,
                                             args=(sampleToFourierX,
                                                   sampleToFourierY,
                                                   sampleToFourierZ,
                                                   sampleToFourierRMS,
                                                   contadorEspectros,)
                                             )
                    hiloFourier.start()
                    contadorEspectros += 1

                # reconfiguramos la frecuencia.
                if(self.duration == -1):
                    self.sensorObject.set_frecMuestreoAcc(self.frecuencia)
                countSamples += numSampleToFourier
#                else:
#                    countSamples += 1

            finalTime = time.time() - start
        print("Muestra finalizada, num de muestras total fue:", countSamples)

    ''' Toma una muestra y almacenarla en un txt, Recibe:
        + numMuestra: contador int
        + tiempo: tiempo que se toma la muestra en seg    '''
    def sampleAceleracion(self, tiempo, save=True):
        acc = self.sensorObject.get_acc_data(self.gUnits)
        self.temperatura = self.sensorObject.get_temperatura()  # Grado celsius
        ax = acc['x']
        ay = acc['y']
        az = acc['z']
        accRMS = self.calc_Acc_RMS(ax, ay, az)

        '''ROTACION no importa en que unidades se trabaja, da el mismo valor'''
#        rotX = self.sensorObject.get_x_rotation(ax, ay, az)
#        rotY = self.sensorObject.get_y_rotation(ax, ay, az)
        # no se puede calcular el angulo en Z. ref:
        # https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

#        '''INCLINACION'''
#        tiltX = self.sensorObject.get_x_Tilt(ax, ay, az)
#        tiltY = self.sensorObject.get_y_Tilt(ax, ay, az)
#        print("incli. x, y: ", tiltX, tiltY)

        self.waitToSampler()  # para no tener datos repetidos
        return {"x": ax, "y": ay, "z": az, "rms": accRMS, 'time': tiempo}

    ''' Evita tomar mas datos de lo q indica la frecuencia de muestreo.'''
    def waitToSampler(self):
        frec = self.sensorObject.get_frecMuestreoAcc()

        if(frec >= 750):
            pass
        elif(500 <= frec < 750):
            time.sleep(1.0/(self.frecuencia*2.2))
        elif(350 <= frec < 500):
            time.sleep(1.0/(self.frecuencia * 4))
        elif(100 < frec < 350):
            time.sleep(1.0/(self.frecuencia * 1.8))
        else:
            time.sleep(1.0/(self.frecuencia * 1))

    def sampleGyro(self, tiempo, save=True):
        gyro = self.sensorObject.get_gyro_data()
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']

        if(save):
            self.saveSampleGyro(tiempo, gx, gy, gz)
        return {"gx": gx, "gy": gy, "gz": gz}

    """  ELIMINA DECIMALES """
    def trunk(self, numberFloat):
        return "{:.4f}".format(numberFloat)

    def saveSampleACC(self, ax, ay, az, accRMS, timeNow):
        txt = self.trunk(ax) + ";" + self.trunk(ay) + ";"
        txt += self.trunk(az) + ";" + self.trunk(accRMS) + ";"
        txt += self.trunk(timeNow) + "\n"
        saveMuestra = sd_card(self.arch_Acc)
        saveMuestra.escribir(txt)

    def saveSampleGyro(self, timeNow, rotX_gyro, rotY_gyro,
                       rotZ_gyro, tiltX, tiltY):
        txt = self.trunk(rotX_gyro) + ";" + self.trunk(rotY_gyro) + ";"
        txt += self.trunk(rotZ_gyro) + ";"
        txt += self.trunk(tiltX) + ";" + self.trunk(tiltY) + ";"
        txt += self.trunk(timeNow) + "\n"
        saveMuestra = sd_card(self.arch_Gyro)
        saveMuestra.escribir(txt)

