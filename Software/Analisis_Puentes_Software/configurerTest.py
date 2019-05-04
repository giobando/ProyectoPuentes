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

    def setSensorObject_port1(self,pSensorObject):
        self.sensorObject_port1 = pSensorObject

    def getSensorObject_port2(self):
        return self.sensorObject_port2

    def setSensorObject_port2(self,pSensorObject):
        self.sensorObject_port2 = pSensorObject

    def inicializarSensor(self, nameSensor, portConected,
                          sensibilidadSensorAcc, numFiltro, frecuencia,
                          sensiGyro):
        global CALIBRATED
        global oldSensibilidad
        print("inicializando, name: " + nameSensor + ", port" + str(portConected))
        print("-Espere, inicializando el sensor \'" + nameSensor + "\'...")
        sensor = gestorSensor(nameSensor, portConected, sensibilidadSensorAcc)
        print("-Sensibilidad a calibrar: " + str(sensibilidadSensorAcc) + " g")
        sensorObject = sensor.getSensorObject()
        print("-Configurando Filtro pasa Baja...")
        sensorObject.set_filtroPasaBaja(numFiltro)
        print("-Configurando frecuencia Muestreo...")
        sensorObject.set_frecMuestreoAcc(frecuencia)

        # Se calibra solo cuando se modifique la sensibliidad
        if(oldSensibilidad != sensibilidadSensorAcc):
            print("-Configurando sensibilidad...")
            oldSensibilidad = sensibilidadSensorAcc
            CALIBRATED = False

        sensorObject.set_sensibilidad_acc(sensibilidadSensorAcc)
        sensorObject.set_sensibilidad_gyro(sensiGyro)

        print("nombre sesor es" + sensorObject.getNameSensor())
        if(CALIBRATED):
            print("Sensor ya fue calibrado")
        else:
            CALIBRATED = True
            print("-calibrando con parametros configurados...")
#            sensor.calibrarDispositivo()

#        print("iniciando, nameSensor: "+ nameSensor + ", names:" + NAME_SENSOR_PORT1)
        if(nameSensor == NAME_SENSOR_PORT1):
            print("\niniiciando sensor, puerto 1 ")
            self.setSensorObject_port1(sensorObject)
        elif(nameSensor == NAME_SENSOR_PORT2):
            print("\niniiciando sensor, puerto 2 ")
            self.setSensorObject_port2(sensorObject)
#        self.setSensorObject(sensorObject)

    def habilitarSensor(self, namePortSensUsed, sensibilidadSensor, numFiltro,
                        nameTest, duration, frecuencia, gUnits, sensiGyro):
        print("\nPuerto" + str(namePortSensUsed)+" conectado")

        if(namePortSensUsed == NAME_SENSOR_PORT1):
            numberPuerto = NUMBER_PORTSENSOR1
        elif(namePortSensUsed == NAME_SENSOR_PORT2):
            numberPuerto = NUMBER_PORTSENSOR2

        print( "\nPuerto" + str(namePortSensUsed)+" frecuencia:" +str(frecuencia))
        print("\nPuerto" + str(namePortSensUsed)+" sensygyro: "+ str(sensiGyro))
        self.inicializarSensor(namePortSensUsed,
                               numberPuerto,
                               sensibilidadSensor,
                               numFiltro,
                               frecuencia, sensiGyro)

        senConfig = str(self.sensorObject.get_sensiblidad_acc())
        frecConfig = str(self.sensorObject.get_frecMuestreoAcc())
        print("sensor: " + namePortSensUsed)
        print("-Sensibilidad config: " + senConfig + "g,\tpuerto: " +
              str(namePortSensUsed))
        print("-Muestreo config a: " + frecConfig + " Hz\tpuerto: " +
              str(namePortSensUsed))

    def get_ID_frecCorte(self, frecCorte):
        # Filtro> # 0=260, 1=184, 2=94, 3=44, 4=21, 5=10, 6=5, 7=reserved (Hz)
        filtro = {'260 Hz': 0, '184 Hz': 1, '94 Hz': 2, '44 Hz': 3, '21 Hz': 4,
                  '10 Hz': 5, '5 Hz': 6, '-1': 7}
        id_FrecCorte = filtro[frecCorte]

        return id_FrecCorte

    '''Configurador los dispositivos.
        Recibe: Parametros: Diccionario '''
    def runConfigurer(self, parametros):
        '''======================     PARAMETROS     ======================='''
        nameTest = parametros["nameTest"]          # (string)Nombre de la carpeta para guardar datos
        numFiltro = self.get_ID_frecCorte(parametros["frecCorte"])
        frecuencia = parametros["fMuestOn"]        # (int) maximo 1K(hz), solo sii hay filtro.
        duration = parametros["durac"] * 60        # (int) -1: continuo (s), digitar en minutos
        sensibilidadSensor = parametros["sensAcc"] # (int) sensiblidades 2,4,8,16
        sensibilidadGyro = parametros["sensGyro"]
        gUnits = parametros["gUnits"]              # (int) True: unidades en g, False: unidades en m/s2

        # ====== THREADS ======
        print("\n==========================================")
        print("-Prueba nombre: \'" + nameTest + "\', nodo: " + str(NAME_NODE))
        print("-Duracion de prueba (seg): " + str(duration))
        print("-id Frec corte configurado: " + str(numFiltro))
        print("-Unidades \'g\': " + str(gUnits))
        print("===========================================\n")

        self.booleanPort1 = self.scanI2cDevice(PORT1)
        self.booleanPort2 = self.scanI2cDevice(PORT2)

#        if(self.booleanPort1 and self.booleanPort2):
        print("=========== INICIALIZANDO PUERTOS ===========")

        hilo_puerto1 = threading.Thread(target=self.habilitarSensor,
                                        args=(NAME_SENSOR_PORT1,
                                              sensibilidadSensor, numFiltro,
                                              nameTest, duration, frecuencia,
                                              gUnits,sensibilidadGyro,))
#            hilo_puerto2 = threading.Thread(target=self.habilitarSensor,
#                                            args=(NAME_SENSOR_PORT2,
#                                                  sensibilidadSensor, numFiltro,
#                                                  nameTest, duration, frecuencia,
#                                                  gUnits,sensibilidadGyro,))
        hilo_puerto1.start()
#            hilo_puerto2.start()
#        elif(self.booleanPort1):
#            print("=========== INICIALIZANDO PUERTO 1 ===========")
#            self.habilitarSensor(NAME_SENSOR_PORT1, sensibilidadSensor,
#                                 numFiltro, nameTest,
#                                 duration, frecuencia, gUnits, sensibilidadGyro)
#        elif(self.booleanPort2):
#            print("=========== INICIALIZANDO PUERTO 2 ===========")
#            self.habilitarSensor(NAME_SENSOR_PORT2, sensibilidadSensor,
#                                 numFiltro, nameTest,
#                                 duration, frecuencia, gUnits, sensibilidadGyro)
#        else:
#            print("\nError!, No se encuentra sensores conectados")
        return True

#correr = gui()
#correr.runConfigurer()
