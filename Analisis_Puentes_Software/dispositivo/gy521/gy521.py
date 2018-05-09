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


class gy521:
    address = None
    bus = None  # smbus.SMBus(1), it will be assigned in the constructor

    def __init__(self, address, numbus):
        # numbum = I2C port assigned.
        self.address = address
        self.bus = smbus.SMBus(numbus)

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0x00)
    
    def calibrarDispositivo(self):
        calibrar = calibracion_Gy521(self.bus, self.address)

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.
        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        # LEYENDO PALABRA 2C
        value = (high << 8) + low
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # Temperature range is -40 C to 85 C
    def get_temp(self):
        """RETURNS TEMPERATURE IN DEGREE CELSIUS"""
        raw_temp = self.read_i2c_word(TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53

        return actual_temp

    def set_accel_sensibility(self, accel_range):
        """SETS ACCELERATION SENSIBILITY."""
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, ACCEL_CONFIG, accel_range)

    def read_accel_sensibility(self, raw=False):
        """RETURN THE SENSIBILITY THE ACCELORMETER IS SET TO.
        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == ACCEL_RANGE_2G:
                return 2
            elif raw_data == ACCEL_RANGE_4G:
                return 4
            elif raw_data == ACCEL_RANGE_8G:
                return 8
            elif raw_data == ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g=False):
        """GETS AND RETURNS THE X, Y AND Z VALUES FROM THE ACCELOMETERS.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        RETURNS a DICTIONARY with the measurement results.
        """
        x = self.read_i2c_word(ACCEL_XOUT0)
        y = self.read_i2c_word(ACCEL_YOUT0)
        z = self.read_i2c_word(ACCEL_ZOUT0)

        # To read the sensitivity set to and assign the correct scalability.
        accel_scale_modifier = None
        # Gets the sensibility set to.
        accel_range = self.read_accel_sensibility(True)

        # Assigns the correct scability at sensibility
        if accel_range == ACCEL_RANGE_2G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_2G
        elif accel_range == ACCEL_RANGE_4G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_4G
        elif accel_range == ACCEL_RANGE_8G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_8G
        elif accel_range == ACCEL_RANGE_16G:
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range:")
            print("- accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = ACCEL_SCALE_MODIFIER_2G

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * GRAVITIY_MS2
            y = y * GRAVITIY_MS2
            z = z * GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}

    def set_gyro_sensibility(self, gyro_range):
        """SETS THE SENSIBILITY OF THE GYROSCOPE.
        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, GYRO_CONFIG, gyro_range)

    def read_gyro_sensibility(self, raw=False):
        """GET THE SENSIBILITY THE GYROSCOPE IS SET TO.
        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == GYRO_RANGE_250DEG:
                return 250
            elif raw_data == GYRO_RANGE_500DEG:
                return 500
            elif raw_data == GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    # AVERIGUAR EN QUE UNIDADES RETORNA!
    def get_gyro_data(self):
        """GETS X, Y AND Z VALUES FROM THE GYROSCOPE.
        RETURNS the read values in a DICTIONARY.
        """
        x = self.read_i2c_word(GYRO_XOUT0)
        y = self.read_i2c_word(GYRO_YOUT0)
        z = self.read_i2c_word(GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_sensibility(True)

        if gyro_range == GYRO_RANGE_250DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == GYRO_RANGE_500DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == GYRO_RANGE_1000DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == GYRO_RANGE_2000DEG:
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range: ")
            print("gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    # el set offset se encuentra dentro de la calibracion!!!!!!

    def get_accel_offset(self):
        # registers fueron tomados de:
        # "MPU Hardware Offset Registers Application Note"
        # https://gzuliani.bitbucket.io/arduino/files/arduino-mpu6050/invensense-hardware-offset-registers.pdf
        x = self.read_i2c_word(ACCEL_XG_OFFS)
        y = self.read_i2c_word(ACCEL_YG_OFFS)
        z = self.read_i2c_word(ACCEL_ZG_OFFS)

        print(x, y, z)

        return {'x': x, 'y': y, 'z': z}

    def get_gyro_offset(self):
        x = self.read_i2c_word(GYRO_XG_OFFS)
        y = self.read_i2c_word(GYRO_YG_OFFS)
        z = self.read_i2c_word(GYRO_ZG_OFFS)

        print(x, y, z)

        return {'x': x, 'y': y, 'z': z}

    # BUSCARLE UNA FUNCION.!!!!!!!!!!!!!!!!!
    def get_all_data(self):
        """READ AND RETURNS ALL THE AVAILABLE DATA"""
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()

        return [accel, gyro, temp]

    def get_distance(self, num1, num2):
        ''' MEASURING DISTANCE OF 2 POINTS TO CALCULATE TILT ANGLE
        From: http://www.hobbytronics.co.uk/accelerometer-info
        '''
        return math.sqrt((num1 * num1)+(num2 * num2))

    def get_x_rotation(self, x, y, z):
        radians = math.atan2(y, self.get_distance(x, z))
        return math.degrees(radians)  # convierte a grados en radianes

    def get_y_rotation(self, x, y, z):
        radians = math.atan2(x, self.get_distance(y, z))
        return -math.degrees(radians)  # convierte a grados en radianes


'''
if __name__ == "__main__":
    mpu = gy521(0x68, I2C_ARM)
    print(mpu.get_temp())
    accel_data = mpu.get_accel_data()
    print(accel_data['x'])
    print(accel_data['y'])
    print(accel_data['z'])
    gyro_data = mpu.get_gyro_data()
    print(gyro_data['x'])
    print(gyro_data['y'])
    print(gyro_data['z'])
'''

# PROBANDO!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# from constantes.const import I2C_ARM

# mpu = gy521(0x68, I2C_ARM)
# mpu.get_accel_offset()
# mpu.get_gyro_offset()
# def probando():
#    mpu = gy521(0x68, I2C_ARM)
#    print("sensibility")
#    mpu.set_accel_sensibility(0x00)
#    print(mpu.read_accel_sensibility())

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


'''
VERIFICAR SI ESTO SE PUEDE HACER EN PYTHON
 // verify connection
  Serial.println("Testing device connections...");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");
  https://www.dfrobot.com/wiki/index.php/6_DOF_Sensor-MPU6050_(SKU:SEN0142)
'''

# ################################
#    print(mpu.get_temp())

#    gyro_data = mpu.get_gyro_data()
#    print(gyro_data['x'])
#    print(gyro_data['y'])
#    print(gyro_data['z'])
