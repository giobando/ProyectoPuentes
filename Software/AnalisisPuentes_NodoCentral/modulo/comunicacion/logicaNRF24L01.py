# -*- coding: utf-8 -*-
from __future__ import division

# import os, sys, inspect
# current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# parent_dir = os.path.dirname(current_dir)
# sys.path.insert(0, parent_dir)

import RPi.GPIO as GPIO
from lib.lib_nrf24 import NRF24
import spidev
# from datetime import datetime
from time import sleep, time  # , strftime,
from modulo.nodo import nodo


class logicaNRF24L01:
    # Direccion de canales de nrf24l01:
    pipes = [[0x78, 0x78, 0x78, 0x78, 0x78],
             [0xb3, 0xb4, 0xb5, 0xb6, 0xF1],
             [0xcd],
             [0xa3]]  # ,[0x0f],[0x05]]

    # Habilitando puertos
    GPIO.setmode(GPIO.BCM)
    spi = spidev.SpiDev()

    # Configurando el NRF24L01
    radio = NRF24(GPIO, spi)
    radio.begin(0, 17)
    radio.setRetries(15, 15)             # Numero de intentos y de espera.
    spi.max_speed_hz = 15200
    radio.setPayloadSize(32)            # tamano de los datos a enviar
    radio.setChannel(0x76)              # Recomendado frecuencias entre [70,80]
    radio.setDataRate(NRF24.BR_250KBPS)  # velocidad de la trasmision de datos
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
#    radio.openReadingPipe(4, pipes[4])
#    radio.openReadingPipe(5, pipes[5])

    unique_ID = "0_"                    # nombre del nodo
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

    def traducirMsj(self, msjUnicode):
        msj = ""
        for n in msjUnicode:
            if (n >= 32 and n <= 126):
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
        startTime = int(round(time() * 1000))
        finalTime = startTime
        msgArrived = False

        while not self.radio.available(0):  # esperando datos
            finalTime = finalTime - startTime
            if(finalTime > 200):            # espera 200 ms antes de salir
                ("no se recibieron datos")
                break
            sleep(1.0 / 100)
            finalTime = int(round(time() * 1000))
        return msgArrived

    def receiveData(self):
        print("ESPERANDO DATOS...")
        self.radio.startListening()         # modo receptor.

        self.esperarDatos()

        receivedMessage = []
        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        self.estado = "Datos recibidos, traduciendo..."

        string = self.traducirMsj(receivedMessage)
        print("EL mensaje recibido fue: {} \n".format(string))
        self.radio.stopListening()           # modo transmisor.
        return string

    def recibirMedicion(self):
        receivedMessage = []
        result = None

        print("ESPERANDO DATOS...")
        self.radio.startListening()          # Modo receptor.
        self.esperarDatos()

        self.radio.read(receivedMessage, self.radio.getDynamicPayloadSize())
        string = self.traducirMsj(receivedMessage)
        self.radio.stopListening()  # modo transmisor.

        parametro = string[:7]      # parametros recibidos
        datos = string[7:]          # Mediciones recibidas
        print("datos>>", datos)
        datoEjeY1, datoEjeY2, datoEjeX = datos.split(",")

        result = {"nodoID": parametro[0],
                  "sensor": parametro[2],
                  "medicion": parametro[3],
                  parametro[4]: datoEjeY1,   # valor en eje y
                  parametro[5]: datoEjeY2,   # segundo valor en eje y
                  parametro[6]: datoEjeX     # valor en eje x.
                  }
        return result

    def buscarNodosActivos(self, progressBar):
        self.listNodosObject = []
        self.NodesUpCount = 0
        mgs = "\n\n==========================================\n         "
        mgs += "BUSCANDO NODOS DISPONIBLES"
        mgs += "\n ============================================"
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
                self.radio.write(list("HEY_LISTEN"))
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
                    sleep(1)
        msg = "\n  CONCLUIDO, NODOS ACTIVOS: "
        self.estado = msg + "{0}".format(str(self.NodesUpCount))
        print(self.estado)
        return self.nodosEncontrados

    def get_listNodosObjectActivos(self):
        return self.listNodosObject

    # define la cantidad de caracteres de un numero
    def trunk(self, numero, enteros, decimales):
        enteros = enteros + decimales  # cantidad de enteros
        string = "%"+str(enteros)+"."+str(decimales)+"f"
        string = string % float(numero)
        return string

    """encargado de colocar siempre la misma cantidad de digitos a cada parametro
    para enviarlos"""
    def prepararParametros(self, parametros):
        # 300,1/0,240,1000,1/0, 2/4/8/1, 1/2/3/4 ]
        durac = self.trunk(parametros["durac"], 3, 0)           # 3 caracters
        filtro = parametros["filtro"]                           # boolean
        frecCorte = self.trunk(parametros["frecCorte"], 3, 0)   # 4 caracters
        gUnits = parametros["gUnits"]
        sensibAcc = self.trunk(parametros["sensAcc"], 3, 0)     # 1 caracters
        sensiGyro = self.trunk(parametros["sensGyro"], 3, 0)    # 1 caracters

        if(filtro):
            filtro = 1
            frecMuestreo = str(parametros["fMuestOn"])
        else:
            filtro = 0
            frecMuestreo = str(parametros["fMuestOff"])
        frecMuestreo = self.trunk(frecMuestreo, 4, 0)

        if(gUnits):
            gUnits = 1
        else:
            gUnits = 0

        # se cambia para disminuir la cantidad de caracteres a enviar.
        if(sensiGyro == "250"):
            sensiGyro = 1
        elif(sensiGyro == "500"):
            sensiGyro = 2
        elif(sensiGyro == "1000"):
            sensiGyro = 3
        else:
            sensiGyro = 4

        return [durac, filtro, frecCorte, frecMuestreo, gUnits, sensibAcc,
                sensiGyro]

    def solicitarDatos(self, parametros):
        parametros = self.prepararParametros(parametros)  # system config.

        if(self.nodosEncontrados):
            msg = "\n\n==============================================\n"
            msg += "         Iniciando Toma de Datos"
            msg += "\n=============================================="
            print(msg)
            self.prepararParametros(parametros)
            while(True):
                command = "GET_DATA"
                for pipeCount in range(0, self.NodesUpCount):
                    self.radio.openWritingPipe(self.NodesUpPipe[pipeCount])
                    self.radio.write(list(command))
                    msg = "Enviando comando para recibir datos: {}"
                    print(msg.format(command))
                    if self.radio.isAckPayloadAvailable():
                        returnedPL = []
                        self.radio.read(returnedPL,
                                        self.radio.getDynamicPayloadSize)
                        print("Recibido: {}".format(returnedPL))
                        message = self.receiveData()
                        print("recibido: ", message)
                        # crear array para escribir al final del ciclo de nodos
#                        csvfile_stream = str(datetime.now())+","+str(message)
#                        print(csvfile_stream)
#                         csvfile.write("{0},{1}\n".format( str(datetime.now()), str(message)))
                    else:
                        print("No se recibieron datos - solicitar datos\n")
        #            sleep(delay)
                    print("DEBUG: final del ciclo\n")
                sleep(1)
        else:
            self.estado = "No hay nodos conectados"
            print(self.estado)

    def get_Estado(self):
        return self.estado
