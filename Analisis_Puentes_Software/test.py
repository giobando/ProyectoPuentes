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
            
class test:

    

    
    '''------------------------------------------------------------------------
    los siguiente metodos van dentro de gestor modulo
    ------------------------------------------------------------------------'''
  
    testName = "Prueba"
    bus = 1
    address = 0x68
    sensorName = None
    sensorObject = None

    def __init__(self, nombrePrueba, nombreSensor, numPortAcelerometro, I2C=True):
        '''
        si i2c = true: bus: 1
        si i2c = false: bus: 0
        '''

        try:
            self.testName = nombrePrueba
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
#        line.remove(palabra)
#        line.remove("=")

        # se recibe una lista de palabras, enteoria unavaribles con valores
        # luego se une todo es una sola linea para dividirlo por el =

        numeros = "".join(line).split('=')
        # luego se elimina el nombre de la variable y se deja los numeros
        numeros.pop(0)
#        print(numeros)
        datos = []
        numeros = numeros[0].split(',')
        for numero in numeros:
            datos.append(int(numero))
        print(datos)

    def cambiarSensibilidadAcc(self, sensibilidadNueva, objectoSensor):
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

        objectoSensor.set_accel_sensibility(sensibilidad)


#def main():

'''========PARAMETROS========'''
namePrueba = "Prueba #1"
nombreSensorA = "sensor1"       # nombre sensor
puertoConectado = 1             # 1= 0x68 o 2 = 0x69
sensibilidadSensorA = 2         # sensiblidades 2,4,8,16

sensor1 = test(namePrueba, nombreSensorA, puertoConectado)
sensor1.getSensorObject().read_accel_sensibility()



#    y.read_accel_sensibility()
#    x.cambiarSensibilidadAcc(sensibilidadSensorA, y)
#    y.read_accel_sensibility()

    #dicc = y.get_accel_offset()
    #diccGiro = y.get_gyro_offset()
    #print("offset Acc", dicc['x'], dicc['y'], dicc['z'])
    #print("offset Gyro", diccGiro['x'], diccGiro['y'], diccGiro['z'])
    #

#if __name__ == "__main__":
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
        
    
