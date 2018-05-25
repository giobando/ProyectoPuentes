# -*- coding: utf-8 -*-

"""This program handles the communication over I2C
between a Raspberry Pi and a MPU-6050 Gyroscope / Accelerometer combo.
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
"""

import smbus
import math
from calibracion_Gy521 import calibracion_Gy521

# -----------------------------------------------------------------------------
#                                CONSTANTES
# -----------------------------------------------------------------------------
# from constantes.const import *
from constantes.const import ACCE_POWER_MGMT_1 as PWR_MGMT_1
# from constantes.const import ACCE_POWER_MGMT_1 as PWR_MGMT_2
from constantes.const import GRAVEDAD as GRAVITIY_MS2

from constantes.MPUConstants import MPUConstants as C

# ---------------ESCABILIDAD ASOCIADA A LA SENSIBILIDAD------------------------
from constantes.const import ACCEL_SCALE_MODIFIER_2G
from constantes.const import ACCEL_SCALE_MODIFIER_4G
from constantes.const import ACCEL_SCALE_MODIFIER_8G
from constantes.const import ACCEL_SCALE_MODIFIER_16G
from constantes.const import GYRO_SCALE_MODIFIER_250DEG
from constantes.const import GYRO_SCALE_MODIFIER_500DEG
from constantes.const import GYRO_SCALE_MODIFIER_1000DEG
from constantes.const import GYRO_SCALE_MODIFIER_2000DEG

# ------------------------------SENSIBILIDAD-----------------------------------
from constantes.const import ACCEL_RANGE_2G
from constantes.const import ACCEL_RANGE_4G
from constantes.const import ACCEL_RANGE_8G
from constantes.const import ACCEL_RANGE_16G
from constantes.const import GYRO_RANGE_250DEG
from constantes.const import GYRO_RANGE_500DEG
from constantes.const import GYRO_RANGE_1000DEG
from constantes.const import GYRO_RANGE_2000DEG

# --------------------------DIRECCION DE SALIDA--------------------------------
from constantes.const import ACCEL_XOUT0
from constantes.const import ACCEL_YOUT0
from constantes.const import ACCEL_ZOUT0
from constantes.const import GYRO_XOUT0
from constantes.const import GYRO_YOUT0
from constantes.const import GYRO_ZOUT0
from constantes.const import TEMP_OUT0

# ----------------------CONFIGURACION ACELETROMETRO----------------------------
from constantes.const import ACCEL_CONFIG
from constantes.const import GYRO_CONFIG

# -----------------------------OFFSETS-----------------------------------------
from constantes.const import ACCEL_XG_OFFS
from constantes.const import ACCEL_YG_OFFS
from constantes.const import ACCEL_ZG_OFFS
from constantes.const import GYRO_XG_OFFS
from constantes.const import GYRO_YG_OFFS
from constantes.const import GYRO_ZG_OFFS

from constantes.const import FREC_CORTE_260_Hz
from constantes.const import FREC_CORTE_184_Hz
from constantes.const import FREC_CORTE_94_Hz
from constantes.const import FREC_CORTE_44_Hz
from constantes.const import FREC_CORTE_21_Hz
from constantes.const import FREC_CORTE_10_Hz
from constantes.const import FREC_CORTE_5_Hz

#from dispositivo.gy521folder.MPU6050Padre import MPU6050Padre
#import MPU6050Padre

from dispositivo.gy521folder.MPU6050Padre import MPU6050Padre
class mpu6050Hijo(MPU6050Padre):
#    address = None
#    mpu = None  # smbus.SMBus(1), it will be assigned in the constructor
#    bus = None
    scaleValue = 1  # depende de la sensibilidad, se escala a este numero
    sensorName = None

#    def __init__(self, address, numbus, name):
#        # numbum = I2C port assigned.
#        self.address = address
#        self.bus = numbus
#        self.mpu = smbus.SMBus(numbus)
#        self.sensorName = name
#
#        # Wake up the MPU-6050 since it starts in sleep mode
#        self.mpu.write_byte_data(self.address, PWR_MGMT_1, 0x00)


    def __init__(self, address, numbus, nameSensor):
        # numbum = I2C port assigned.
        MPU6050Padre.__init__(self, numbus, address)
        self.sensorName = nameSensor

    '''
    CONFIGURACION OFFSET
    '''
    def set_offset(self, ax, ay, az, gx, gy, gz):
        self.set_x_accel_offset(ax)
        self.set_y_accel_offset(ay)
        self.set_z_accel_offset(az)

        self.set_x_gyro_offset(gx)
        self.set_y_gyro_offset(gy)
        self.set_z_gyro_offset(gz)

    '''
    METODO ENCARGADO DE RETORNAR MEDICIONES ACC, GYRO
    retorna raw o unidades en un diccionario
    {'x':x, 'y':y, 'z':z}

    Depende de la sensbilidad aplica factor de escalamiento
    '''
    def get_acc_data(self, gUnit=False):
        # if g is True, return data in g units
        # else in m/s2

        # return accel_range(entero) if parameter is blank
        # return accel_range(register) if parameter is True
        accel_range = self.get_sensiblidad_acc(True)
        factorScale = 1

        # Assigns the correct scability at sensibility
        if accel_range == C.MPU6050_ACCEL_FS_2:
            factorScale = ACCEL_SCALE_MODIFIER_2G

        elif accel_range == C.MPU6050_ACCEL_FS_4:
            factorScale = ACCEL_SCALE_MODIFIER_4G

        elif accel_range == C.MPU6050_ACCEL_FS_8:
            factorScale = ACCEL_SCALE_MODIFIER_8G

        elif accel_range == C.MPU6050_ACCEL_FS_16:
            factorScale = ACCEL_SCALE_MODIFIER_16G

        else:
            print("Unkown range:")
            print("- accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            factorScale = ACCEL_SCALE_MODIFIER_2G

        acc = self.get_acceleration()
        x = acc[0] / factorScale
        y = acc[1] / factorScale
        z = acc[2] / factorScale

        if(gUnit):
            return {'x': x, 'y': y, 'z': z}

        else:
            x = x * GRAVITIY_MS2
            y = y * GRAVITIY_MS2
            z = z * GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}


    def get_gyro_data(self):
        # return accel_range(entero) if parameter is blank
        # return accel_range(register) if parameter is True
        gyro_range = self.get_sensiblidad_gyro(True)
        factorScale = 1

        # Assigns the correct scability at sensibility
        if gyro_range == C.MPU6050_GYRO_FS_250:
            factorScale = GYRO_SCALE_MODIFIER_250DEG

        elif gyro_range == C.MPU6050_GYRO_FS_500:
            factorScale = GYRO_SCALE_MODIFIER_500DEG

        elif gyro_range == C.MPU6050_GYRO_FS_1000:
            factorScale = GYRO_SCALE_MODIFIER_1000DEG

        elif gyro_range == C.MPU6050_GYRO_FS_2000:
            factorScale = GYRO_SCALE_MODIFIER_2000DEG

        else:
            print("Unkown range: ")
            print("gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            factorScale = GYRO_SCALE_MODIFIER_250DEG

        gyro = self.get_rotation()
        x = gyro[0] / factorScale
        y = gyro[1] / factorScale
        z = gyro[2] / factorScale

        return {'x': x, 'y': y, 'z': z}

    '''
    METODO ENCARGADO DE APLICAR FILTRO PASA BAJA
    TOMADO DE: MPU-6000-REGISTER-MAP1, pag 13
     _________________________________________________
     |          |   ACELEROMETRO     |   GYROSCOPIO  |
     |          |      Fs = 1kHz     |               |
     | DLPF_CFG | Bandwidth | Delay  |  Sample Rate  |
     |          |    (Hz)   |  (ms)  |     (KHz)     |
     | ---------+-----------+--------+---------------|
     |   0      |    260    |   0    |   8           |
     |   1      |    184    |  2.0   |   1           |
     |   2      |    94     |  3.0   |   1           |
     |   3      |    44     |  4.9   |   1           |
     |   4      |    21     |  8.5   |   1           |
     |   5      |    10     |  13.8  |   1           |
     |   6      |    5      |  19.0  |   1           |
     |   7      |   -- Reserved --   | Reserved      |
     |__________|____________________|_______________|
    '''
    '''
     METODO ENCARGADO DE CONFIGURAR FRECUENCIA DE CORTE
     RECIBE ENTEROS DE 0 A 6 segun la tabla anterior.
    '''
    def set_filtroPasaBaja(self, frecCorte):
        if (frecCorte == 0):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 1):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 2):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 3):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 4):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 5):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        elif (frecCorte == 6):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)

        else:
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)
            print("filtro fuera de rango, se desactiva")

    '''
    Metodo encargado de cambiar la sensiblidad del giroscopio
    Recibe enteros:
        250:  Sensibilidad 250 grados/segundo
        500:  Sensibilidad 500 grados/segundo
        1000: Sensibilidad 1000 grados/segundo
        2000: Sensibilidad 2000 grados/segundo
    '''
    import time
    def set_sensibilidad_gyro(self, sensibilidad):
        if(sensibilidad == 250):
            print('entro1')
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_250)

        elif(sensibilidad == 500):
            print('entro2')
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_500)

        elif(sensibilidad == 1000):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_1000)

        elif(sensibilidad == 2000):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_2000)
        else:
            print("Sensiblidad fuera de rango, disponible 250,500,1000,2000")
#        time.sleep(1)


    def get_sensiblidad_gyro(self, raw=False):
        # falta arreglar el terder parametro lenght
        raw_data = self.get_RangeSensitive_Gyro()
        sensiblidad = -1

        # if raw is True return register
        if(raw):
            sensiblidad = raw_data
        else:
            if raw_data == C.MPU6050_GYRO_FS_250:
                sensiblidad = 250

            elif raw_data == C.MPU6050_GYRO_FS_500:
                sensiblidad = 500

            elif raw_data == C.MPU6050_GYRO_FS_1000:
                sensiblidad = 1000

            elif raw_data == C.MPU6050_GYRO_FS_2000:
                sensiblidad = 2000


#        print("sensibilidad gyro:", sensiblidad)
        return sensiblidad

    '''
    Metodo encargado de cambiar la sensiblidad del acelerometro
    Recibe enteros:
        2:  Sensibilidad 2g
        4:  Sensibilidad 4g
        8: Sensibilidad 8g
        16: Sensibilidad 16g
    '''
    def set_sensibilidad_acc(self, sensibilidad):
        if(sensibilidad == 2):
            self.set_accel_RangeSensitive(C.MPU6050_ACCEL_FS_2)

        elif(sensibilidad == 4):
            self.set_accel_RangeSensitive(C.MPU6050_ACCEL_FS_4)

        elif(sensibilidad == 8):
            self.set_accel_RangeSensitive(C.MPU6050_ACCEL_FS_8)

        elif(sensibilidad == 16):
            self.set_accel_RangeSensitive(C.MPU6050_ACCEL_FS_16)
        else:
            print("Sensiblidad fuera de rango, disponible 2,4,8,16")


    def get_sensiblidad_acc(self, raw=False):
        raw_data = self.get_RangeSensitive_Acc()

        sensiblidad = -1

        # if raw is True return register
        if(raw):
            sensiblidad = raw_data
        else:
            if raw_data == C.MPU6050_ACCEL_FS_2:
                sensiblidad = 2

            elif raw_data == C.MPU6050_ACCEL_FS_4:
                sensiblidad = 4

            elif raw_data == C.MPU6050_ACCEL_FS_8:
                sensiblidad = 8

            elif raw_data == C.MPU6050_ACCEL_FS_16:
                sensiblidad = 16

#        print("sensibilidad acc:", sensiblidad)
        return sensiblidad

    '''
    Metodo para obtener el valor de los offset
    '''
    def get_offset_acc(self):
        x = self.read_i2c_word(C.MPU6050_RA_XA_OFFS_H)
        y = self.read_i2c_word(C.MPU6050_RA_YA_OFFS_H)
        z = self.read_i2c_word(C.MPU6050_RA_ZA_OFFS_H)

        print(x, y, z)
        return {'x': x, 'y': y, 'z': z}

    def get_offset_gyro(self):
        x = self.read_i2c_word(C.MPU6050_RA_XG_OFFS_USRH)
        y = self.read_i2c_word(C.MPU6050_RA_YG_OFFS_USRH)
        z = self.read_i2c_word(C.MPU6050_RA_ZG_OFFS_USRH)

        print(x, y, z)
        return {'x': x, 'y': y, 'z': z}

'''
    Metodo que hereda de libreria, se encarga de
    + asignar la direccion
    + asignar el bus i2c
    + asignar la sensiblidad 2g y 250 x default
    + despertar al dispositivo

    Tomar mediciones (in raw), devuelven una lista con los ejes
    get_acceleration()
    get_rotation()

    Para un correcto funcionamiento>
         1. instanciar x =  gy521(0x68,1,"nombre"), para despertarlo
         2. se resetea, y se vuelve a inciar para configurarse
         3. se debe configurar los offset

    '''

numbus = 1
x = mpu6050Hijo(0x68,numbus, "nombre")
#x.reset()
#x = mpu6050Hijo(0x68,numbus, "nombre")

#sensor 1
x.set_x_accel_offset(-1279)
x.set_y_accel_offset(-1097)
x.set_z_accel_offset(1252)

x.set_x_gyro_offset(189)
x.set_y_gyro_offset(-177)
x.set_z_gyro_offset(-188)

#print("offset_tc_xAcc",x.get_x_gyro_offset_TC())
print("sensibilidad acc", x.get_sensiblidad_acc())
print("sensibilidad gyro", x.get_sensiblidad_gyro())
print("aceleracion ",x.get_acc_data())
print("gyro", x.get_gyro_data())

x.set_sensibilidad_acc(8)
x.set_sensibilidad_gyro(2000)
print("sensibilidad nueva acc", x.get_sensiblidad_acc())
print("sensibilidad nueva gyro", x.get_sensiblidad_gyro())
#print("temperatura", x.get_)
#print("estatus", x.get_int_status())

#print("gryo x", x.)


#    def calibrarDispositivo(self):
#        calibrar = calibracion_Gy521(self.mpu, self.address)
#        calibrar.start()
#

#
#    # Temperature range is -40 C to 85 C
#    def get_temp(self):
#        """RETURNS TEMPERATURE IN DEGREE CELSIUS"""
#        raw_temp = self.read_i2c_word(TEMP_OUT0)
#
#        # Get the actual temperature using the formule given in the
#        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
#        actual_temp = (raw_temp / 340.0) + 36.53
#
#        return actual_temp

#    def get_distance(self, num1, num2):
#        '''# MEASURING DISTANCE OF 2 POINTS TO CALCULATE TILT ANGLE
#        From: http://www.hobbytronics.co.uk/accelerometer-info
#        '''
#        return math.sqrt((num1 * num1)+(num2 * num2))
#
## =======OBTIENE EL ANGULO DE ROTACION DE UN EJE POR MEDIO DE 3 EJE========
## https://www.luisllamas.es/arduino-orientacion-imu-mpu-6050/
## math.atan2( y / x ): Return atan(y / x), in radians.
#    def get_x_rotation(self, x, y, z):
#        radians = math.atan2(y, self.get_distance(x, z))
#        return math.degrees(radians)  # convierte a grados en radianes
#
#    def get_y_rotation(self, x, y, z):
#        radians = math.atan2(x, self.get_distance(y, z))
#        return -math.degrees(radians)  # convierte a grados en radianes
#
## =======OBTIENE EL ANGULO DE INCLINACION DE UN EJE POR MEDIO DE 3 EJE========
#    def get_y_Tilt(self, x, y, z):
#        radians = math.atan2(y, self.get_distance(x, z))
#        return -math.degrees(radians)
#
#    def get_x_Tilt(self, x, y, z):
#        radians = math.atan2(x, self.get_distance(y, z))
#        return math.degrees(radians)
#
#'''
#if __name__ == "__main__":
#    mpu = gy521(0x68, I2C_ARM)
#    print(mpu.get_temp())
#    accel_data = mpu.get_accel_data()
#    print(accel_data['x'])
#    print(accel_data['y'])
#    print(accel_data['z'])
#    gyro_data = mpu.get_gyro_data()
#    print(gyro_data['x'])
#    print(gyro_data['y'])
#    print(gyro_data['z'])
#'''
#
## PROBANDO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#from constantes.const import I2C_ARM
#
## mpu = gy521(0x68, I2C_ARM)
## mpu.get_accel_offset()
## mpu.get_gyro_offset()
##def probando():
##    mpu = gy521(0x68, I2C_ARM)
##    mpu.set_accel_sensibility(0x00)
##    mpu.read_accel_sensibility()
#
##    while(True):
##        accel_data = mpu.get_accel_data(True)  # if = true: "g", else m/s^2
##        print("x: " + str(accel_data['x']) +", y:" + str(accel_data['y']) +"x: " + str(accel_data['z']) )
##        print(accel_data['y'])
##        print("z")
##        print(accel_data['z'])
##
##    print("------CHANGING SENSIBILITY------")
##    mpu.set_accel_sensibility(0x18)
##    print("new sensibility")
##    print(mpu.read_accel_sensibility())
##    accel_data = mpu.get_accel_data(False)# if = true: "g", else m/s^2
##    print("x: ")
##    print(accel_data['x'])
##    print("y: ")
##    print(accel_data['y'])
##    print("z")
##    print(accel_data['z'])
##    print("==============")
##    print("=====FIN======")
##    print("==============")
##x = probando()
#
#
#'''
#VERIFICAR SI ESTO SE PUEDE HACER EN PYTHON
# // verify connection
#  Serial.println("Testing device connections...");
#  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
#  https://www.dfrobot.com/wiki/index.php/6_DOF_Sensor-MPU6050_(SKU:SEN0142)
#'''
#
## ################################
##    print(mpu.get_temp())
#
##    gyro_data = mpu.get_gyro_data()
##    print(gyro_data['x'])
##    print(gyro_data['y'])
##    print(gyro_data['z'])
## -*- coding: utf-8 -*-
#
