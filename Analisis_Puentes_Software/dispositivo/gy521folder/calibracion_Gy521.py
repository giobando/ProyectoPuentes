# -*- coding: utf-8 -*-
'''
    TITLE:      const
    CREATED:    Wed Apr 25 16:34:28 2018
    AUTOR:      Gilbert Obando Quesada  <gilobaqu@gmail.com>
    BASED:      I2Cdev library and previous work by:
                    - Jeff Rowberg <jeff@rowberg.net>, available at:
                    - https://github.com/jrowberg/i2cdevlib
                    https://naylampmechatronics.com/blog/45_tutorial-mpu6050-acelerometro-y
        -giroscopio.html

    OBJECTIVE
        + sensor gy521 calibrate

    NOTES:
        + It is recomendable calibrate this sensor on the temperature where you
          will work.
        + When this sketch is calibrating:
            - Don't touch the sensor.
            - The sensor should be placed in horizontal position.
            - The sensibility should be 8g.
'''
from MPU6050 import MPU6050

# deadzone trabajara similar al concepto de "varianza"
from constantes.const import ACEL_DEADZONE  # variabilidad permitida
from constantes.const import GIRO_DEADZONE  # variabilidad permitida

from constantes.const import BUFFER_SIZE  # num de lecturas para el promedio
from constantes.const import ACCEL_SCALE_MODIFIER_2G
from constantes.const import ACCEL_SCALE_MODIFIER_4G
from constantes.const import ACCEL_SCALE_MODIFIER_8G
from constantes.const import ACCEL_SCALE_MODIFIER_16G
from constantes.const import SENSITIVE_to_CALIBRATE

import time

#from dispositivo.gy521folder.mpu6050Hijo import mpu6050Hijo
from dispositivo.gy521folder.MPU6050Padre import MPU6050Padre


class calibracion_Gy521:
    scaleFactor = ACCEL_SCALE_MODIFIER_8G

    # valores promedio
    mean_ax = 0
    mean_ay = 0
    mean_az = 0
    mean_gx = 0
    mean_gy = 0
    mean_gz = 0

    # offset, inicialmente sera 0
    ax_offset = 0
    ay_offset = 0
    az_offset = 0
    gx_offset = 0
    gy_offset = 0
    gz_offset = 0

    accelgyro = None

    '''
    Recibe:
        + numbus = bus i2c al que fue conectado el sensor. Como solo se va
                    trabajar con I2cArm, sera x default 1 siempre
    '''
    def __init__(self, sensorObject):

        # Se inicializa la conexion con el sensor y se configura offsets!
        self.accelgyro = sensorObject

        # La sensibilidad con la que trabaja la calibracion es de 8g,
        # de cambiarla, se debe modificar la constante SENSITIVE_TO_CALIBRATE
        # Se obtiene el factor de escala dependiendo del anterior
        self.set_scaleFactor()

    def set_scaleFactor(self):
        if SENSITIVE_to_CALIBRATE == 2:
            self.scaleFactor = int(ACCEL_SCALE_MODIFIER_2G)

        elif SENSITIVE_to_CALIBRATE == 4:
            self.scaleFactor = int(ACCEL_SCALE_MODIFIER_4G)

        elif SENSITIVE_to_CALIBRATE == 8:
            self.scaleFactor = int(ACCEL_SCALE_MODIFIER_8G)

        elif SENSITIVE_to_CALIBRATE == 16:
            self.scaleFactor = int(ACCEL_SCALE_MODIFIER_16G)

    def set_offset(self, ax, ay, az, gx, gy, gz):
        self.accelgyro.set_x_accel_offset(ax)
        self.accelgyro.set_y_accel_offset(ay)
        self.accelgyro.set_z_accel_offset(az)
        self.accelgyro.set_x_gyro_offset(gx)
        self.accelgyro.set_y_gyro_offset(gy)
        self.accelgyro.set_z_gyro_offset(gz)

    '''
    Encargado de calcular promedios en los tres ejes de acelerometro y gyrosco-
    pio para calcular el offset '''
    def meansensors(self):
        i = 0
        buff_ax = 0
        buff_ay = 0
        buff_az = 0
        buff_gx = 0
        buff_gy = 0
        buff_gz = 0

        while (i < (BUFFER_SIZE + 101)):
            # read raw accel/gyro measurements from device
            accel_reading = self.accelgyro.get_acceleration()
            x_accel_reading = accel_reading[0]
            y_accel_reading = accel_reading[1]
            z_accel_reading = accel_reading[2]

            gyro_reading = self.accelgyro.get_rotation()
            x_gyro_reading = gyro_reading[0]
            y_gyro_reading = gyro_reading[1]
            z_gyro_reading = gyro_reading[2]

            # First 100 measures are discarded
            if (i > 100 and i <= (BUFFER_SIZE + 100)):
                buff_ax = buff_ax + x_accel_reading
                buff_ay = buff_ay + y_accel_reading
                buff_az = buff_az + z_accel_reading
                buff_gx = buff_gx + x_gyro_reading
                buff_gy = buff_gy + y_gyro_reading
                buff_gz = buff_gz + z_gyro_reading

            if (i == (BUFFER_SIZE + 100)):
                self.mean_ax = buff_ax / BUFFER_SIZE
                self.mean_ay = buff_ay / BUFFER_SIZE
                self.mean_az = buff_az / BUFFER_SIZE
                self.mean_gx = buff_gx / BUFFER_SIZE
                self.mean_gy = buff_gy / BUFFER_SIZE
                self.mean_gz = buff_gz / BUFFER_SIZE
            i += 1
            time.sleep(2/1000)  # Needed so we don't get repeated measures

        print("meansensor mean ax, ay, az",
              self.mean_ax, self.mean_ay, self.mean_az)

    '''
    Encargado de configurar el offset en cada eje y configurar el sensor con
    los respectivos offset para luego ser evaluado en otra funcion  '''
    def calibration(self):
        ''' Se divide en 32 medidas ya el acelerometro es muy sensible y obtiene
        datos muy variantes.   '''
        self.ax_offset = -self.mean_ax / 32
        self.ay_offset = -self.mean_ay / 32
        self.az_offset = (self.scaleFactor - self.mean_az) / 32
        print("Valores offset ax, ay, az, y scaleFactor respectivo a la sensibilidad: \n\t",
              self.ax_offset, self.ay_offset, self.az_offset, self.scaleFactor)

        self.gx_offset = -self.mean_gx / 8
        self.gy_offset = -self.mean_gy / 8
        self.gz_offset = -self.mean_gz / 8

        print("Calibrating offsets (ax, ay, az, gx, gy, gz):",
              self.ax_offset, self.ay_offset, self.az_offset,
              self.gx_offset, self.gy_offset, self.gz_offset)

        num_offset_Succeful = 6
        while (1):
            self.accelgyro.set_x_accel_offset(self.ax_offset)
            self.accelgyro.set_y_accel_offset(self.ay_offset)
            self.accelgyro.set_z_accel_offset(self.az_offset)

            self.accelgyro.set_x_gyro_offset(self.gx_offset)
            self.accelgyro.set_y_gyro_offset(self.gy_offset)
            self.accelgyro.set_z_gyro_offset(self.gz_offset)

            self.meansensors()

            print("\n Averages news:")
            x = self.scaleFactor - self.mean_az
            print("meanX: ", self.mean_ax, "meanY:", self.mean_ay, "meanZ:", x)
            print("mean_gx: ", self.mean_gx,
                  "mean_gy:", self.mean_gy, "mean_gz:", self.mean_gz)
            print("offset acc x,y,z", self.ax_offset, self.ay_offset,
                  self.az_offset, "offset gyro x,y,z", self.gx_offset,
                  self.gy_offset, self.gz_offset)

            if (self.evaluateOffset() == num_offset_Succeful):
                return True

    def evaluateOffset(self):
        ready = 0

        if (abs(self.mean_ax) <= ACEL_DEADZONE):
                self.ax_offset += 1
                ready += 1
        else:
            correction = self.mean_ax / ACEL_DEADZONE - 1
            self.ax_offset = self.ax_offset - correction

        if (abs(self.mean_ay) <= ACEL_DEADZONE):
            self.ay_offset += 1
            ready += 1
        else:
            correction = self.mean_ay / ACEL_DEADZONE - 1
            self.ay_offset = self.ay_offset - correction

        if (abs(self.scaleFactor - self.mean_az) <= ACEL_DEADZONE):
            self.az_offset += 1
            ready += 1
        else:
            correction = (self.scaleFactor - self.mean_az) / ACEL_DEADZONE - 1
            self.az_offset = self.az_offset + correction

        if (abs(self.mean_gx) <= GIRO_DEADZONE):
            ready += 1
        else:
            correction = self.mean_gx / (GIRO_DEADZONE + 1)
            self.gx_offset = self.gx_offset - correction

        if (abs(self.mean_gy) <= GIRO_DEADZONE):
            ready += 1
        else:
            correction = self.mean_gy / (GIRO_DEADZONE + 1)
            self.gy_offset = self.gy_offset - correction

        if (abs(self.mean_gz) <= GIRO_DEADZONE):
            ready += 1
        else:
            correction = self.mean_gz / (GIRO_DEADZONE + 1)
            self.gz_offset = self.gz_offset - correction

        return ready

    # =========================== promedio ====================================
    def start(self):

        while (True):
            # PASO 1: Obtiene promedios de mediciones
            print("\nCargando: \n\tMPU6050 Calibration Sketch...")
#            print("\nYour MPU6050 should be placed in horizontal position," +
#                  "with package letters facing up. \nDon't touch it until " +
#                  "you see a finish message.\n")
            print("\nVerifique que el sensor Gy-521 tenga una posicion horizontal." +
                  "\nPOR FAVOR NO LO TOQUE EL SENSOR HASTA " +
                  "VER UN MENSAJE DE FINALIZADO.\n")
            # time.sleep(2)
#            print("\nReading sensors for first time...")
            print("\nLeyendo sensores por primera vez...")
            self.meansensors()
            time.sleep(1)

            # PASO 2: Calcula los posibles offsets
#            print("\nCalculating offsets...")
            print("\mCalculando offset...")
            if (self.calibration()):
                print("\nFINISHED")
                break
            # time.sleep(1)  # delay(1000)

            # PASO 3: Imprime resultados, aqui ya esta configurado en el sensor
            self.meansensors()
            print("\nFINISHED!")

            print("Sensor readings with mean (Ax, Ay, Az, Gx, Gy, Gz):")
            print(self.mean_ax, self.mean_ay, self.mean_az,
                  self.mean_gx, self.mean_gy, self.mean_gz)

            print("Your offsets (Ax, Ay, Az, Gx, Gy, Gz):")
            print(self.ax_offset, self.ay_offset, self.az_offset,
                  self.gx_offset, self.gy_offset, self.gz_offset)

            print("Check that sensor readings are close to 0 0 16384 0 0 0")

    def get_offset_Gyro_Calibrated(self):
        return self.gx_offset, self.gy_offset, self.gz_offset

    def get_offset_Acc_Calibrated(self):
        return self.ax_offset, self.ay_offset, self.az_offset




#Para iniciar calibrando el sensor 1>
#x = calibracion_Gy521(1)
# para sensor #1
#
        #se debe de modificar la sensibilidad a 8g
#x.set_offset(-2635,-359, 1034,58,-227,385)

#x.start()

