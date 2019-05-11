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

#from constantes.const import offset_accX1 as ACC_X1
#from constantes.const import offset_accY1 as ACC_Y1
#from constantes.const import offset_accZ1 as ACC_Z1
#from constantes.const import offset_gyrX1 as GYRO_X1
#from constantes.const import offset_gyrY1 as GYRO_Y1
#from constantes.const import offset_gyrZ1 as GYRO_Z1
#from constantes.const import offset_accX2 as ACC_X2
#from constantes.const import offset_accY2 as ACC_Y2
#from constantes.const import offset_accZ2 as ACC_Z2
#from constantes.const import offset_gyrX2 as GYRO_X2
#from constantes.const import offset_gyrY2 as GYRO_Y2
#from constantes.const import offset_gyrZ2 as GYRO_Z2

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

    def getSensorObject_port1(self):
        return self.sensorObject_port1

    def setSensorObject_port1(self, pSensorObject):
        self.sensorObject_port1 = pSensorObject

    def getSensorObject_port2(self):
        return self.sensorObject_port2

    def setSensorObject_port2(self, pSensorObject):
        self.sensorObject_port2 = pSensorObject

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

        sensor = gestorSensor(nameSensor, numberPuerto, sensibilidadSensor)
        sensorObject = sensor.getSensorObject()
        sensorObject.set_sensibilidad_acc(sensibilidadSensor)
        sensorObject.set_sensibilidad_gyro(sensiGyro)
        sensorObject.set_filtroPasaBaja(numFiltro)
        sensorObject.set_frecMuestreoAcc(frecuencia)

        frecConfig = str(sensorObject.get_frecMuestreoAcc())
        senConfig = str(sensorObject.get_sensiblidad_acc())
        print("\nPUERTO: " + sensorObject.getNameSensor() + " CONFIGURADO en:"
              + "\n\t-Muestreo: " + frecConfig + "Hz\n\t-Sensibilidad acc: " +
              senConfig)
        if(nameSensor == NAME_SENSOR_PORT1):
            self.setSensorObject_port1(sensorObject)
        elif(nameSensor == NAME_SENSOR_PORT2):
            self.setSensorObject_port2(sensorObject)

        # Si la sensibilidad recibida es diferente a la anterior, se calibra
        if(oldSensibilidad != sensibilidadSensor):
            print("-Configurando sensibilidad...")
            oldSensibilidad = sensibilidadSensor
            sensor.calibrarDispositivo()
            CALIBRATED = True
        else:
            CALIBRATED = False
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
