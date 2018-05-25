# -*- coding: utf-8 -*-
from dispositivo.gy521folder.gy521 import gy521
from datosAlmacen.sd_card import sd_card
from presentacion.grafica import grafica



from constantes.const import ADDRESS_REG_accA
from constantes.const import ADDRESS_REG_accB
from constantes.const import I2C_ARM
from constantes.const import I2C_VC

from constantes.const import ACCEL_RANGE_2G
from constantes.const import ACCEL_RANGE_4G
from constantes.const import ACCEL_RANGE_8G
from constantes.const import ACCEL_RANGE_16G

from constantes.const import TEMP_OUT0

import math
import time
import datetime

# esto es solo para las pruebas!!!
import threading

class modulo:

    '''------------------------------------------------------------------------
    los siguiente metodos van dentro de gestor modulo
    ------------------------------------------------------------------------'''

    bus = 1
    address = 0x68
    sensorName = None
    sensorObject = None

    def __init__(self, nombreSensor, numPortAcelerometro, I2C=True):
        '''
        si i2c = true: bus: 1
        si i2c = false: bus: 0
        '''

        try:
            self.sensorName = nombreSensor

            if(numPortAcelerometro == 1):
                self.address = ADDRESS_REG_accA
            elif numPortAcelerometro == 2:
                self.address = ADDRESS_REG_accB
            else:
                print("Lo siento, de momento solo se puede conectar como \n" +
                      "maximo 2 acelerómetro por puerto I2C")
            if I2C:
                self.bus = I2C_ARM
            else:
                self.bus = I2C_VC

            self.sensorObject = gy521(self.address, self.bus, nombreSensor)
#            self.sensorObject.read_gyro_sensibility()

        except IOError:
            print("Error, verifique la conexión de los sensores")

    def getSensorObject(self):
        return self.sensorObject

    def extraerConfiguracionSensor(self, line):
        # se recibe una lista de palabras, enteoria unavaribles con valores
        # luego se une todo es una sola linea para dividirlo por el =
        numeros = "".join(line).split('=')

        # Se elimina el nombre de la variable y se deja los numeros
        numeros.pop(0)

        datos = []
        numeros = numeros[0].split(',')
        for numero in numeros:
            datos.append(int(numero))
        print(datos)
        return datos

    def cambiarSensibilidadAcc(self, sensibilidadNueva):
        sensibilidad = 0x00

        if (sensibilidadNueva == 2):
            sensibilidad = ACCEL_RANGE_2G
        elif (sensibilidadNueva == 4):
            sensibilidad = ACCEL_RANGE_4G
        elif (sensibilidadNueva == 8):
            sensibilidad = ACCEL_RANGE_8G
        elif (sensibilidadNueva == 16):
            sensibilidad = ACCEL_RANGE_16G
        else:
            print("sensiblidad fuera de rango\n limitese a 2,4,8,16 g")

        self.sensorObject.set_accel_sensibility(sensibilidad)


class test:

    sensorObject = None
    nameTest = None

    def __init__(self, nombrePrueba, sensorObject):
        # ya debe de estar inicializado el sensor
        self.nameTest = nombrePrueba
        self.sensorObject = sensorObject

    def getTime(self):
        dt = datetime.datetime.now()
        return str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)

    def printTable(self, timeNow, actual_temp, contador, accTotal,
                   inclinacionX, inclinacionY,
                   gyroScaleX, gyroScaleY, gyroScaleZ, accX, accY, accZ,
                   rotX, rotY):

        print(contador, self.sensorObject.sensorName,
              (" %10.2f" % accTotal),
              (" %6.2f" % accX), ("%1.2f" % rotX),
              ("%7.2f" % accY), ("%5.2f" % rotY),
              ("%8.2f" % accZ), ("%1.0f" % 0),
              ("      %5.2f" % gyroScaleX), (" %1.2f" % gyroScaleY),
              (" %1.2f" % gyroScaleZ),
              timeNow,
              ("%1.2f" % inclinacionX), ("%1.2f" % inclinacionY),
              ("%1.2f" % actual_temp))

    def calcAceleracionTotal(self, ax, ay, az):
        # para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    def muestra(self, numMuestra, gUnits=True, saveSample=False):
        # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
        # bus.write_byte_data(address, power_mgmt_1, 0)
        acc = self.sensorObject.get_accel_data(gUnits) # si no tiene parametros, retorna m/s2
        gyro = self.sensorObject.get_gyro_data()

        """Lee la temperatura sobre el sensor gy-521
        Temperatura en grados C
        Rango de temperatura: -40 a 85C.
        # Get the actual temperature using the formule given in the MPU-6050 -
        Register Map and Descriptions revision 4.2, page 30"""
        raw_temp = self.sensorObject.read_i2c_word(TEMP_OUT0)
        tempEscalado = (raw_temp / 340.0) + 36.53

        ''' SAMPLES '''
        ax = acc['x']
        ay = acc['y']
        az = acc['z']
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']

        '''ROTACION no importa en que unidades se trabaja, da el mismo valor'''
        rotX = self.sensorObject.get_x_rotation(ax, ay, az)
        rotY = self.sensorObject.get_y_rotation(ax, ay, az)
        # no se puede calcular el angulo en Z. https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

        ''' INCLINACION'''
        tiltX = self.sensorObject.get_x_Tilt(ax, ay, az)
        tiltY = self.sensorObject.get_y_Tilt(ax, ay, az)

        accTotal = self.calcAceleracionTotal(ax, ay, az)
        timeNow = self.getTime()

        if(saveSample):
            self.saveTXT(ax, ay, az, time, rotX, rotY, tiltX, tiltY)

#        self.printTable(timeNow, tempEscalado, numMuestra, accTotal,
#                        tiltX, tiltY,
#                        gx, gy, gz, ax, ay, az,
#                        rotX, rotY)

    def saveTXT(self, ax, ay, az, timeNow, rotX, rotY, tiltX, tiltY):
        saveMuestra = sd_card(self.sensorObject.sensorName)

        # creando carpeta
        carpetaNueva = self.nameTest
        direcCarpeta = "../Analisis_Puentes_Software/AlmacenPruebas/"
        saveMuestra.crearCarpeta(direcCarpeta + carpetaNueva)

        # guarda archivos
        arch_Acc = direcCarpeta +self.nameTest +"/"+self.sensorObject.sensorName +"_Aceleracion.txt"
        saveMuestra = sd_card(arch_Acc)

        txt_acc = ""
        txt_acc = str(ax) + "," + str(ay) + "," + str(az) + "\n"
        saveMuestra.escribir(txt_acc)
        saveMuestra.cerrar()

        arch_Gyro = direcCarpeta +self.nameTest +"/"+self.sensorObject.sensorName +"_Gyro.txt"
        saveMuestra = sd_card(arch_Gyro)

        txt_gyro = ""
        txt_gyro = txt_gyro + str(rotX) + "," + str(rotY) + ","
        txt_gyro = txt_gyro +  str(tiltX) + "," + str(tiltY)
        txt_gyro = txt_gyro +  "l" + ","
        txt_gyro = txt_gyro +  "\n"

        saveMuestra.escribir(txt_acc)
        saveMuestra.cerrar()


def printHeader():
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro\t\t\t\t\t\t\t  ||\t\t\t  Gyroscopio \t\t\t\t\t   |"
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"
    print "|(#) \t   \t\t(g-m/s2)    (g-m/s2) (degree)\t    (g-m/s2) (degree)    (g-m/s2)  \t  ||   \t\t\t\t"+u'\u00b0'+ "/s"+"      \t\t   \t"+ u'\u00b0'+"\t   |"
    print "|contador   sensor \tg_total\t X_out / rotacX\t      Y_out / rotac \tZ_out / rotacZ \t\t  ||   X_out\tY_out \t Z_out \t  Time   |" +"Inclicacion x/y\t temp"
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"


def graficar(nombreSensor, nombrePrueba):
    from presentacion.grafica import grafica
    # los graficos no se pueden leer junto con el codigo en esta aplicacion
    grafico_sensor1 = grafica() #"Prueba #1", "sensor1")
#    grafico_sensor1.start(45)   # recibe milisegundos

def tomarMuestras(sensorTest,gUnits=True, save=True):
    contadorMuestras = 0
    while(1):
        sensorTest.muestra(contadorMuestras, gUnits, save)
        contadorMuestras += 1
        
def main():
    '''========================        SENSOR 1       ========================
       --------PARAMETROS-------------------------------------------------------'''
    namePrueba = "Prueba #1"        # Para almacenar datos en capeta con ese nombre
    nombreSensorA = "sensor1"       # nombre sensor
    puertoConectado = 1             # 1= 0x68 o 2 = 0x69
    sensibilidadSensorA = 16         # sensiblidades 2,4,8,16
    
    sensor1Modulo = modulo(nombreSensorA, puertoConectado)
    
    '''--------CONFIGURACION----------------------------------------------------'''
    # sensibilidad
    sensor1 = sensor1Modulo.getSensorObject()
    sensor1.read_accel_sensibility()
    sensor1Modulo.cambiarSensibilidadAcc(sensibilidadSensorA)
    sensor1.read_accel_sensibility()
    
    # ------ Configurar offsset x medio de txt ------------
    print("\n offset Acc:")
    sensor1.get_accel_offset()
    print("\n offset Gyro:")
    sensor1.get_gyro_offset()
    
    # lectura de archivos
    archivo = "/home/pi/Desktop/ProyectoPUentes/Analisis_Puentes_Software/configuracionSensorTXT/accelerometro.txt"
    leerConfSensor1 = sd_card(archivo)
    leerConfSensor1.abrirTxt()

    # busqueda del nombre del sensor
    configSensor1 = leerConfSensor1.devolverLineaDePalabraEncontrada("sensor1")
    print("offset encontrdos", configSensor1)
    leerConfSensor1.cerrar()

    offset_to_sensor1 = sensor1Modulo.extraerConfiguracionSensor(configSensor1)
    print("offset guardados", offset_to_sensor1)

    # configuracion de los offset
    offset_ax = offset_to_sensor1[0]
    offset_ay = offset_to_sensor1[1]
    offset_az = offset_to_sensor1[2]

    offset_gx = offset_to_sensor1[3]
    offset_gy = offset_to_sensor1[4]
    offset_gz = offset_to_sensor1[5]
    
    sensor1.set_Offset(offset_ax, offset_ay, offset_az,
                       offset_gx, offset_gy, offset_gz)

    print("nuevos offset")
    sensor1.get_accel_offset()
    sensor1.get_gyro_offset()


    '''==================== HACER PRUEBAS sensor1 ============================='''
    testsensor1 = test(namePrueba, sensor1)

    # printHeader()
    '''Primero hacer la primer muestra para generar el archivo
       y poder correr el grafico sin que se caiga
    '''
    testsensor1.muestra(0, True, True)

##    grafico_sensor1 = grafica("Prueba #1", "sensor1", 45,False) #milisengudos
##    t1 = threading.Thread(target=grafica,args=("Prueba #1","sensor1",45,False,))
    
##    t2 = threading.Thread(target=tomarMuestras,args=(testsensor1,True,True,))

##    t1.start()
####    t2.start()
    tomarMuestras(testsensor1,True,True)



if __name__ == "__main__":
    main()

