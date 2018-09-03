# -*- coding: utf-8 -*-
from __future__ import division

import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev
import logging
import csv
##import Adafruit_ADS1x15
from datetime import datetime
from time import sleep, strftime, time

GPIO.setmode(GPIO.BCM)
pipes = [[0x78, 0x78, 0x78, 0x78, 0x78], [0xb3, 0xb4, 0xb5, 0xb6, 0xF1], [0xcd], [0xa3], [0x0f], [0x05]]

spi = spidev.SpiDev()

radio = NRF24(GPIO, spi)
radio.begin(0, 17)
radio.setRetries(15,5)
spi.max_speed_hz = 15200
radio.setPayloadSize(32)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_250KBPS)
radio.setPALevel(NRF24.PA_HIGH)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[1])

radio.printDetails()
radio.startListening()

unique_ID = "3"

exists_flag = 0

csvHeading = "Timestamp,"
reportes_path = '../reportes/'
csvfile_path = reportes_path + str(datetime.now().date()) + '_Sensor1.csv'

################# ADC Setup #################
##adc_input = Adafruit_ADS1x15.ADS1115()
##GAIN = 1
START = 1
def readSensor():
    flex = 0.19238  # adc_input.read_adc_difference(0, gain=GAIN)
    return str(flex)

def sendData(ID, value):
    radio.stopListening()
    sleep(1.0/300)
    message = list(ID + str(value) )
    print("Iniciando envio de datos.")
    radio.write(message)
    print("Datos enviados")
    radio.startListening()

# Redondea a 4 decimales!!
def trunk(dato):
    return "{f:.4f}".format(f=dato)

def sendMedicion(ID, value):    # value[sensor, tipoMedicion, eje1,eje2,t/f, dato1, dato2, tiempo]
    radio.stopListening()
    sleep(1.0/300)

    nodo = ID
    sensor = value[0]           # 1 o 2
    tipoMedicion = value[1]     # "a" # aceleracion
    nameEje1 = value[2]         # "x"
    nameEje2 = value[3]         # "y"
    nameEjeX = value[4]         # "t (tiempo), f (frecuencia)"

    # eliminamos unos decimales
    print("dato 1, dato 2:", value[5], value[6])
    print("timepo:", value[7])
    dataEje1 = trunk(value[5])
    dataEje2 = trunk(value[6])
##    print("truck>>> dato 1, dato 2:", dataEje1, dataEje2)
    time = trunk(value[7])

    message = list(nodo+ sensor + tipoMedicion + nameEje1 + nameEje2 +nameEjeX+ dataEje1+ ',' + dataEje2 + ',' + time)
    print("Iniciando envio de datos."+str(message))
    radio.write(message)
    print("Datos enviados")
    radio.startListening()

if (os.path.isfile(str(csvfile_path))):
    exists_flag = 1
    print("El archivo ya existe!")
else:
    exists_flag= 0
    print("Archivo inexistente!")
    print("direcion", csvfile_path)
##    archivo=open(csvfile_path,"w")
##    archivo.close()
    print("Creando archivo nuevo")

#with open(csvfile_path, 'a') as csvfile:
if(True):
    if (exists_flag == 0):
        pass
#        csvfile.write("timestamp,Sensor\n")
    while(START):
        ackPL = [1]
        radio.writeAckPayload(1, ackPL, len(ackPL))
        print("Enviando ACK")
        receivedMessage = []
        while not radio.available(0):
            sleep(1.0 / 2)
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        print("Recibido: {}".format(receivedMessage))

        print("Traduciendo el mensaje recibido...")
        string = ""
        for n in receivedMessage:
            # Decode into standard unicode set
            if (n >= 32 and n <= 126):
                string += chr(n)
        print(string)

        # We want to react to the command from the master.
        command = string
        if command == "GET_DATA":
            print("Solicitud de datos recibida")
            flex = readSensor()
##            sendData(unique_ID, flex)
            sendMedicion(unique_ID, ['2', 'a','x','y','t',0.1234567,23.123456789,300.123456789])
            csvfile.write(str(datetime.now())+","+str(flex)+"\n")
            #START = 0
        elif command == "HEY_LISTEN":
            print("Secuencia de autoconfiguracion")
            sendData(unique_ID,"-ALIVE")
        command = ""
        radio.writeAckPayload(1, ackPL, len(ackPL))
        print("Cargando respuesta de carga {}".format(ackPL))


