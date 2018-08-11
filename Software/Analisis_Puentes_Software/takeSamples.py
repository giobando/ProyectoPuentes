# -*- coding: utf-8 -*-
from datosAlmacen.sd_card import sd_card
from dispositivo.gestorSensor import gestorSensor

from constantes.const import ZERO_EJE_Z
from constantes.const import ACCE_MINIMA
from constantes.const import DIRECC_TO_SAVE

import math
import time

# esto es solo para las pruebas!!!
import threading


class test:

    sensorObject = None
    nameTest = None
    temperatura = -1
    duration = -1   # if -1: continue time.
    gUnits = True   # it is indicate "g" units
    frecuencia = None
    aceleracionMinima = 0

    arch_Acc = ""  # ARchivo para guardar Aceleraciones
    arch_Gyro = ""  # ARchivo para guardar gyroscopio

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
        self.arch_Acc = DIRECC_TO_SAVE + nameTest + "/" + "sensor_"
        self.arch_Acc += self.sensorObject.sensorName + "_Aceleracion.csv"
        self.arch_Gyro = DIRECC_TO_SAVE + self.nameTest + "/" + "sensor_"
        self.arch_Gyro += self.sensorObject.sensorName + "_Gyro.csv"

    def defineMinValue_to_aceleration(self):
        if(ZERO_EJE_Z and self.gUnits):
            print("entro a 1")
            self.aceleracionMinima = ACCE_MINIMA

        elif (ZERO_EJE_Z and not self.gUnits):
            print("entro a 2")
            self.aceleracionMinima = ACCE_MINIMA

        elif(not ZERO_EJE_Z and self.gUnits):  # i.e cercano a 1g
            print("entro a 3")
            self.aceleracionMinima = ACCE_MINIMA + 1

        elif (not ZERO_EJE_Z and not self.gUnits):
            print("entro a 4")
            self.aceleracionMinima = ACCE_MINIMA * 9.8 + 9.8

    '''Calcula la aceleracion total. Recibe:
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
        txt = "ax("+accUnits+"),ay("+accUnits+"),az("+accUnits+"),"
        txt += "accRMS(" + accUnits + "),time(s)\n"
        saveMuestra.escribir(txt)

        saveMuestra = sd_card(self.arch_Gyro)
        txt = "gx(degree/s),gy(degree/s),gz(degree/s),inclinacionX,"
        txt += "inclinacionY,time(s)\n"
        saveMuestra.escribir(txt)

    '''
    Metodo encargado de las muestras
    Recibe:
        + frec: frecuencia de muestreo en Hz (limite max 1000Hz, mas de esto no
          es posible a menos que se use FIFO que proporciona el sensor)'''
    def makeTest(self, save=False):
        start = time.time()
        finalTime = 0
        countSamples = 0
        self.crearArchivos()

        while(finalTime < self.duration or self.duration == -1):
            save = False
            sampleACCRMS = self.sample(finalTime, save)

            # Inicia guardar los datos
            if(sampleACCRMS >= self.aceleracionMinima):
                print("perturbacion")
                muestrasFourier = 0
                self.sensorObject.set_frecMuestreoAcc(1000)

                while(muestrasFourier <= 32768 and finalTime < self.duration):
                    finalTime = time.time() - start
                    save = True
                    self.sample(finalTime, save)
                    time.sleep(1.0/2500)  # para no tener datos repetidos
                    muestrasFourier += 1
                self.sensorObject.set_frecMuestreoAcc(self.frecuencia)
                countSamples += muestrasFourier
            else:
                countSamples += 1

            finalTime = time.time() - start
            # para no tener datos repetidos:
            # Espera la mitad del tiempo que tarda en tomar muestras, Nyquist
            time.sleep(1.0/(self.frecuencia*2))
        print("Muestra finalizada, num de muestras total fue:", countSamples)

    ''' Toma una muestra y almacenarla en un txt, Recibe:
        + numMuestra: contador int
        + tiempo: tiempo que se toma la muestra en seg    '''
    def sample(self, tiempo, save=True):
        # si no tiene parametros, retorna m/s2
        acc = self.sensorObject.get_acc_data(self.gUnits)
        gyro = self.sensorObject.get_gyro_data()
        self.temperatura = self.sensorObject.get_temperatura()  # Grado celsius

        ''' SAMPLES '''
        ax = acc['x']
        ay = acc['y']
        az = acc['z']
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']
        accRMS = self.calc_Acc_RMS(ax, ay, az)

        '''ROTACION no importa en que unidades se trabaja, da el mismo valor'''
        rotX = self.sensorObject.get_x_rotation(ax, ay, az)
        rotY = self.sensorObject.get_y_rotation(ax, ay, az)
        # no se puede calcular el angulo en Z. ref:
        # https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

        ''' INCLINACION'''
        tiltX = self.sensorObject.get_x_Tilt(ax, ay, az)
        tiltY = self.sensorObject.get_y_Tilt(ax, ay, az)

        if(save):
            self.saveSampleACC(ax, ay, az, accRMS, tiempo)
            self.saveSampleGyro(tiempo, gx, gy, gz, tiltX, tiltY)
        return accRMS

    """  ELIMINA ALGUNOS DECIMALES """
    def trunk(self, numberFloat):
        return "{:.4f}".format(numberFloat)

    def saveSampleACC(self, ax, ay, az, accRMS, timeNow):
        txt = self.trunk(ax) + "," + self.trunk(ay) + ","
        txt += self.trunk(az) + "," + self.trunk(accRMS) + ","
        txt += self.trunk(timeNow) + "\n"
        saveMuestra = sd_card(self.arch_Acc)
        saveMuestra.escribir(txt)

    def saveSampleGyro(self, timeNow, rotX_gyro, rotY_gyro,
                       rotZ_gyro, tiltX, tiltY):
        txt = self.trunk(rotX_gyro) + "," + self.trunk(rotY_gyro) + ","
        txt += self.trunk(rotZ_gyro) + ","
        txt += self.trunk(tiltX) + "," + self.trunk(tiltY) + ","
        txt += self.trunk(timeNow) + "\n"
        saveMuestra = sd_card(self.arch_Gyro)
        saveMuestra.escribir(txt)


class gui:
    def inicializarSensor(self, nameSensor, portConected,
                          sensibilidadSensor, numFiltro, frecuencia):
        print("-Inicializando el sensor \'" + nameSensor)
        print("\' \nEspere por favor...\n")

        sensor = gestorSensor(nameSensor, portConected, sensibilidadSensor)
        print("-Sensibilidad para calibrar: " + str(sensibilidadSensor) + " g")

        sensorObject = sensor.getSensorObject()
#        sensor.calibrarDispositivo()
        print("\n-Configurando Filtro pasa Baja...")

        sensorObject.set_filtroPasaBaja(numFiltro)
        print("-Configurando frecuencia Muestreo...")

        sensorObject.set_frecMuestreoAcc(frecuencia)
        print("-Configurando sensibilidad...")

        sensorObject.set_sensibilidad_acc(sensibilidadSensor)
        sensorObject.set_sensibilidad_gyro(500)
        print("-calibrando con parametros configurados:")

        return sensorObject

    def main(self):
        '''======================     PARAMETROS     ======================='''
        nameTest = "10agosto"  # Para nombrar la carpeta para guardar datos

        # sensor 1
        nameSensor1 = "sensor1"
        portConected1 = 1   # Puerto fisico Conectado: 1= 0x68 o 2 = 0x69

        # sensor 2
    #    nameSensor2 = "sensor2"
    #    portConected2 = 2       # Puerto fisico Conectado: 1= 0x68 o 2 = 0x69

        # prueba
        # Filtro> # 0=260, 1=184, 2=94, 3=44, 4=21, 5=10, 6=5, 7=reserved (Hz)
        numFiltro = 3
        frecuencia = 22  # maximo (hz), solo sii hay filtro.
        duration = 10  # -1: continuo (s)
        sensibilidadSensor = 2  # sensiblidades 2,4,8,16
        gUnits = False  # True: unidades en g, False: unidades en m/s2

        print("=================  INICIALIZACION  ==================")
        sensor1Object = self.inicializarSensor(nameSensor1, portConected1,
                                               sensibilidadSensor, numFiltro,
                                               frecuencia)

        print("\n\n===============  Ejecutando Pruebas  ================")
        # hacer hilos aqui!!!
        print("PARAMETROS CONFIGURADOS:")
        print("-Nombre de la prueba: \'" + nameTest + "\'")
        print("-Duracion de prueba (seg): " + str(duration))
        print("-Frec corte configurado: " + str(numFiltro))
        string = str(sensor1Object.get_sensiblidad_acc())
        print("-Sensibilidad para muestrear: " + string)
        print("-Unidades \'g\' activado: " + str(gUnits))
        print("-Frecu muestreo: " + str(sensor1Object.get_frecMuestreoAcc()))

        testsensor1 = test(nameTest, sensor1Object, duration,
                           frecuencia, gUnits)
        testsensor1.makeTest()


correr = gui()
correr.main()

