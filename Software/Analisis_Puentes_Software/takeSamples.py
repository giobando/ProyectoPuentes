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

    arch_Acc = ""       # ARchivo para guardar Aceleraciones
    arch_Gyro = ""      # ARchivo para guardar gyroscopio
    spectrum = None

    '''
    Recibe:
        + nameTest: nombre de la prueba
        + sensorObject: Objecto mpu6050
        + duration: tiempo en segundos
        + gUnits: True: para unidades en g, False: para unidades en m/s2 '''
    def __init__(self, nameTest, sensorObject, duration, frec, gUnits):
        self.nameTest = nameTest
        self.sensorObject = sensorObject
        self.duration = duration
        self.gUnits = gUnits
        self.frecuencia = frec  # de momento no se esta ocupando

        # definicion del valor minimo depende de las unidades
        self.defineMinValue_to_aceleration()

        # creando carpeta para almacenar datos
        saveMuestra = sd_card('')
        carpetaNueva = self.nameTest
        saveMuestra.crearCarpeta(DIRECC_TO_SAVE + carpetaNueva)

        # Creando Archivos para los datos
        self.arch_Acc = DIRECC_TO_SAVE + nameTest + "/"
        self.arch_Acc += "nodo_" + str(NAME_NODE)
        self.arch_Acc += "-sensor_" + self.sensorObject.sensorName
        self.arch_Acc +=  "_Aceleracion.csv"

        self.arch_Gyro = DIRECC_TO_SAVE + self.nameTest + "/"
        self.arch_Gyro += "nodo_" + str(NAME_NODE)
        self.arch_Gyro += "-sensor_" + self.sensorObject.sensorName + "_Gyro.csv"

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
        + Aceleracion de los 3 ejes, No importa en que unidades este.  '''
    def calc_Acc_RMS(self, ax, ay, az):
        # para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    def get_unitAcc(self):
        if(self.gUnits):
            return "g"
        else:
            return "m/s"

    "Crea archivos con encabezados para aceleracion y gyroscopio"
    def crearArchivos(self):
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

            if(rmsSample >= self.aceleracionMinima): # Inicia guardar los datos
                numSampleToFourier = 0
                sampleToFourierX = []
                sampleToFourierY = []
                sampleToFourierZ = []
                sampleToFourierRMS = []
#                self.sensorObject.set_frecMuestreoAcc(1000)
#                self.frecuencia = 1000

                while(numSampleToFourier < NUM_SAMPLES_TO_FOURIER and
                      finalTime <= self.duration):
                    sampleACC = self.sampleAceleracion(finalTime)
                    rmsSample = sampleACC['rms']

                    if(rmsOld != rmsSample):
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
#                    self.calcularFourier(sampleToFourierX,
#                                         sampleToFourierY,
#                                         sampleToFourierZ,
#                                         sampleToFourierRMS, contadorEspectros)
                    hilo1 = threading.Thread(target= self.calcularFourier,
                                             args=(sampleToFourierX,
                                                   sampleToFourierY,
                                                   sampleToFourierZ,
                                                   sampleToFourierRMS,
                                                   contadorEspectros,)
                                             )
                    hilo1.start()
                    contadorEspectros += 1

                # reconfiguramos la frecuencia.
                self.sensorObject.set_frecMuestreoAcc(self.frecuencia)
                countSamples += numSampleToFourier
            else:
                countSamples += 1

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


class gui:
    bus = smbus.SMBus(1)  # 1 = i2c
    booleanPort1 = None
    booleanPort2 = None
    nameSensor1 = NAME_SENSOR_PORT1
    portConected1 = NUMBER_PORTSENSOR1
    nameSensor2 = NAME_SENSOR_PORT2
    portConected2 = NUMBER_PORTSENSOR2

    def __init__(self):  # scan i2c devices
        self.booleanPort1 = self.scanI2cDevice(PORT1)
        self.booleanPort2 = self.scanI2cDevice(PORT2)

    ''' evalua si la direccion que recibe esta activa'''
    def scanI2cDevice(self, dirDevice):
        try:
            self.bus.read_byte(dirDevice)
            return True
        except:
            return False

    def inicializarSensor(self, nameSensor, portConected,
                          sensibilidadSensor, numFiltro, frecuencia):
        print("-Espere, inicializando el sensor \'" + nameSensor + "\'...")
        sensor = gestorSensor(nameSensor, portConected, sensibilidadSensor)
        print("-Sensibilidad para calibrar: " + str(sensibilidadSensor) + " g")
        sensorObject = sensor.getSensorObject()
        print("-Configurando Filtro pasa Baja...")
        sensorObject.set_filtroPasaBaja(numFiltro)
        print("-Configurando frecuencia Muestreo...")
        sensorObject.set_frecMuestreoAcc(frecuencia)
        print("-Configurando sensibilidad...")
        sensorObject.set_sensibilidad_acc(sensibilidadSensor)
        sensorObject.set_sensibilidad_gyro(500)
        print("-calibrando con parametros configurados...")
#        sensor.calibrarDispositivo()
        return sensorObject

    def verificarPuertosConectados(self):
        if(self.booleanPort1 or self.booleanPort2):
            print("=========== INICIALIZANDO PUERTOS ===========")
        else:
            print("\nError!, No se encuentra sensores conectados")

    def habilitarSensor(self, namePortSensUsed, sensibilidadSensor,
                        numFiltro, nameTest,
                        duration, frecuencia, gUnits):
        print("Puerto" + str(namePortSensUsed)+" conectado")

        if(namePortSensUsed =="1"):
            numberPuerto = NUMBER_PORTSENSOR1
        elif(namePortSensUsed =="2"):
            numberPuerto = NUMBER_PORTSENSOR2

        sensorObject_port = self.inicializarSensor(namePortSensUsed,
                                                   numberPuerto,
                                                   sensibilidadSensor,
                                                   numFiltro,
                                                   frecuencia)

        senConfig= str(sensorObject_port.get_sensiblidad_acc())
        frecConfig = str(sensorObject_port.get_frecMuestreoAcc())

        print("-Sensibilidad config: " + senConfig + "g,\tpuerto: " + str(namePortSensUsed))
        print("-Muestreo config a: " + frecConfig + "Hz\tpuerto: " + str(namePortSensUsed))

        testsensor_puerto = test(nameTest, sensorObject_port, duration,
                                  frecuencia, gUnits)
        # por hilos
#            hilo_puerto1 = threading.Thread(target=testsensor_puerto1.makeTest)
#            hilo_puerto1.start()
        # sin hilos

        print("iniciado")
        testsensor_puerto.makeTest()

    def main(self):
        '''======================     PARAMETROS     ======================='''
        nameTest = "12OCTUBRE"  # Nombre de la carpeta para guardar datos

        numFiltro = 0  # Filtro> # 0=260, 1=184, 2=94, 3=44, 4=21, 5=10, 6=5, 7=reserved (Hz)
        frecuencia = 1000       # maximo 1K(hz), solo sii hay filtro.
        duration = 1*60         # -1: continuo (s), digitar en minutos
        sensibilidadSensor = 2  # sensiblidades 2,4,8,16
        gUnits = True           # True: unidades en g, False: unidades en m/s2

        # ====== THREADS ======
        print("\n============¿==============================")
        print("-Prueba nombre: \'" + nameTest + "\', nodo: " + str(NAME_NODE))
        print("-Duracion de prueba (seg): " + str(duration))
        print("-Frec corte configurado: " + str(numFiltro))
        print("-Unidades \'g\': " + str(gUnits))
        print("===========================================\n")

        self.verificarPuertosConectados()

        if(self.booleanPort1):
            self.habilitarSensor(NAME_SENSOR_PORT1, sensibilidadSensor,
                                 numFiltro, nameTest,
                                 duration, frecuencia, gUnits)
        if(self.booleanPort2):
            self.habilitarSensor(NAME_SENSOR_PORT2, sensibilidadSensor,
                                 numFiltro, nameTest,
                                 duration, frecuencia, gUnits)


#        if(self.booleanPort2):
#            print("Puerto 2 conectado")
#            sensorObject_port2 = self.inicializarSensor(NAME_SENSOR_PORT2,
#                                                        NUMBER_PORTSENSOR2,
#                                                        sensibilidadSensor,
#                                                        numFiltro,
#                                                        frecuencia)
#
#            string2Sensiblidad = str(sensorObject_port2.get_sensiblidad_acc())
#            string2Frec = str(sensorObject_port2.get_frecMuestreoAcc())
#
#            print("\nPARAMETROS CONFIGURADOS en puerto 2:")
#            print("-Sensibilidad para muestrear: " + string2Sensiblidad)
#            print("-Frecu muestreo puerto 2: " + string2Frec)
#
#            testsensor_puerto2 = test(nameTest, sensorObject_port2, duration,
#                                      frecuencia, gUnits)
#            hilo_puerto2 = threading.Thread(target=testsensor_puerto2.makeTest)
#            hilo_puerto2.start()


correr = gui()
correr.main()
