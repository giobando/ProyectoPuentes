# -*- coding: utf-8 -*-

"""This program handles the communication over I2C
between a Raspberry Pi and a MPU-6050 Gyroscope / Accelerometer combo.
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
"""

import smbus
# import math
# import time

# -----------------------------------------------------------------------------
#                                CONSTANTES
# -----------------------------------------------------------------------------
#from constantes.const import *
from constantes.const import ACCE_POWER_MGMT_1 as PWR_MGMT_1
from constantes.const import ACCE_POWER_MGMT_1 as PWR_MGMT_2
from constantes.const import GRAVEDAD as GRAVITIY_MS2

# ---------------ESCABILIDAD ASOCIADA A LA SENSIBILIDAD------------------------
# ACELEROMETRO
from constantes.const import ACCEL_SCALE_MODIFIER_2G
from constantes.const import ACCEL_SCALE_MODIFIER_4G
from constantes.const import ACCEL_SCALE_MODIFIER_8G
from constantes.const import ACCEL_SCALE_MODIFIER_16G
# GIROSCOPIO
from constantes.const import GYRO_SCALE_MODIFIER_250DEG
from constantes.const import GYRO_SCALE_MODIFIER_500DEG
from constantes.const import GYRO_SCALE_MODIFIER_1000DEG
from constantes.const import GYRO_SCALE_MODIFIER_2000DEG

# ------------------------------SENSIBILIDAD-----------------------------------
# ACELEROMETRO
from constantes.const import ACCEL_RANGE_2G
from constantes.const import ACCEL_RANGE_4G
from constantes.const import ACCEL_RANGE_8G
from constantes.const import ACCEL_RANGE_16G
# GIROSCOPIO
from constantes.const import GYRO_RANGE_250DEG
from constantes.const import GYRO_RANGE_500DEG
from constantes.const import GYRO_RANGE_1000DEG
from constantes.const import GYRO_RANGE_2000DEG

# --------------------------DIRECCION DE SALIDA--------------------------------
# ACELEROMETRO
from constantes.const import ACCEL_XOUT0
from constantes.const import ACCEL_YOUT0
from constantes.const import ACCEL_ZOUT0
# GIROSCOPIO
from constantes.const import GYRO_XOUT0
from constantes.const import GYRO_YOUT0
from constantes.const import GYRO_ZOUT0
# TEMPERATURA
from constantes.const import TEMP_OUT0

# -------------CONFIGURACION ACELETROMETRO-------------
from constantes.const import ACCEL_CONFIG
from constantes.const import GYRO_CONFIG


class gy521:
    address = None
    bus = None  # smbus.SMBus(1) SE INICIARA CUANDO SE INSTANCIE

    def __init__(self, address, numbus):
        self.address = address
        self.bus = smbus.SMBus(numbus)

        # Wake up the MPU-6050 since it starts in sleep mode
        self.bus.write_byte_data(self.address, PWR_MGMT_1, 0x00)

    # -------------------------leido-----------------------------------------
    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers (LEYENDO WORD)
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        # LEYENDO PALABRA 2C
        value = (high << 8) + low
        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # -------------------------leido-----------------------------------------
    def get_temp(self):
        """OBTIENE LA TEMPERATURA Y LA RETORNA EN GRADOS CELCIUS"""
        raw_temp = self.read_i2c_word(TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53

        return actual_temp

    # -------------------------leido-----------------------------------------
    def set_accel_range(self, accel_range):
        """CONFIGURA LA SENSIBILIDAD DE LA ACELERACION!!     """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    # -------------------------leido-----------------------------------------
    def read_accel_range(self, raw=False):
        """RETORNA QUE SENSIBILIDAD TIENE CONFIGURADO EL ACELEROMETRO
        Reads the range the accelerometer is set to.
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

    # -------------------------leido-----------------------------------------
    # retorna una lista
    def get_accel_data(self, g=False):
        """OBTIENE EL VALOR DE LA ACELERACION EN LOS TRES EJES EN "g" O "M/S2"
        Gets and returns the X, Y and Z values from the accelerometer.
        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        x = self.read_i2c_word(ACCEL_XOUT0)
        y = self.read_i2c_word(ACCEL_YOUT0)
        z = self.read_i2c_word(ACCEL_ZOUT0)

        # verifica sensibilidad tiene para asignarle la escabilidad correcta.
        accel_scale_modifier = None
        # obtiene la sensibilidad que tiene configurado.
        accel_range = self.read_accel_range(True)

#        # asignacion de escabilidad correcta.
#        if accel_range == self.ACCEL_RANGE_2G:
#            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
#        elif accel_range == self.ACCEL_RANGE_4G:
#            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
#        elif accel_range == self.ACCEL_RANGE_8G:
#            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
#        elif accel_range == self.ACCEL_RANGE_16G:
#            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
#        else:
#            print("Unkown range - accel_scale_modifier se....
#            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        # asignacion de escabilidad correcta.
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

        # modificar para sacar estos valores con GETS!!!!!
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

    # -------------------------leido-----------------------------------------
    def set_gyro_range(self, gyro_range):
        """CONFIGURA LA SENSIBILIDAD DEL GIROSCOPIO
        Sets the range of the gyroscope to range.
        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, GYRO_CONFIG, gyro_range)

    # -------------------------leido-----------------------------------------
    def read_gyro_range(self, raw=False):
        """RETORNA QUE SENSIBILIDAD TIENE CONFIGURADO EL ACELEROMETRO
        Reads the range the gyroscope is set to.
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

    # -------------------------leido-----------------------------------------
    # AVERIGUAR EN QUE UNIDADES RETORNA!! retorna lista
    def get_gyro_data(self):
        """OBTIENE EL VALOR DEL GIROSCOPIO.
        Gets and returns the X, Y and Z values from the gyroscope.
        Returns the read values in a dictionary.
        """
        x = self.read_i2c_word(GYRO_XOUT0)
        y = self.read_i2c_word(GYRO_YOUT0)
        z = self.read_i2c_word(GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

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

    # -------------------------leido-----------------------------------------
    # BUSCARLE UNA FUNCION.
    def get_all_data(self):
        """Lee y retorna todos los datos posibles!!
        Reads and returns all the available data.
        """
        temp = self.get_temp()
        accel = self.get_accel_data()
        gyro = self.get_gyro_data()

        return [accel, gyro, temp]


if __name__ == "__main__":
    mpu = gy521(0x68, 1)
    print(mpu.get_temp())
    accel_data = mpu.get_accel_data()
    print(accel_data['x'])
    print(accel_data['y'])
    print(accel_data['z'])
    gyro_data = mpu.get_gyro_data()
    print(gyro_data['x'])
    print(gyro_data['y'])
    print(gyro_data['z'])
