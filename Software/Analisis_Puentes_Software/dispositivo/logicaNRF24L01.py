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

GPIO.setmode(GPIO.BCM)
pipes = [[0x78, 0x78, 0x78, 0x78, 0x78], [0xb3, 0xb4, 0xb5, 0xb6, 0xF1], [0xcd], [0xa3], [0x0f], [0x05]]

spi = spidev.SpiDev()

radio = NRF24(GPIO, spi)
radio.begin(0, 17)
radio.setRetries(15, 15)

spi.max_speed_hz = 7629
radio.setPayloadSize(32)
radio.setChannel(0x60)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MAX)
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()

radio.openWritingPipe(pipes[1])
radio.openReadingPipe(1, pipes[1])

radio.printDetails()
radio.startListening()

unique_ID = "1_"

exists_flag = 0

csvHeading = "Timestamp,"
#reportes_path = '../AlmacenPruebas/'
#csvfile_path = reportes_path + str(datetime.now().date()) + '_Sensor1.csv'

################# ADC Setup #################
##adc_input = Adafruit_ADS1x15.ADS1115()
##GAIN = 1
START = 1
def readSensor():
    flex = 12345  # adc_input.read_adc_difference(0, gain=GAIN)
    return str(flex)

def sendData(ID, value):
    radio.stopListening()               # Configurando como transmisor.
    sleep(1.0/300)
    message = list(ID) + list(value)

#    print("Iniciando envio de datos.")
    radio.write(message)

    print("Datos enviados")
    radio.startListening()              # Configurando como receptor.

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

print ("\n\n============================================\n"+
       "           CONEXION A NODO CENTRAL"+
       "\n============================================")
while(START):
    ackPL = [1]
    radio.writeAckPayload(1, ackPL, len(ackPL))
    print("\nEspere, enviando ACK")
    receivedMessage = []

    while not radio.available(0):   # VERIFICA QUE NO HAYA DATOS.
        sleep(1.0 / 100)

    radio.read(receivedMessage, radio.getDynamicPayloadSize())
#    print("Se recibio respuesta, traduciendo: {}".format(receivedMessage))
    string = ""
    for n in receivedMessage:        # Decode into standard unicode set
        if (n >= 32 and n <= 126):
            string += chr(n)

    print("Comando recibido: " + string +", procesando...")
    command = string
    if command == "GET_DATA":       # Comando recibido del master.
        print("=====> Comando de envio de datos ")
        flex = readSensor()
        sendData(unique_ID, flex)
#        csvfile.write(str(datetime.now())+","+str(flex)+"\n")
        START = 0
    elif command == "HEY_LISTEN":
        print("=====> Comando de conexion al nodo central ")
        sendData(unique_ID,"ALIVE")
    command = ""
    radio.writeAckPayload(1, ackPL, len(ackPL))
    print("Cargando respuesta de carga {}".format(ackPL))
