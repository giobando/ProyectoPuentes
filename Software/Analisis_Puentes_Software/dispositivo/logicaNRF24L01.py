# -*- coding: utf-8 -*-
from __future__ import division

import os
import sys
import inspect
import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev

#current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
#parent_dir = os.path.dirname(current_dir)
#sys.path.insert(0, parent_dir)


#import logging
#import csv
##import Adafruit_ADS1x15
from datetime import datetime
from time import sleep, strftime, time
from constantes.const import IDNODE

class logicaNRF24L01:
    GPIO.setmode(GPIO.BCM)

    # cada lista corresponde a una direccion  de 1 nodo.
    pipes = [[0x78, 0x78, 0x78, 0x78, 0x78],
             [0xb3, 0xb4, 0xb5, 0xb6, 0xF1],
             [0xcd], [0xa3], [0x0f], [0x05]]

    spi = spidev.SpiDev()
    GPIO.setwarnings(False)
    radio = NRF24(GPIO, spi)
    radio.begin(0, 17)
    radio.setRetries(11, 15)
    spi.max_speed_hz = 15200
    radio.setPayloadSize(32)
    radio.setChannel(0x76)

    radio.setDataRate(NRF24.BR_1MBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
#    sleep(0.1)

    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[1])
    sleep(0.1)
    radio.startListening()

    exists_flag = 0
    csvHeading = "Timestamp,"
    # reportes_path = '../AlmacenPruebas/'
    # csvfile_path = reportes_path + str(datetime.now().date()) + '_Sensor1.csv'

    def __init__(self):
        self.radio.printDetails()

    def readSensor(self):
        flex = 0.19238
        return str(flex)

    def sendCommand(self, value):
        self.radio.stopListening()   # modo trasmisor
        sleep(0.25)
        message = list(IDNODE + str(value))
        print("Iniciando envio de comando.")
        self.radio.write(message)
        print("Comando enviado")
        self.radio.startListening()  # modo receptor

    def trunk(self, dato):           # Redondea a 4 decimales!!
        return "{f:.4f}".format(f=dato)

    # value[sensor, tipoMedicion, eje1,eje2,t/f, dato1, dato2, tiempo]
    def sendMedicion(self, value):
#         self.unique_ID, ['2', 'a', 'x', 'y', 't',
#                          0.1234567, 23.123456789, 300.123456789])
        print("=====>GET_DATA: Comando de envio de datos ")
        # flex = readSensor()   PEDIR DATOS
        # csvfile.write(str(datetime.now())+","+str(flex)+"\n")

        self.radio.stopListening()
#        sleep(1.0/300)
        sensor = value[0]           # 1 o 2
        tipoMedicion = value[1]     # "a" # aceleracion
        nameEje1 = value[2]         # "x"
        nameEje2 = value[3]         # "y"
        nameEjeX = value[4]         # "t (tiempo), f (frecuencia)"

#        print("dato 1, dato 2:", value[5], value[6])
#        print("timepo:", value[7])
        dataEje1 = self.trunk(value[5])
        dataEje2 = self.trunk(value[6])
        tiempo = self.trunk(value[7])

        message = list(IDNODE + sensor + tipoMedicion + nameEje1 +
                       nameEje2 + nameEjeX + dataEje1 + ';' +
                       dataEje2 + ';' + tiempo)
        print("Iniciando envio de datos."+str(message))
        self.radio.write(message)
        self.radio.startListening()

#if (os.path.isfile(str(csvfile_path))):
#    exists_flag = 1
#    print("El archivo ya existe!")
#else:
#    exists_flag= 0
#    print("Archivo inexistente!")
#    print("direcion", csvfile_path)
###    archivo=open(csvfile_path,"w")
###    archivo.close()
#    print("Creando archivo nuevo")

#with open(csvfile_path, 'a') as csvfile:
#    if (exists_flag == 0):
#        csvfile.write("timestamp,Sensor\n")

    def traducirMsj(self, msjUnicode):
        msj = ""
        for n in msjUnicode:
            if (n >= 32 and n <= 126):
                msj += chr(n)
        return msj

    def recibir_Comandos(self):
        START = True

        while(START):
            ackPL = [1]
            receivedMessage = []
            self.radio.startListening()

            self.radio.writeAckPayload(1, ackPL, len(ackPL))
            print("\nEspere, enviando ACK.")

            while not self.radio.available(0):   # ESPERAR DATOS
                sleep(0.01)    # REVISAR SI SE CAMBIA EL TIEMPO DE ESPERA

            self.radio.read(receivedMessage,
                            self.radio.getDynamicPayloadSize())
            msjTraducido = self.traducirMsj(receivedMessage)

            print("Comando recibido: " + msjTraducido + ", procesando...")
            command = msjTraducido
            print("msj traducido (en esperar comando)", command)

            if command == "GET_DATA":
                dt = datetime.now()
                minute = dt.minute
                second = dt.second
                self.sendMedicion(['2', 'a', 'x', 'y', 't', 0, minute, second])
                salir = False
                contador = 1
                msg = IDNODE
                msg += ';2;'+ 'a;'+'x;'+'y;'
                msg += 't;' + str(contador)
                msg += ";"+str(self.trunk(minute))
                msg += ";"+str(self.trunk(second))
                csvfile.write(msg+"\n")
    ##            contador += 1
            elif command == "HEY_LISTEN":
                print("\n\n CONEXION A NODO CENTRAL. Configurando.... ")
                self.sendCommand("-ALIVE")

            command = ""
            self.radio.writeAckPayload(1, ackPL, len(ackPL))
            print("Cargando respuesta de carga {}".format(ackPL))


x = logicaNRF24L01()
x.recibir_Comandos()
