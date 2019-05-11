
# -*- coding: utf-8 -*-
from constantes.const import ADDRESS_REG_accA
from constantes.const import ADDRESS_REG_accB
from constantes.const import I2C_ARM
from constantes.const import I2C_VC

from dispositivo.gy521folder.mpu6050Hijo import mpu6050Hijo
from dispositivo.gy521folder.calibracion_Gy521 import calibracion_Gy521
'''
iniciliza todos los sensores e indica la cantidad a inicializar
configura addres, calibracion, y toma de datos.
'''

class gestorSensor:

    bus = 1     # 1 si es i2cArm. 0 GPIO
    address = 0x68
    sensorName = None
    sensorObject = None
    sensibility = None
    calibrated = False  # si no se ha calibrado sera siempre False

    def __init__(self, nameSensor, numPortConected, sensibildadAcc, I2C=True):
        '''
        si i2c = true: bus: 1
        si i2c = false: bus: 0
        '''
        print("\nHabilitando el puerto: " + str(nameSensor))
        try:
            self.sensorName = nameSensor
            self.sensibility = sensibildadAcc

            if(numPortConected == 1):           # address = 0x68
                self.address = ADDRESS_REG_accA
            elif numPortConected == 2:          # address = 0x69
                self.address = ADDRESS_REG_accB
            else:
                print("Lo siento, solo se puede conectar como \n" +
                      "maximo 2 acelerómetro por puerto I2C")

            '''siempre sera I2C_arm porque solo hay dos puertos,
            pero si se desea mas de 2 puertos se debe habilitar'''
            if I2C:
                self.bus = I2C_ARM
            else:
                self.bus = I2C_VC

            self.sensorObject = mpu6050Hijo(self.address, self.bus)
            self.sensorObject.set_nameSensor(self.sensorName)

        except IOError:
            print("Error, verifique la conexión de los sensores")

    def calibrarDispositivo(self):
        if(not self.calibrated):
            self.sensorObject.set_sensibilidad_acc(self.sensibility)

            # La calibracion configura automaticamente los offset
            calibrar = calibracion_Gy521(self.sensorObject, self.sensibility)
            calibrar.start(self.sensorName)
            self.calibrated = True

    def getSensorObject(self):
        return self.sensorObject

    '''Indica que ya se realizo una calibracion
    '''
    def get_status_calibration(self):
        return self.calibrated

    '''
    Metodo encargado de leer lineas obtenidas de txt de configuracion parametro
    Recibe: lista de palabras: ['sensor1= 1,2,3,4,5,6]    '''
    def extraerConfiguracionSensor(self, line):
        # se recibe una lista de palabras
        # luego se une todo es una sola linea para eliminar el = y la variable
        numeros = "".join(line).split('=')

        # Se elimina el nombre de la variable y se deja los numeros
        numeros.pop(0)

        datos = []
        numeros = numeros[0].split(',')
        for numero in numeros:
            datos.append(int(numero))
#        print(datos)
        return datos