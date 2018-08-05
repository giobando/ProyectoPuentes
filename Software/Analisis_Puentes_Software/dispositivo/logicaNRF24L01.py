from __future__ import division

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev
#import logging
#import csv
##import Adafruit_ADS1x15
from datetime import datetime
from time import sleep, strftime, time


class logicaNRF24L01:
    GPIO.setmode(GPIO.BCM)
    pipes = [[0x78, 0x78, 0x78, 0x78, 0x78], [0xb3, 0xb4, 0xb5, 0xb6, 0xF1], [0xcd], [0xa3], [0x0f], [0x05]]

    spi = spidev.SpiDev()

    radio = NRF24(GPIO, spi)
    radio.begin(0, 17)
    radio.setRetries(15, 15)
    spi.max_speed_hz = 15200
    radio.setPayloadSize(32)
    radio.setChannel(0x76)
    radio.setDataRate(NRF24.BR_250KBPS)
    radio.setPALevel(NRF24.PA_MAX)
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    radio.openWritingPipe(pipes[1])
    radio.openReadingPipe(1, pipes[1])
    radio.printDetails()
    radio.startListening()

    unique_ID = "2"
    exists_flag = 0
    csvHeading = "Timestamp,"
    #reportes_path = '../AlmacenPruebas/'
    #csvfile_path = reportes_path + str(datetime.now().date()) + '_Sensor1.csv'


    def readSensor(self):
        flex = 0.19238
        return str(flex)

    def sendData(self, ID, value):
        self.radio.stopListening()   # modo trasmisor
        sleep(1.0/300)
        message = list(ID + str(value) )
        print("Iniciando envio de datos.")
        self.radio.write(message)
        print("Datos enviados")
        self.radio.startListening()  # modo receptor

    # Redondea a 4 decimales!!
    def trunk(self, dato):
        return "{f:.4f}".format(f=dato)

    # value[sensor, tipoMedicion, eje1,eje2,t/f, dato1, dato2, tiempo]
    def sendMedicion(self, ID, value):
        # self.unique_ID, ['2', 'a','x','y','t',0.1234567,23.123456789,300.123456789])
        print("=====>GET_DATA: Comando de envio de datos ")
        # flex = readSensor()   PEDIR DATOS
        # csvfile.write(str(datetime.now())+","+str(flex)+"\n")


        self.radio.stopListening()
        sleep(1.0/300)
        nodo = ID
        sensor = value[0]           # 1 o 2
        tipoMedicion = value[1]     # "a" # aceleracion
        nameEje1 = value[2]         # "x"
        nameEje2 = value[3]         # "y"
        nameEjeX = value[4]         # "t (tiempo), f (frecuencia)"

        # redondeamos a 4 decimales
        print("dato 1, dato 2:", value[5], value[6])
        print("timepo:", value[7])
        dataEje1 = self.trunk(value[5])
        dataEje2 = self.trunk(value[6])
        time = self.trunk(value[7])

        message = list(nodo+ sensor + tipoMedicion + nameEje1 + nameEje2 +nameEjeX+ dataEje1+ ',' + dataEje2 + ',' + time)
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

            self.radio.writeAckPayload(1, ackPL, len(ackPL))
            print("\nEspere, enviando ACK.")

            while not self.radio.available(0):   # ESPERANDO QUE LLEGUEN DATOS
                sleep(1.0 / 100)

            self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
            msjTraducido = self.traducirMsj(receivedMessage)







            print("Comando recibido: " + msjTraducido +", procesando...")
            command = msjTraducido
            print("msj traducido (en esperar comando)", command)

            if command == "GET_DATA":       # Comando recibido del master.
                self.sendMedicion(self.unique_ID, ['2', 'a','x','y','t',0.1234567,23.123456789,300.123456789])
                # START = SALIR SI SE RECIBE QUE SE termino pruebas

            elif command == "HEY_LISTEN":
                print ("\n\n CONEXION A NODO CENTRAL. Configurando.... ")
                self.sendData(self.unique_ID,"-ALIVE")

            command = ""
            self.radio.writeAckPayload(1, ackPL, len(ackPL))
            print("Cargando respuesta de carga {}".format(ackPL))

x = logicaNRF24L01()
x.recibir_Comandos()