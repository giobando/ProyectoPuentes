"""
Created on Wed Apr 25 16:34:28 2018

@author: Gilbert Obando Quesada
"""

'''Constantes compartidas por varias instancias con el mismo valor'''

NODE_NUM = 1
DIRECTION = 'holaaa'


'''----------------------------------------------------------------------------
                                 ACELEROMETRO
   ----------------------------------------------------------------------------
mas detalles en:
    www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

ACCE_POWER_MGMT_1:
    -It allows to configure the power mode and clock source.
    -It also provides a bit for resetting the entire device,
     and a bit for disabling the temperature sensor.

ACCE_POWER_MGMT_2:
    -It allows to configure the frequency of wake-ups in Accelerometer Only Low
     Power Mode.
    -It allows to put individual axes of the accelerometer and gyroscope into
     standby mode.
'''
# Registers
ACCE_POWER_MGMT_1 = 0X6b
ACCE_POWER_MGMT_2 = 0X6C
ACCE_WHO_I_AM = 0x68        # registro lectura del dispositivo
ACCE_WHO_I_AM_AD0 = 0x68    # registro lectura del dispositivo cambiado por AD0

GRAVITIY_MS2 = 9.8          # unidades [m/s2]

I2C_ARM = 1
I2C_VC = 0

# ##################################
# Global Variables
address = None
# bus = smbus.SMBus(1)

# Scale Modifiers
ACCEL_SCALE_MODIFIER_2G = 16384.0
ACCEL_SCALE_MODIFIER_4G = 8192.0
ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0

GYRO_SCALE_MODIFIER_250DEG = 131.0
GYRO_SCALE_MODIFIER_500DEG = 65.5
GYRO_SCALE_MODIFIER_1000DEG = 32.8
GYRO_SCALE_MODIFIER_2000DEG = 16.4

# Pre-defined ranges
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x08
ACCEL_RANGE_8G = 0x10
ACCEL_RANGE_16G = 0x18

GYRO_RANGE_250DEG = 0x00
GYRO_RANGE_500DEG = 0x08
GYRO_RANGE_1000DEG = 0x10
GYRO_RANGE_2000DEG = 0x18

# MPU-6050 Registers
PWR_MGMT_1 = 0x6B
PWR_MGMT_2 = 0x6C

ACCEL_XOUT0 = 0x3B
ACCEL_YOUT0 = 0x3D
ACCEL_ZOUT0 = 0x3F

TEMP_OUT0 = 0x41

GYRO_XOUT0 = 0x43
GYRO_YOUT0 = 0x45
GYRO_ZOUT0 = 0x47

ACCEL_CONFIG = 0x1C
GYRO_CONFIG = 0x1B
