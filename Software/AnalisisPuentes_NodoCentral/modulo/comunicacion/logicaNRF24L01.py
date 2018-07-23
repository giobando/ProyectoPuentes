# -*- coding: utf-8 -*-
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
from datetime import datetime
from time import sleep, strftime, time


class logicaNRF24L01:
    # Direccion de canales de nrf24l01:
    pipes = [[0x78, 0x78, 0x78, 0x78, 0x78], [0xb3, 0xb4, 0xb5, 0xb6, 0xF1], [0xcd],[0xa3],[0x0f],[0x05]]

    # Habilitando puertos
    GPIO.setmode(GPIO.BCM)
    spi = spidev.SpiDev()

    # Configurando el NRF24L01
    radio = NRF24(GPIO, spi)
    radio.begin(0, 17)
    radio.setRetries(15,15)             # Numero de intentos y de espera.
    spi.max_speed_hz = 7629
    radio.setPayloadSize(32)            # tamano de los datos a enviar
    radio.setChannel(0x60)              # Recomendado frecuencias entre [70,80]
    radio.setDataRate(NRF24.BR_1MBPS)   # velocidad de la trasmision de datos
    radio.setPALevel(NRF24.PA_MAX)      # Controla la distancia de comunicación

    # ack: forma practica de devolver datos a los remitentes sin cambiar
    # manualmente los modos de radio en ambas unidades.
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()

    # Configurando las direcciones.
    radio.openWritingPipe(pipes[0])     # funcion para el modo recibidor.
    radio.openReadingPipe(0, pipes[0])
    radio.openReadingPipe(1, pipes[1])
    radio.openReadingPipe(2, pipes[2])
    radio.openReadingPipe(3, pipes[3])
    radio.openReadingPipe(4, pipes[4])
    radio.openReadingPipe(5, pipes[5])

    unique_ID = "0_"                    # nombre del nodo
    refreshRate = 30
    WakeUpRetriesCount = 0
    MaxRetriesWakeUp = 2                # Intentos para conectarse.
    NodesUpCount = 0
    NodesUpPipe = []                    # Direcciones de canales activos.
    NodeCount = 1                       # Cantidad de canales activos.
    exists_flag = 0
    csvHeading = "Timestamp,"
    #reportes_path = '../almacenPruebas/'
    #csvfile_path = reportes_path + str(datetime.now().date()) + '.csv'

    def __init__(self):

        self.radio.printDetails()


    def receiveData(self):
        print("ESPERANDO DATOS...")
        self.radio.startListening()          # Configurando como receptor.

        while not self.radio.available(0):   # Verificando que si no hay datos.
            sleep(1.0 / 100)

        receivedMessage = []
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())

#        print("Datos recibidos, traduciendo...")
        string = ""
        for n in receivedMessage:            # Decoficación de msj recibido.
            if (n >= 32 and n <= 126):
                string += chr(n)
        print("EL mensaje recibido fue: {} \n".format(string))
        self.radio.stopListening()           # Configurando como transmisor.
        return string

    def buscarNodosActivos(self):
        print ("\n\n===========================================\n"+
               "        BUSCANDO NODOS DISPONIBLES"+
               "\n============================================")
        nodoEncontrado = False

        for pipeCount in range(0, len(self.pipes)-1):
            WakeUpRetriesCount = 0
            self.radio.openWritingPipe(self.pipes[pipeCount])
            print("\n------------>Abriendo canal de transmision<------------")
            self.radio.print_address_register("TX_ADDR", NRF24.TX_ADDR)
            print("Enviando comando de conexion: HEY_LISTEN")

            while (WakeUpRetriesCount <= self.MaxRetriesWakeUp):
                self.radio.write(list("HEY_LISTEN"))

                # Determina si un ack fue recibido en la ultima llamada.
                if(self.radio.isAckPayloadAvailable()):
                    returnedPL = []
                    self.radio.read(returnedPL, self.radio.getDynamicPayloadSize())
                    print("\tNODO ENCONTRADO! \n     Los datos recibidos son: {} ".format(returnedPL))
                    self.NodesUpPipe.append(self.pipes[pipeCount])
                    self.NodesUpCount += 1
                    nodoEncontrado = True
                    break
                else:
                    if WakeUpRetriesCount == self.MaxRetriesWakeUp:
                        print("Nodo no encontrado.")
                    WakeUpRetriesCount += 1
                    sleep(1)

        print("\n  BUSQUEDA FINALIZADA. Nodos activos {0}".format( str( self.NodesUpCount)))
        return nodoEncontrado

    #print("Tiempo de retardo: {}".format(str(delay)))
    #
    #if (os.path.isfile(str(csvfile_path))):
    #    exists_flag = 1
    #    print("El archivo ya existe!")
    #else:Aaaaaaa
    #    print("Archivo inexistente!")
    #    print("Creando archivo nuevo")

    #while (NodeCount <= NodesUpCount):
    #    if NodeCount == NodesUpCount:
    #        csvHeading = csvHeading+"Sensor"+str(NodeCount)+"\n"
    #    else:
    #        csvHeading = csvHeading+"Sensor"+str(NodeCount)+","
    #    NodeCount += 1

    def conectar(self):

        if(not self.buscarNodosActivos()):
            print("Verifique nodos y vuelvalo a intentar.")
    #    with open(csvfile_path, 'a') as csvfile:
    #        if (exists_flag == 0):
    #            csvfile.write(csvHeading)
        else:
            print ("\n\n==============================================\n"+
                   "         Iniciando Toma de Datos"+
                   "\n==============================================")

            while(True):
                command = "GET_DATA"
                for pipeCount in range(0, self.NodesUpCount):
                    self.radio.openWritingPipe(self.NodesUpPipe[pipeCount])
                    self.radio.write(list(command))

                    print("Enviando comando para recibir datos: {}".format(command))
                    if self.radio.isAckPayloadAvailable():
                        returnedPL = []
                        self.radio.read(returnedPL, self.radio.getDynamicPayloadSize)
                        print("Recibido: {}".format(returnedPL))
                        message = self.receiveData()
                        #crear array para escribir, escribir al final del ciclo de nodos
        #                csvfile_stream = str(datetime.now())+","+str(message)
        #                print(csvfile_stream)

                        #csvfile.write( "{0}, {1}\n".format( str(datetime.now()), str(message)))
                    else:
                        print("No se recibieron datos\n")
        #            sleep(delay)
#                print("DEBUG: final del ciclo\n")
                sleep(1)

#if __name__ == "__main__":
#	main()

x = logicaNRF24L01()
x.conectar()
