# -*- coding: utf-8 -*-


from datosAlmacen import sd_card


#import dispositivo.gy521folder.gy521

from dispositivo.gy521folder.gy521 import gy521

from constantes.const import ADDRESS_REG_accA
from constantes.const import ADDRESS_REG_accB
from constantes.const import I2C_ARM
from constantes.const import I2C_VC

from constantes.const import ACCEL_RANGE_2G
from constantes.const import ACCEL_RANGE_4G
from constantes.const import ACCEL_RANGE_8G
from constantes.const import ACCEL_RANGE_16G

from constantes.const import GRAVEDAD
from constantes.const import TEMP_OUT0

import math
import time
import datetime


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

            self.sensorObject = gy521(self.address, self.bus)
            self.sensorObject.read_gyro_sensibility()

        except IOError:
            print("Error, verifique la conexión de los sensores")

    def getSensorObject(self):
        return self.sensorObject

    def extraerConfiguracionSensor(line):
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
        self.nameTest = NombrePrueba
        self.sensorObject = sensorObject

    def getTime(self):
        dt = datetime.datetime.now()
        return str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)

    def printTable(timeNow, actual_temp, contador, accTotal,
                   inclinacionX, inclinacionY,
                   gyroScaleX, gyroScaleY, gyroScaleZ, accX, accY, accZ,
                   rotX, rotY):

        print(contador,
              ("  %1.2f" % accTotal),
              (" \t%1.2f" % accX), "/", ("%1.2f" % rotX),
              ("%8.2f" % accY), "/", ("%5.2f" % rotY),
              ("%10.2f" % accZ), "/", ("%1.4f" % 0),
              ("\t      %1.2f" % gyroScaleX), ("\t%1.2f" % gyroScaleY),
              ("   %1.2f" % gyroScaleZ),
              "// ", timeNow,
              ("\t%1.2f" % inclinacionX), ("\t%1.2f" % inclinacionY),
              ("\t%1.2f" % actual_temp))

    def calcAceleracionTotal(self, ax, ay, az):
        # para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    def muestra(self, numMuestra):
        # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
        # bus.write_byte_data(address, power_mgmt_1, 0)
        acc = self.sensorObject.get_accel_data() # si no tiene parametros, retorna m/s2
        gyro = self.sensorObject.get_gyro_data()
        
        """Lee la temperatura sobre el sensor gy-521
        Temperatura en grados C
        Rango de temperatura: -40 a 85C.
        # Get the actual temperature using the formule given in the MPU-6050 -
        Register Map and Descriptions revision 4.2, page 30"""
        raw_temp = self.sensorObject.read_i2c_word(TEMP_OUT0)
        tempEscalado = (raw_temp / 340.0) + 36.53

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

        saveTXT(Ax, Ay, Az, time, rotX, rotY, tiltX, TiltY)
        self.printTable(timeNow, tempEscalado, muestra, accTotal,
                        tiltX, tiltY,
                        gx, gy, gz, ax, ay, az,
                        rotX, rotY)

    def TXT(self, nameSensor, ax, ay, az):
        saveMuestra = sd_card(self.nameTest)
        saveMuestra.x.abrirTxt()
        

        txt =str((Ax))+","+str((Ay))+","+str((Az))+"\n"
        txt.close()

# def main():
'''========================        SENSOR 1       ========================
   --------PARAMETROS-------------------------------------------------------'''
namePrueba = "Prueba #1"        # Para almacenar datos en capeta con ese nombre
nombreSensorA = "sensor1"       # nombre sensor
puertoConectado = 1             # 1= 0x68 o 2 = 0x69
sensibilidadSensorA = 4         # sensiblidades 2,4,8,16

sensor1Modulo = modulo(nombreSensorA, puertoConectado)

'''--------CONFIGURACION----------------------------------------------------'''
sensor1 = sensor1Modulo.getSensorObject()
sensor1.read_accel_sensibility()
sensor1Modulo.cambiarSensibilidadAcc(sensibilidadSensorA)
sensor1.read_accel_sensibility()

# configurar offsset
print("\n offset Acc:")
offset_sensor1_Acc = sensor1.get_accel_offset()
print("\n offset Gyro:")
offset_sensor1_Gyro = sensor1.get_gyro_offset()

dirArch = "/home/pi/Desktop/ProyectoPUentes/Analisis_Puentes_Software/configuracionSensorTXT/accelerometro.txt"
leerConfSensor1 = sd_card(nombreSensorA)

configuracion = leerConfSensor1.devolverLineaDePalabraEncontrada("sensor1")
print(configuracion)
#sensor1.set_Offset()

'''==================== HACER PRUEBAS sensor1 ============================='''



# if __name__ == "__main__":
#    main()

# mpu.get_gyro_offset()
# def probando():


#    while(True):
#        accel_data = mpu.get_accel_data(True)  # if = true: "g", else m/s^2
#        print("x: " + str(accel_data['x']) +", y:" + str(accel_data['y']) +"x: " + str(accel_data['z']) )
#        print(accel_data['y'])
#        print("z")
#        print(accel_data['z'])
#
#    print("------CHANGING SENSIBILITY------")
#    mpu.set_accel_sensibility(0x18)
#    print("new sensibility")
#    print(mpu.read_accel_sensibility())
#    accel_data = mpu.get_accel_data(False)# if = true: "g", else m/s^2
#    print("x: ")
#    print(accel_data['x'])
#    print("y: ")
#    print(accel_data['y'])
#    print("z")
#    print(accel_data['z'])
#    print("==============")
#    print("=====FIN======")
#    print("==============")
        
    
