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
from datetime import datetime
from time import sleep, strftime, time

GPIO.setmode(GPIO.BCM)
pipes = [[0x78, 0x78, 0x78, 0x78, 0x78], [0xb3, 0xb4, 0xb5, 0xb6, 0xF1], [0xcd], [0xa3]] #, [0x0f], [0x05]]

spi = spidev.SpiDev()
GPIO.setwarnings(False)
radio = NRF24(GPIO, spi)
radio.begin(0, 17)
radio.setRetries(11,15)
spi.max_speed_hz = 15200
radio.setPayloadSize(32)
radio.setChannel(0x76)

radio.setDataRate(NRF24.BR_1MBPS)
radio.setPALevel(NRF24.PA_MIN) # PA_HIGH
radio.setAutoAck(True)
radio.enableDynamicPayloads()
radio.enableAckPayload()
##sleep(1.0/10)
radio.openWritingPipe(pipes[0])
radio.openReadingPipe(0, pipes[0])
radio.openReadingPipe(1, pipes[1])
radio.openReadingPipe(2, pipes[2])
##radio.openReadingPipe(3, pipes[3])
##radio.openReadingPipe(4, pipes[4])
##radio.openReadingPipe(5, pipes[5])

radio.printDetails()
##print("channel::::", radio.getChannel())

unique_ID = "0"

refreshRate = 30
WakeUpRetriesCount = 0
MaxRetriesWakeUp = 2
NodesUpCount = 0
NodesUpPipe = []
NodeCount = 1
exists_flag = 0
csvHeading = "Timestamp,"
reportes_path = '../reportes/'
csvfile_path = reportes_path + str(datetime.now().date()) + '.csv'

millis = lambda: int(round(time() * 1000 ))

def esperarDatos():
    radio.startListening()
    startTime = millis()
    msgArrived = False
    timeOut = False
    while (not radio.available(0)) and (not timeOut): # repetir hasta que se reciba datos
        if((millis()-startTime )> 800):            # espera antes de salir
            timeOut = True
    if timeOut:
        print("ED. Fallo, no se recibio nada.")
    else:
##        print("ED. Dato recibido")
        msgArrived = True
    
    return msgArrived
            
def receiveData():
    string = ""
    ackPL = [1]
    receivedMessage = []

    if(esperarDatos()):       
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        radio.testRPD() # SOLO CUANDO SE RECIBE ESTO FUCINOA
        for n in receivedMessage: 
            if ((n >= 32) and (n <= 126)):
                string += chr(n)
        radio.writeAckPayload(1, ackPL, len(ackPL))
    else:
        print("RD.No se recibio ningun comando")   
    return string

def receiveMedicion():
    string = ""
    ackPL = [1]
    receivedMessage = []   
    
    if(esperarDatos()): 
        radio.read(receivedMessage, radio.getDynamicPayloadSize())
        radio.testRPD()
        for n in receivedMessage:
            if ((n >= 32) and (n <= 126)):
                string += chr(n)
        if(string != ''):
            radio.writeAckPayload(1, ackPL, len(ackPL))            
            parametro = string[:6]
            datos =     string[6:]
##            print("RM.parametro", parametro)
##            print("RM.Nodo:"+parametro[0]+", sensor: "+parametro[1] +", medicion: "+parametro[2]+", ejes: "+parametro[3] +","+parametro[4] +": "+parametro[5])
            print("RM.datos", datos)
            a, b, c = datos.split(";")
    ##        print("eje "+parametro[4]+": "+ a+", eje "+parametro[5]+": "+ b+", eje "+parametro[6]+": "+ c)
    else:
        print("RM.Dato no recibido. fin")
    return string

print ("Iniciando secuencia de autoconfiguracion")
for pipeCount in range(0, len(pipes)-1):
    WakeUpRetriesCount = 0
    radio.openWritingPipe(pipes[pipeCount])
    print("\nAbriendo pipes de transmision #"+str(pipeCount+1)+ ", enviando: 'HEY_LISTEN' a:")
    radio.print_address_register("\tTX_ADDR", NRF24.TX_ADDR)
    intentoNum = 1
    while (WakeUpRetriesCount <= MaxRetriesWakeUp):
##        print("\t"+str(intentoNum)+". Enviando mensaje de busqueda: HEY_LISTEN")
        radio.stopListening()
        radio.write(list("HEY_LISTEN"))
        radio.startListening()

        if radio.isAckPayloadAvailable():
            print("Nodo encontrado!")
            returnedPL = []
            radio.read(returnedPL, radio.getDynamicPayloadSize)
##            print("Los datos recibidos son: {} ".format(returnedPL))
            x = receiveData()
            print("Nodo 'alive' num: ", x)
            NodesUpPipe.append(pipes[pipeCount])
            NodesUpCount += 1
            intentoNum = 0
            break                   
        else:            
            intentoNum += 1
            if WakeUpRetriesCount == MaxRetriesWakeUp:
                print("\tNodo no esta activo, intentando en otra tuberia")
            WakeUpRetriesCount += 1
            sleep(0.2) # tiempo espera de un nodo.

delay = 1.0/ (NodesUpCount*refreshRate+1)
print("\nConfiguracion finalizada... {0} Nodos activos".format(str(NodesUpCount)))

if (os.path.isfile(str(csvfile_path))):
    exists_flag = 1
    print("El archivo ya existe!")
else:
    exists_flag= 0
    print("Archivo inexistente!")
    print("Creando archivo nuevo")

while (NodeCount <= NodesUpCount):
    if NodeCount == NodesUpCount:
        csvHeading = csvHeading+"Sensor"+str(NodeCount)+"\n"
    else:
        csvHeading = csvHeading+"Sensor"+str(NodeCount)+","
    NodeCount += 1

def main():
    with open(csvfile_path, 'a') as csvfile:
        if (exists_flag == 0):
##            csvfile.write(csvHeading)
            pass
        print("Iniciando Toma de Datos...")
        while(1):
            command = "GET_DATA"
##            print(str(NodesUpCount)+" nodos")
            for pipeCount in range(0, NodesUpCount):
                radio.openWritingPipe(NodesUpPipe[pipeCount])
                radio.stopListening()
                radio.write(list(command))
##                print("Mensaje enviado: {}".format(list(command)))
                if radio.isAckPayloadAvailable(): #confirmar si se recibio anterior
                    message = receiveMedicion() 
##                    print("mns:" , message)
##                    csvfile_stream = str(datetime.now())+","+str(message)
##          print(csvfile_stream)
##                    csvfile.write("{0};{1}\n".format(str(datetime.now()),str(message)))
##                else: 
                        
##                    csvfile.write("{0}\n".format(str(message)))
##                    print("No se recibieron datos")
##                    sleep(delay) # tiempo entre cada dato recibido
##            print("DEBUG: final del ciclo")
##            sleep(1) # traspaso entre nodos.

if __name__ == "__main__":
    main()
