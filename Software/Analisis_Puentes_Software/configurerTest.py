#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 14 03:37:01 2019

@author: pi
"""

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


class configurerTest:
    bus = smbus.SMBus(1)  # 1 = i2c
    booleanPort1 = None
    booleanPort2 = None
    nameSensor1 = NAME_SENSOR_PORT1
    portConected1 = NUMBER_PORTSENSOR1
    nameSensor2 = NAME_SENSOR_PORT2
    portConected2 = NUMBER_PORTSENSOR2

    # objecto sensor a inicializar:
    sensorObject = None
    sensorObject_port1 = None
    sensorObject_port2 = None

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

#    def getSensorObject(self):
#        return self.sensorObject
#
#    def setSensorObject(self,pSensorObject):
#        self.sensorObject = pSensorObject

    def getSensorObject_port1(self):
        return self.sensorObject_port1

    def setSensorObject_port1(self, pSensorObject):
        self.sensorObject_port1 = pSensorObject

    def getSensorObject_port2(self):
        return self.sensorObject_port2

    def setSensorObject_port2(self, pSensorObject):
        self.sensorObject_port2 = pSensorObject
#
#    def inicializarSensor(self, nameSensor, portConected,
#                          sensibilidadSensorAcc, numFiltro, frecuencia,
#                          sensiGyro):
#        global CALIBRATED
#        global oldSensibilidad
#        print("inicializando, name: " + nameSensor + ", port" +
#              str(portConected))
#        print("-Espere, inicializando el sensor \'" + nameSensor + "\'...")
#        sensor = gestorSensor(nameSensor, portConected, sensibilidadSensorAcc)
#        print("-Sensibilidad a calibrar: " + str(sensibilidadSensorAcc) + " g")
#        sensorObject = sensor.getSensorObject()
#        print("-Configurando Filtro pasa Baja...")
#        sensorObject.set_filtroPasaBaja(numFiltro)
#        print("-Configurando frecuencia Muestreo...")
#        sensorObject.set_frecMuestreoAcc(frecuencia)
#
#        # Se calibra solo cuando se modifique la sensibliidad
#        if(oldSensibilidad != sensibilidadSensorAcc):
#            print("-Configurando sensibilidad...")
#            oldSensibilidad = sensibilidadSensorAcc
#            CALIBRATED = False
#
#        sensorObject.set_sensibilidad_acc(sensibilidadSensorAcc)
#        sensorObject.set_sensibilidad_gyro(sensiGyro)
#
#        print("nombre sesor es" + sensorObject.getNameSensor())
#        if(CALIBRATED):
#            print("Sensor ya fue calibrado")
#        else:
#            CALIBRATED = True
#            print("-calibrando con parametros configurados...")
##            sensor.calibrarDispositivo()

#        print("iniciando, nameSensor: "+ nameSensor + ", names:"
# + NAME_SENSOR_PORT1)
#        if(nameSensor == NAME_SENSOR_PORT1):
#            print("\niniiciando sensor, puerto 1 ")
#            self.setSensorObject_port1(sensorObject)
#        elif(nameSensor == NAME_SENSOR_PORT2):
#            print("\niniiciando sensor, puerto 2 ")
#            self.setSensorObject_port2(sensorObject)
##        self.setSensorObject(sensorObject)

    def habilitarSensor(self, nameSensor, sensibilidadSensor, numFiltro,
                        nameTest, duration, frecuencia, gUnits, sensiGyro,
                        testObject):
        global CALIBRATED
        global oldSensibilidad

        if(nameSensor == NAME_SENSOR_PORT1):
            numberPuerto = NUMBER_PORTSENSOR1
            print("\nIniciando sensor, puerto 1")
        elif(nameSensor == NAME_SENSOR_PORT2):
            print("\nIniciando sensor, puerto 2")
            numberPuerto = NUMBER_PORTSENSOR2

        print("\nHabilitando el puerto: " + str(nameSensor))
        sensor = gestorSensor(nameSensor, numberPuerto, sensibilidadSensor)
        sensorObject = sensor.getSensorObject()
        print("\n-Calibrando sensibilidad del puerto: " + str(nameSensor))
        sensorObject.set_sensibilidad_acc(sensibilidadSensor)
        sensorObject.set_sensibilidad_gyro(sensiGyro)
        print("\n-Configurando Filtro pasa Baja del puerto " + str(nameSensor))
        sensorObject.set_filtroPasaBaja(numFiltro)
        print("\n-Configurando frec. Muestreo del puerto " + str(nameSensor))
        sensorObject.set_frecMuestreoAcc(frecuencia)
        print("\nConfiguracion Finalizada del puerto: " +
              sensorObject.getNameSensor())
        frecConfig = str(sensorObject.get_frecMuestreoAcc())
        senConfig = str(sensorObject.get_sensiblidad_acc())
        print("\n-Muestreo y sensiblidad configurado a: " + frecConfig + "Hz, "
              + "sensibilidad: " + senConfig + " en el puerto: "
              + str(nameSensor))
        if(nameSensor == NAME_SENSOR_PORT1):
            self.setSensorObject_port1(sensorObject)
        elif(nameSensor == NAME_SENSOR_PORT2):
            self.setSensorObject_port2(sensorObject)

        print("sensnor naem: " + sensorObject.getNameSensor())
#        # Se calibra solo cuando se modifique la sensibliidad
#        if(oldSensibilidad != sensibilidadSensorAcc):
#            print("-Configurando sensibilidad...")
#            oldSensibilidad = sensibilidadSensorAcc
#            CALIBRATED = False

#        if(CALIBRATED):
#            print("Sensor ya fue calibrado")
#        else:
#            CALIBRATED = True
#            print("-calibrando con parametros configurados...")
#            sensor.calibrarDispositivo()

#        print("iniciando, nameSensor: "+ nameSensor + ", names:"
# + NAME_SENSOR_PORT1)
        testObject.runTest(sensorObject)

    def get_ID_frecCorte(self, frecCorte):
        # Filtro> # 0=260, 1=184, 2=94, 3=44, 4=21, 5=10, 6=5, 7=reserved (Hz)
        filtro = {'260 Hz': 0, '184 Hz': 1, '94 Hz': 2, '44 Hz': 3, '21 Hz': 4,
                  '10 Hz': 5, '5 Hz': 6, '-1': 7}
        id_FrecCorte = filtro[frecCorte]
        return id_FrecCorte

    def printParametros(self, parametros):
        nameTest = parametros["nameTest"]
        numFiltro = self.get_ID_frecCorte(parametros["frecCorte"])
        duration = parametros["durac"] * 60
        sensibilidadGyro = parametros["sensGyro"]
        gUnits = parametros["gUnits"]
        print("\n========== PARAMETROS ============")
        print("-Prueba nombre: \'" + nameTest + "\', nodo: " + str(NAME_NODE))
        print("-Duracion de prueba (seg): " + str(duration))
        print("-id Frec corte configurado: " + str(numFiltro))
        print("-Unidades \'g\': " + str(gUnits))
        print("-Sensibilidad giroscopio: " + str(sensibilidadGyro))
        print("======================")

    '''Configurador los dispositivos.
        Recibe como diccionario "Parametros":
        nameTest = (string)Nombre de la carpeta para guardar datos
        numFiltro = (int)
        frecuencia = (int) maximo 1K(hz), solo sii hay filtro.
        duration = (int) -1: continuo (s), digitar en minutos
        sensibilidadSensor = (int) sensiblidades 2,4,8,16
        sensibilidadGyro = parametros["sensGyro"]
        gUnits = (int) True: unidades en g, False: unidades en m/s2 '''
    def runConfigurer(self, parametros, testObject):
        nameTest = parametros["nameTest"]
        numFiltro = self.get_ID_frecCorte(parametros["frecCorte"])
        frecuencia = parametros["fMuestOn"]
        duration = parametros["durac"] * 60
        sensibilidadSensor = parametros["sensAcc"]
        sensibilidadGyro = parametros["sensGyro"]
        gUnits = parametros["gUnits"]
        self.booleanPort1 = self.scanI2cDevice(PORT1)
        self.booleanPort2 = self.scanI2cDevice(PORT2)
        self.printParametros(parametros)

        if(self.booleanPort1 and self.booleanPort2):
            hilo_puerto1 = threading.Thread(target=self.habilitarSensor,
                                            args=(NAME_SENSOR_PORT1,
                                                  sensibilidadSensor,
                                                  numFiltro, nameTest,
                                                  duration, frecuencia, gUnits,
                                                  sensibilidadGyro,
                                                  testObject,))
            hilo_puerto2 = threading.Thread(target=self.habilitarSensor,
                                            args=(NAME_SENSOR_PORT2,
                                                  sensibilidadSensor,
                                                  numFiltro, nameTest,
                                                  duration, frecuencia, gUnits,
                                                  sensibilidadGyro,
                                                  testObject,))
            hilo_puerto1.start()
            hilo_puerto2.start()
        elif(self.booleanPort1):
            self.habilitarSensor(NAME_SENSOR_PORT1, sensibilidadSensor,
                                 numFiltro, nameTest,
                                 duration, frecuencia, gUnits,
                                 sensibilidadGyro, testObject)
        elif(self.booleanPort2):
            self.habilitarSensor(NAME_SENSOR_PORT2, sensibilidadSensor,
                                 numFiltro, nameTest,
                                 duration, frecuencia, gUnits,
                                 sensibilidadGyro, testObject)
        else:
            print("\nError!, No se encuentra sensores conectados")
        return True

# correr = gui()
# correr.runConfigurer()
