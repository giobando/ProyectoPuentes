# -*- coding: utf-8 -*-

"""This program handles the communication over I2C
between a Raspberry Pi and a MPU-6050 Gyroscope / Accelerometer combo.
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
"""

import math
from calibracion_Gy521 import calibracion_Gy521

# from time import sleep
# import time

# -----------------------------------------------------------------------------
#                                CONSTANTES
# -----------------------------------------------------------------------------

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
from dispositivo.gy521folder.MPU6050Padre import MPU6050Padre


class mpu6050Hijo(MPU6050Padre):
    scaleValue = 1  # depende de la sensibilidad, se escala a este numero
    sensorName = None

    '''
    Constructor, recibe la direccion del sensor ejm
    address = 0x68
    numbus = 1 si es para i2c, 0 si es para ARM
    nameSensor =<<strng>>    '''
    def __init__(self, address, numbus):
        # numbum = I2C port assigned.
        MPU6050Padre.__init__(self, numbus, address)
    def set_nameSensor(self, nameSensor):
        self.sensorName = nameSensor

    '''
    CONFIGURACION OFFSET
    Recibe: 6 valores enteros    '''
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
    Depende de la sensbilidad aplica factor de escalamiento    '''
    def get_acc_data(self, gUnit=False):
        # if g is True, return data in g units,else in m/s2
        accel_range = self.get_sensiblidad_acc(True)
        factorScale = 1

        # Assigns the correct scability at sensibility
        if accel_range == C.MPU6050_ACCEL_FS_2:
#            print("sensibilidad", 2)
            factorScale = ACCEL_SCALE_MODIFIER_2G
        elif accel_range == C.MPU6050_ACCEL_FS_4:
#            print("sensibilidad", 4)
            factorScale = ACCEL_SCALE_MODIFIER_4G
        elif accel_range == C.MPU6050_ACCEL_FS_8:
#            print("sensibilidad", 8)
            factorScale = ACCEL_SCALE_MODIFIER_8G
        elif accel_range == C.MPU6050_ACCEL_FS_16:
#            print("sensibilidad", 16)
            factorScale = ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range:")
            print("- accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            factorScale = ACCEL_SCALE_MODIFIER_2G

#        print("factor scala", factorScale)
        acc = self.get_acceleration()
        x = acc[0] / factorScale
        y = acc[1] / factorScale
        z = acc[2] / factorScale

        if(gUnit):  # unidades g
            return {'x': x, 'y': y, 'z': z}
        else:  # unidades m/2
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
        Metodo para obtener la temperatura en raw y retorna en grados celsius
        Rango de temperatura: -40 a 85C.
        using the formule given in the MPU-6050 -
        Register Map and Descriptions revision 4.2, page 30 '''
    def get_temperatura(self):
        raw_temp = self.get_Temperature()
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53
        return actual_temp

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
     |   7      |   -- Reserved --   |   8           |
     |__________|____________________|_______________|

     RECIBE ENTEROS DE 0 A 6 segun la tabla anterior.    '''
    def set_filtroPasaBaja(self, frecCorte):
        if (frecCorte == 0):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)
        elif (frecCorte == 1):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_188)
        elif (frecCorte == 2):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_98)
        elif (frecCorte == 3):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_42)
        elif (frecCorte == 4):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_20)
        elif (frecCorte == 5):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_10)
        elif (frecCorte == 6):
            self.set_DLF_mode(C.MPU6050_DLPF_BW_5)
        else:
            self.set_DLF_mode(C.MPU6050_DLPF_BW_256)
            print("filtro fuera de rango, se desactiva")

    '''
    Metodos encargados de obtener y configurar la frecuencia de muestreo
    Formula tomada de
    MPU-6000-Register-Map1, pag 12
    Recordar:
        + si DLPF esta desactivado (0 o 7):
            frecuencia maxima = 8Khz, else: 1000    '''
    def set_frecMuestreoAcc(self, frecMuestreo):
        # la frec muestreo a configurar a continuacion sera cuando
        # el DLPF esta activado!!!
        smplrt = 0
        if(0 < frecMuestreo <= 1000):
            smplrt = (1000 / frecMuestreo) - 1
            self.set_rate(smplrt)
        else:
            print("frecuencia fuera de rango")
            print("Frecuencia permitido entre 0 a 1000 Hz")

    def set_frecMuestreoAccSinFiltro(self, frecMuestreo):
        # la frec muestreo a configurar a continuacion sera cuando
        # el DLPF esta activado!!!
        smplrt = 0
        if(0 < frecMuestreo <= 1000):
            smplrt = (8000 / frecMuestreo) - 1
            self.set_rate(smplrt)
        else:
            print("frecuencia fuera de rango")
            print("Frecuencia permitido entre 0 a 1000 Hz")

    def get_frecMuestreoAcc(self):
        smplrt = self.get_rate()
        frecAcc = 1000 / (1 + smplrt)
        return frecAcc

    def get_frecMuestreoAccSinFiltro(self):
        smplrt = self.get_rate()
        frecAcc = 8000 / (1 + smplrt)
        return frecAcc

    '''
    Metodo encargado de cambiar la sensiblidad del giroscopio
    Recibe enteros:
        250:  Sensibilidad 250 grados/segundo
        500:  Sensibilidad 500 grados/segundo
        1000: Sensibilidad 1000 grados/segundo
        2000: Sensibilidad 2000 grados/segundo  '''
    def set_sensibilidad_gyro(self, sensibilidad):
        if(sensibilidad == 250):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_250)
        elif(sensibilidad == 500):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_500)
        elif(sensibilidad == 1000):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_1000)
        elif(sensibilidad == 2000):
            self.set_gyro_rangeSensitive(C.MPU6050_GYRO_FS_2000)
        else:
            print("Sensiblidad fuera de rango, disponible 250,500,1000,2000")

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
        return sensiblidad

    '''
    Metodo encargado de cambiar la sensiblidad del acelerometro
    Recibe enteros:
        2:  Sensibilidad 2g
        4:  Sensibilidad 4g
        8: Sensibilidad 8g
        16: Sensibilidad 16g    '''
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

    '''
    Retorna la sensibilidad.
    si recibe True, retorna el registro de la sensibilidad
    si recibe False, retorna la sensiblidad en Int  '''
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
        return sensiblidad

    '''
    Metodo para obtener el valor de los offset
    '''
    def get_offset_acc(self):
        x = self.read_i2c_word(C.MPU6050_RA_XA_OFFS_H)
        y = self.read_i2c_word(C.MPU6050_RA_YA_OFFS_H)
        z = self.read_i2c_word(C.MPU6050_RA_ZA_OFFS_H)
        return {'x': x, 'y': y, 'z': z}

    def get_offset_gyro(self):
        x = self.read_i2c_word(C.MPU6050_RA_XG_OFFS_USRH)
        y = self.read_i2c_word(C.MPU6050_RA_YG_OFFS_USRH)
        z = self.read_i2c_word(C.MPU6050_RA_ZG_OFFS_USRH)
        return {'x': x, 'y': y, 'z': z}

    '''
    Funcion encargada de la distancia entre dos puntos,
    necesaria para el calcuo de la rotacion y la inclinacion
    From: http://www.hobbytronics.co.uk/accelerometer-info  '''
    def get_distance(self, num1, num2):
        return math.sqrt((num1 * num1)+(num2 * num2))

    '''
    Metodo que calcula las rotaciones en el eje x y y por medio del
    acelerometro.
    El eje z no, porque es paralelo a la gravedad, se necesita magnometro
    Recibe aceleraciones, la unidad d los parametros no importa porque
    se cancelan.
    ## https://www.luisllamas.es/arduino-orientacion-imu-mpu-6050/
    ## math.atan2( y / x ): Return atan(y / x), in radians.   '''
    # ROTACIONES
    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.get_distance(x, z))
        return math.degrees(radians)  # convierte a grados en radianes

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.get_distance(y, z))
        return -math.degrees(radians)  # convierte a grados en radianes

    # INCLINACIONES
    def get_y_Tilt(self, x, y, z):
        radians = math.atan2(y, self.get_distance(x, z))
        return -math.degrees(radians)

    def get_x_Tilt(self, x, y, z):
        radians = math.atan2(x, self.get_distance(y, z))
        return math.degrees(radians)

# COMO CORRER LAS FUCNONES:
#numbus = 1
#x = mpu6050Hijo(0x68, numbus, "nombre")
#x.reset() #usar solo en SPI Interface
#x = mpu6050Hijo(0x68,numbus, "nombre")

#print("rotacion con acc",x.get_x_rotation(1,0.2,5))
#print("distancia",x.get_distance(3,6))
#print("inclinacion", x.get_x_Tilt(4,5,6))
#print("temperatura", x.get_temperatura())
#
#print("offset_tc_xAcc",x.get_x_gyro_offset_TC())
#print("sensibilidad acc", x.get_sensiblidad_acc())
#print("sensibilidad gyro", x.get_sensiblidad_gyro())
#print("aceleracion ",x.get_acc_data())
#print("gyro", x.get_gyro_data())
#
#x.set_sensibilidad_acc(8)
#x.set_sensibilidad_gyro(2000)
#print("sensibilidad nueva acc", x.get_sensiblidad_acc())
#print("sensibilidad nueva gyro", x.get_sensiblidad_gyro())
#
#print("offset acc", x.get_offset_acc())
#print("offset gyro", x.get_offset_gyro())


