# -*- coding: utf-8 -*-
from __future__ import division

# import os, sys, inspect
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)

import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev
from datetime import datetime
from time import sleep, time
from modulo.nodo import nodo
#GPIO.setwarnings(False)
import logging
import csv

from constantes.const import COMMAND_CONEXION_NRF24L01
from constantes.const import COMMAND_RECEIVEDATA

class logicaNRF24L01:
    GPIO.setmode(GPIO.BCM)
    pipes = [[0x78, 0x78, 0x78, 0x78, 0x78],
             [0xb3, 0xb4, 0xb5, 0xb6, 0xF1],
             [0xcd] , [0xa3]] #,[0x0f],[0x05]]
    spi = spidev.SpiDev()          # Habilitando puertos

    GPIO.setwarnings(False)
    radio = NRF24(GPIO, spi)
    radio.begin(0, 17)
    radio.setRetries(11, 15)       # Numero de intentos y de espera.
    spi.max_speed_hz = 15200
    radio.setPayloadSize(32)       # tamano de los datos a enviar
    radio.setChannel(0x76)         # Recomendado frecuencias entre [70,80]

    radio.setDataRate(NRF24.BR_1MBPS) #BR_250KBPS)  # velocidad de la trasmision de datos
    radio.setPALevel(NRF24.PA_MIN)      # Para la distancia de comunicación

    ''' ack: forma practica de devolver datos a los remitentes sin cambiar
    manualmente los modos de radio en ambas unidades.'''
    radio.setAutoAck(True)
    radio.enableDynamicPayloads()
    radio.enableAckPayload()
#    sleep(0.1)
    radio.openWritingPipe(pipes[0])    # Configurando las direcciones.
    radio.openReadingPipe(0, pipes[0])
    radio.openReadingPipe(1, pipes[1])
    radio.openReadingPipe(2, pipes[2])
#    radio.openReadingPipe(3, pipes[3])
#    radio.openReadingPipe(4, pipes[4])
#    radio.openReadingPipe(5, pipes[5])

    unique_ID = "0"                    # nombre del nodo
    refreshRate = 30
    WakeUpRetriesCount = 0
    MaxRetriesWakeUp = 4                # Intentos para conectarse.
    NodeCount = 1                       # Cantidad de canales activos.
    exists_flag = 0
#    csvHeading = "Timestamp,"
#    reportes_path = '../almacenPruebas/'
#    csvfile_path = reportes_path + str(datetime.now().date()) + '.csv'
    estado = ""

    # nodos Encontrados
    NodesUpCount = 0
    NodesUpPipe = []                    # Direcciones de canales activos.
    nodosEncontrados = False
    listNodosObject = None

    def __init__(self):
        self.radio.printDetails()

    def millis(self):
        return int(round(time() * 1000))

    def traducirMsj(self, msjUnicode):
        msj = ""
        for n in msjUnicode:
            if ((n >= 32) and (n <= 126)):
                msj += chr(n)
        return msj

    def sendComando(self, commando):
        self.radio.stopListening()
        sleep(1.0/300)
        message = list(commando)
        self.radio.write(message)
        print("comando enviado")
        self.radio.startListening()

    def esperarDatos(self):
        self.radio.startListening()
        startTime = self.millis()
        msgArrived = False
        timeOut = False
        # repetir hasta que se reciba datos
        while (not self.radio.available(0)) and (not timeOut):
            if((self.millis()-startTime) > 1500):
                timeOut = True
        if timeOut:
            print("ED. Fallo, no se recibio nada.")
        else:
            msgArrived = True
        return msgArrived

    def receiveData(self):
        string = ""
        ackPL = [1]
        receivedMessage = []
        if(self.esperarDatos()):
            self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
            self.radio.testRPD()
            string = self.traducirMsj(receivedMessage)
            self.radio.writeAckPayload(1, ackPL, len(ackPL))
        else:
            print("RD.No se recibio ningun comando")
        return string

    def recibirMedicion(self):
        receivedMessage = []
        ackPL = [1]
        result = None
        print("ESPERANDO DATOS...")
        if(self.esperarDatos()):
            self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
            self.radio.testRPD()
            string = self.traducirMsj(receivedMessage)
            if(string != ''):
                self.radio.writeAckPayload(1, ackPL, len(ackPL))
                parametro = string[:6]      # parametros recibidos
                datos = string[6:]          # Mediciones recibidas
                print("datos>>", datos)
                datoEjeY1, datoEjeY2, datoEjeX = datos.split(";")

                result = {"nodoID": parametro[0],
                          "sensor": parametro[1],
                          "medicion": parametro[2],
                          parametro[3]: datoEjeY1,   # valor 1 en eje y
                          parametro[4]: datoEjeY2,   # valor 2 en eje y
                          parametro[5]: datoEjeX}    # valor en eje x.
            else:
                print("RM.Dato no recibido. fin")
        return result

    def buscarNodosActivos(self, progressBar):
        self.listNodosObject = []
        self.NodesUpCount = 0
        mgs = "\n\n=========================================="
        mgs += "\n         BUSCANDO NODOS DISPONIBLES"
        mgs += "\n============================================"
        print(mgs)

        totalCanales = len(self.pipes)-1
        for pipeCount in range(0, totalCanales):
            WakeUpRetriesCount = 0
            self.radio.openWritingPipe(self.pipes[pipeCount])

            print("\n------------>Abriendo canal de transmision<------------")
            self.radio.print_address_register("TX_ADDR", NRF24.TX_ADDR)
            porcentajeProgreso = (pipeCount+1)*100 / totalCanales  # Interfaz
            progressBar.setValue(porcentajeProgreso)

            print("Enviando comando de conexion: HEY_LISTEN")
            while (WakeUpRetriesCount <= self.MaxRetriesWakeUp):
                self.radio.write(list(COMMAND_CONEXION_NRF24L01))
                if(self.radio.isAckPayloadAvailable()):  # si se recibio msj
                    print("\n\tNODO ENCONTRADO!  ")
                    returnedPL = []
                    self.radio.read(returnedPL,
                                    self.radio.getDynamicPayloadSize)
                    msgActivo = self.receiveData()
                    address_activo = self.pipes[pipeCount]
                    Id_activo = msgActivo[0]

                    nodoNuevo = nodo(Id_activo, address_activo)
                    self.listNodosObject.append(nodoNuevo)
                    self.NodesUpPipe.append(address_activo)
                    self.NodesUpCount += 1
                    self.nodosEncontrados = True
                    break
                else:
                    if WakeUpRetriesCount == self.MaxRetriesWakeUp:
                        print("\n\tNodo no encontrado.")
                    WakeUpRetriesCount += 1
                    sleep(0.2)  # tiempo q tarda en buscar el mismo nodo
        print("\n===================================================")
        msg = "\n  CONCLUIDO. Nodos Activos: "
        self.estado = msg + "{0}".format(str(self.NodesUpCount))
        print(self.estado)
        return self.nodosEncontrados

    def get_listNodosObjectActivos(self):
        return self.listNodosObject

    # define la cantidad de caracteres de un numero
    def trunk(self, numero, enteros, decimales):
        enteros = enteros + decimales  # cantidad de enteros
#        string = "%"+str(enteros)+"."+str(decimales)+"f"
        string = "%."+str(decimales)+"f"
        string = string % float(numero)
        string = str(string).zfill(enteros)
        return string

    """Coloca la misma cantidad de digitos a cada parametro para enviar"""
    def prepararParametros(self, parametros):
        # 300,1/0,240,1000,1/0, 2/4/8/1, 1/2/3/4 ]
        # self.trunk(parametros["durac"], 3, 0)           # 3 caracters
        durac = parametros["durac"]
        filtro = parametros["filtro"]                           # boolean
        frecCorte = self.trunk(parametros["frecCorte"], 3, 0)   # 4 caracters
        gUnits = parametros["gUnits"]
        sensibAcc = self.trunk(parametros["sensAcc"], 2, 0)     # 1 caracters
        sensiGyro = self.trunk(parametros["sensGyro"], 3, 0)    # 1 caracters
        nameTest = parametros["nameT"]

        if(filtro):
            filtro = '1'
            frecMuestreo = str(parametros["fMuestOn"])
        else:
            filtro = '0'
            frecMuestreo = str(parametros["fMuestOff"])
        frecMuestreo = self.trunk(frecMuestreo, 4, 0)

        if(gUnits):
            gUnits = '1'
        else:
            gUnits = '0'

        durac = self.trunk(durac, 3, 0)
        # se cambia para disminuir la cantidad de caracteres a enviar.
        if(sensiGyro == "250"):
            sensiGyro = str(1)
        elif(sensiGyro == "500"):
            sensiGyro = str(2)
        elif(sensiGyro == "1000"):
            sensiGyro = str(3)
        else:
            sensiGyro = str(4)
#        total = len(durac) + 1 + len(frecCorte)
#        total += len(frecMuestreo)+1+len(sensibAcc)
#        total += len(sensiGyro) + len(nameTest)
        x = [durac, filtro, frecCorte, frecMuestreo, gUnits, sensibAcc,
             sensiGyro, nameTest]
        print(x)
#        print(x, "total", total) # total de caracteres
        return x

    def solicitarDatos(self, parametrosDicc):
        if(self.nodosEncontrados):
            msg = "\n\n==============================================\n"
            msg += "         Iniciando Toma de Datos"
            msg += "\n=============================================="
            print(msg)
            # system config:
            parametros = self.prepararParametros(parametrosDicc)
            print("Parametros:",parametros)
            while(True):
                command = COMMAND_CONEXION_NRF24L01
                # se solicita datos a todos los nodos
                for pipeCount in range(0, self.NodesUpCount):
                    self.radio.openWritingPipe(self.NodesUpPipe[pipeCount])
                    self.radio.stopListening() # probar si esto se necesita
                    self.radio.write(list(command))
                    self.radio.write(list(parametros))
                    msg = "Enviando comando para recibir datos: {}"
                    if self.radio.isAckPayloadAvailable():
                        message = self.recibirMedicion()
                        print("recibido: ", message)
                        # crear array para escribir al final del ciclo de nodos
                        #csvfile_stream = str(datetime.now())+","+str(message)
                        #print(csvfile_stream)
                        # csvfile.write("{0},{1}\n".format( str(datetime.now()), str(message)))
                    else:
                        print("No se recibieron datos en 'solicitar datos'\n")
#                    delay = 3 * refreshRate
#                    sleep(delay)
                    print("DEBUG: final del ciclo en 'solicitar datos'\n")
#                sleep(1.0/2)  # tiempo de demora para buscar otro nodo.
        else:
            self.estado = "No hay nodos conectados"
            print(self.estado)

    def get_Estado(self):
        return self.estado
