'''
    Title:      const
    Created:    Wed Apr 25 16:34:28 2018
    @author:    Gilbert Obando Quesada  <gilobaqu@gmail.com>

    OBJECTIVE
        + Change the constants used throughout the system quickly.
'''

NODE_NUM = 1
DIRECTION = 'holaaa'
CORRECTION = 110

'''----------------------------------------------------------------------------
                                 I2C's
   -------------------------------------------------------------------------'''
I2C_ARM = 1
I2C_VC = 0

'''----------------------------------------------------------------------------
                               SENSOR GY-521
   ----------------------------------------------------------------------------
mas detalles en:
,    www.invensense.com/wp-content/uploads/2015/02/MPU-6000-Register-Map1.pdf

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
# -------------Registros de encendido, reset-------------
ACCE_POWER_MGMT_1 = 0X6b
ACCE_POWER_MGMT_2 = 0X6C

# -------------Tipos de I2C dsponible en Raspberry-------------
I2C_ARM = 1
I2C_VC = 0

# ------------- Ubicacion del registro del acelerometro-------------
ADDRESS_REG_accA = 0x68
ADDRESS_REG_accB = 0x69

# Escabilidad del acelerometro deoendiendo de la sensibilidad
GRAVEDAD = 9.81          # unidades [m/s2]
ACCEL_SCALE_MODIFIER_2G = 16384.0
ACCEL_SCALE_MODIFIER_4G = 8192.0
ACCEL_SCALE_MODIFIER_8G = 4096.0
ACCEL_SCALE_MODIFIER_16G = 2048.0

GYRO_SCALE_MODIFIER_250DEG = 131.0
GYRO_SCALE_MODIFIER_500DEG = 65.5
GYRO_SCALE_MODIFIER_1000DEG = 32.8
GYRO_SCALE_MODIFIER_2000DEG = 16.4

# Registros de Sensibilidad
ACCEL_RANGE_2G = 0x00
ACCEL_RANGE_4G = 0x08
ACCEL_RANGE_8G = 0x10
ACCEL_RANGE_16G = 0x18

GYRO_RANGE_250DEG = 0x00
GYRO_RANGE_500DEG = 0x08
GYRO_RANGE_1000DEG = 0x10
GYRO_RANGE_2000DEG = 0x18

# -------------Direccion de salida de lecturas-------------
# acelerometro
ACCEL_XOUT0 = 0x3B
ACCEL_YOUT0 = 0x3D
ACCEL_ZOUT0 = 0x3F

# giroscopio
GYRO_XOUT0 = 0x43
GYRO_YOUT0 = 0x45
GYRO_ZOUT0 = 0x47

# temperatura
TEMP_OUT0 = 0x41

# -------------CONFIGURACION --------------------------------
ACCEL_CONFIG = 0x1C
GYRO_CONFIG = 0x1B

# Leer los offset acelerometro
ACCEL_XG_OFFS = 0x06
ACCEL_YG_OFFS = 0X08
ACCEL_ZG_OFFS = 0X0A

# Leer los offset acelerometro
GYRO_XG_OFFS = 0x13
GYRO_YG_OFFS = 0X15
GYRO_ZG_OFFS = 0X17

'''---------------------------------------------------------------------------
                            CALIBRACION GY521
   -------------------------------------------------------------------------'''
# Num de lecturas para el promedio, entre mas grande mas lento es calibrar
BUFFER_SIZE = 500  # default 1000

'''Variabilidad (o error) permitida con respecto a la media de la aceleracion.
Entre mas pequeno mas preciso sera, pero es posible que el sketch no converja.
Default 8'''
ACEL_DEADZONE = 12

'''Variabilidad (o error) permitido con respecto a la media del giroscopio.
Entre mas pequeno mas preciso sera, pero es posible que el sketch no converja.
Default: 1    '''
GIRO_DEADZONE = 5
# deadzone trabajara similar al concepto de "varianza"

'''Indica si el eje Z tambien debe de ir en Zero o NO'''
ZERO_EJE_Z = True

''' para verificar si se debe calibrar, el segundo
indica si se cambia sensibilidad para calibrar.'''
CALIBRATED = False
oldSensibilidad = -1

''' Valores por default: '''
#offset_accX1 = -5801
#offset_accY1 = -1773
#offset_accZ1 = -1030
#offset_gyrX1 = 4
#offset_gyrY1 = -10
#offset_gyrZ1 = 19
#
#offset_accX2 = -3503
#offset_accY2 = -1159
#offset_accZ2 = -333
#offset_gyrX2 = 4
#offset_gyrY2 = -28
#offset_gyrZ2 = 28

'''---------------------------------------------------------------------------
                                    PRUEBA
   -------------------------------------------------------------------------'''
ACCE_MINIMA = 0.0  # aceleracion minima(en g) para guardar y analizar datos,
DIRECC_TO_SAVE = "../Analisis_Puentes_Software/AlmacenPruebas/"
NAME_SENSOR_PORT1 = '1'
NUMBER_PORTSENSOR1 = 1

NAME_SENSOR_PORT2 = '2'
NUMBER_PORTSENSOR2 = 2

NAME_NODE = 1
NUM_SAMPLES_TO_FOURIER = 8192  # 16384  # 32768
IDNODE = '2'

'''---------------------------------------------------------------------------
                            FILTRO PASA BAJA GY521
   -------------------------------------------------------------------------'''
FREC_CORTE_260_Hz = 0x00
FREC_CORTE_184_Hz = 0x01
FREC_CORTE_94_Hz = 0x02
FREC_CORTE_44_Hz = 0x03
FREC_CORTE_21_Hz = 0x04
FREC_CORTE_10_Hz = 0x05
FREC_CORTE_5_Hz = 0x06

'''---------------------------------------------------------------------------
                                    NRF24L01
   -------------------------------------------------------------------------'''
COMMAND_CONEXION_NRF24L01 = "HEY_LISTEN"
COMMAND_RECEIVEDATA = "GET_DATA"

'''---------------------------------------------------------------------------
                                    GRAFICOS
   -------------------------------------------------------------------------'''
GRID_ENABLE = True
GRID_LINESTYLE = '-'     # ":"
GRID_LINEWIDTH = 0.2
GRID_COLOR = 'k'
AXE_EDGECOLOR = 'black'
AXE_LINEWIDTH = 1
FIGURE_SIZE = [5.0, 6.0]
FIGURE_DPI = 80
LINEWIDTH = 0.5   # redefine el grosor de las lineas de la senal
INTERVAL = 30     # <<float>> Representa el refrescamiento en ms
