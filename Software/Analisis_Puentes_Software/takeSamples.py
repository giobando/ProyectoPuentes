# -*- coding: utf-8 -*-
from datosAlmacen.sd_card import sd_card
from dispositivo.gestorSensor import gestorSensor

from constantes.const import ZERO_EJE_Z
from constantes.const import ACCE_MINIMA

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
        self.frecuencia = frec # de momento no se esta ocupando

        # definicion del valor minimo depende de las unidades
        if(ZERO_EJE_Z and self.gUnits):
            print("entro a 1")
            self.aceleracionMinima = ACCE_MINIMA

        elif (ZERO_EJE_Z and not self.gUnits):
            print("entro a 2")
            self.aceleracionMinima = ACCE_MINIMA

        elif(not ZERO_EJE_Z and self.gUnits): # i.e cercano a 1g
            print("entro a 3")
            self.aceleracionMinima = ACCE_MINIMA + 1

        elif (not ZERO_EJE_Z and not self.gUnits):
            print("entro a 4")
            self.aceleracionMinima = ACCE_MINIMA * 9.8+ 9.8


    '''
    Metodo encargado de calcular la aceleracion total
    Recibe: aceleracion de los 3 ejes, No importa en que unidades este.  '''
    def calc_Acc_RMS(self, ax, ay, az):
        # para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    '''
    Metodo encargado de las muestras
    Recibe:
        + frec: frecuencia de muestreo en Hz (limite max 1000Hz, mas de esto no
          es posible a menos que se use FIFO que proporciona el sensor)   '''
    def makeTest(self, save=False):
        start = time.time()
        finalTime = 0
        countSamples = 0

        while(finalTime < self.duration or self.duration == -1 ):
            save = False
            sampleACCRMS = self.sample(finalTime, save)

            if(sampleACCRMS >=  self.aceleracionMinima ): # entonces se va guardar los datos
                print("perturbacion")
                muestrasFourier = 0
                self.sensorObject.set_frecMuestreoAcc(1000)

                while(muestrasFourier <= 32768 and finalTime < self.duration):
                    finalTime = time.time() - start
                    save = True
                    self.sample(finalTime, save)
                    time.sleep(1.0/2500) # para no tener datos repetidos
                    muestrasFourier += 1
                self.sensorObject.set_frecMuestreoAcc(self.frecuencia)
                countSamples += muestrasFourier
            else:
                countSamples += 1

            finalTime = time.time() - start
            time.sleep(1.0/(self.frecuencia*2)) # para no tener datos repetidos, se espera la mitad del tiempo que tarda en tomar muestras, Nyquist
        print("Muestra finalizada, el num de muestras total fue:", countSamples)

    '''
    Encargado de tomar una muestra y almacenarla en un txt
    Recibe:
        + numMuestra: contador int
        + tiempo: tiempo que se toma la muestra en seg    '''
    def sample(self, tiempo, save=True):
        # si no tiene parametros, retorna m/s2
        acc = self.sensorObject.get_acc_data(self.gUnits)
        gyro = self.sensorObject.get_gyro_data()
        self.temperatura = self.sensorObject.get_temperatura() # degree celsius

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
            self.saveTXT(ax, ay, az, accRMS, tiempo, gx, gy, gz, tiltX, tiltY)
        return accRMS

    '''
    Encargado de almacenar cada muestra en un txt.
    Recibe
        + aceleracion en cada eje
        + aceleraciron RMS calculado
        + Tiempo que se toma la muestra
        + medida del giroscopio
        + inclinacion de la aceleracion   '''
    def saveTXT(self, ax, ay, az, accRMS, timeNow, rotX_gyro, rotY_gyro, rotZ_gyro, tiltX, tiltY):
        # creando carpeta
        saveMuestra = sd_card(self.sensorObject.sensorName)
        carpetaNueva = self.nameTest
        direcCarpeta = "../Analisis_Puentes_Software/AlmacenPruebas/"
        saveMuestra.crearCarpeta(direcCarpeta + carpetaNueva)

        # Creando archivo para aceleraciones
        arch_Acc = direcCarpeta + self.nameTest + "/" +"sensor_"+ self.sensorObject.sensorName + "_Aceleracion.txt"
        saveMuestra = sd_card(arch_Acc)

        # guardando aceleraciones en txt
        txt_acc = ""
        txt_acc = str(ax) + "," + str(ay) + "," + str(az) + ","+ str(accRMS) + "," + str(timeNow) + "\n"
        saveMuestra.escribir(txt_acc)
        saveMuestra.cerrar()

#        # Creando archivo para gyroscopio
#        arch_Gyro = direcCarpeta +self.nameTest +"/"+self.sensorObject.sensorName +"_Gyro.txt"
#        saveMuestra2 = sd_card(arch_Gyro)
#
#        # guardando gyroscopio data
#        txt_gyro = ""
#        txt_gyro = txt_gyro + str(rotX_gyro) + "," + str(rotY_gyro) + "," + str(rotZ_gyro) + ","
#        txt_gyro = txt_gyro + str(tiltX) + "," + str(tiltY)
#        txt_gyro = txt_gyro + "l" + ","
#        txt_gyro = txt_gyro + "\n"
#        saveMuestra2.escribir(txt_gyro)
#        saveMuestra2.cerrar()

#def graficar(nombreSensor, nombrePrueba):
#    from presentacion.grafica import grafica
#    grafico_sensor1 = grafica() #"Prueba #1", "sensor1")
#    print("nuevos offset")
#    print( sensorObject.get_offset_acc())
#    print( sensorObject.get_offset_gyro())
#
#    print("sensiblidad raw:",sensorObject.get_sensiblidad_acc())
#    sensorObject.set_filtroPasaBaja(numFiltro)       # pruebas


class gui:
    def inicializarSensor(self, nameSensor, portConected, sensibilidadSensor, numFiltro, frecuencia):
        print("-Inicializando el sensor \'" + nameSensor +"\' \nEspere por favor...\n")
        sensor = gestorSensor(nameSensor, portConected, sensibilidadSensor)

        print("-Sensibilidad para calibrar: " + str(sensibilidadSensor) +" g")

        sensorObject = sensor.getSensorObject()
        sensor.calibrarDispositivo()

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
        '''======================       PARAMETROS       ======================='''
        nameTest = "7Agosto" # Usado para nombrar la carpeta para guardar datos

        # sensor 1
        nameSensor1 = "sensor1"
        portConected1 = 1       # Puerto fisico Conectado: 1= 0x68 o 2 = 0x69

        # sensor 2
    #    nameSensor2 = "sensor2"
    #    portConected2 = 2       # Puerto fisico Conectado: 1= 0x68 o 2 = 0x69

        # prueba
        numFiltro =3 # 0=260, 1=184, 2=94, 3=44, 4=21, 5=10, 6=5, 7=reserved (Hz)
        frecuencia = 22       # maximo (hz), solo sii hay filtro.
        duration = 100         # -1: continuo (s)
        sensibilidadSensor = 2 # sensiblidades 2,4,8,16
        gUnits = False           # True: unidades en g, False: unidades en m/s2

        print("=================  INICIALIZACION  ==================")
        sensor1Object = self.inicializarSensor(nameSensor1, portConected1, sensibilidadSensor, numFiltro, frecuencia)


        print("\n\n===============  Ejecutando Pruebas  ================")
        # hacer hilos aqui!!!
        print("PARAMETROS CONFIGURADOS:")
        print("-Nombre de la prueba: \'" + nameTest + "\'")
        print("-Duracion de prueba (seg): " + str(duration))
        print("-Frec corte configurado: " + str(numFiltro))
        print("-Sensibilidad para muestrear: " + str( sensor1Object.get_sensiblidad_acc()))
        print("-Unidades \'g\' activado: " + str(gUnits))
        print("-Frecu muestreo: " + str(sensor1Object.get_frecMuestreoAcc()))

        testsensor1 = test(nameTest, sensor1Object, duration, frecuencia, gUnits)
        testsensor1.makeTest()

##    grafico_sensor1 = grafica(nameTest, nameSensor1, 45,False) #milisengudos


#    if __name__ == "__main__":
#        main()

correr = gui()
correr.main()

