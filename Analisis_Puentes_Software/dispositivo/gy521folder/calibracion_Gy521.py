'''
    TITLE:      const
    CREATED:    Wed Apr 25 16:34:28 2018
    AUTOR:      Gilbert Obando Quesada  <gilobaqu@gmail.com>
    BASED:      I2Cdev library and previous work by:
                    - Jeff Rowberg <jeff@rowberg.net>, available at:
                    - https://github.com/jrowberg/i2cdevlib

    OBJECTIVE
        + sensor gy521 calibrate

    NOTES:
        + It is recomendable calibrate this sensor on the temperature where you
          will work.
        + When this sketch is calibrating:
            - Don't touch the sensor.
            - The sensor should be placed in horizontal position.
'''

from MPU6050 import MPU6050
from constantes.const import BUFFER_SIZE  # num de lecturas para el promedio

# deadzone trabajara similar al concepto de "varianza"
from constantes.const import ACEL_DEADZONE  # variabilidad permitida
from constantes.const import GIRO_DEADZONE  # variabilidad permitida
import time


class calibracion_Gy521:
    i2c_bus = None  # 1
    device_address = None  # 0x68
    scaleFactor = 16384  # x default sera factor para sensiblidad de 2g.

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

    def __init__(self, numbus=1, a_address=0x69):
        self.device_address = a_address
        self.i2c_bus = numbus
        self.scaleFactor = 16384

        # Se inicializa la conexion con el sensor y se configura offsets!
        self.accelgyro = MPU6050(self.i2c_bus, self.device_address,
                                 self.ax_offset, self.ay_offset,
                                 self.az_offset, self.gx_offset,
                                 self.gy_offset, self.gz_offset, True)

    def set_offset(self, ax, ay, az, gx, gy, gz):
        self.accelgyro.set_x_accel_offset(ax)
        self.accelgyro.set_y_accel_offset(ay)
        self.accelgyro.set_z_accel_offset(az)
        self.accelgyro.set_x_gyro_offset(gx)
        self.accelgyro.set_y_gyro_offset(gy)
        self.accelgyro.set_z_gyro_offset(gz)

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

    def calibration(self):
        ''' se divide entre 32 ya que el acelerometro es muy sensible y obtiene
        datos muy variantes, 32 se refiere a 32 muestras,
        https://naylampmechatronics.com/blog/45_tutorial-mpu6050-acelerometro-y
        -giroscopio.html'''
        self.ax_offset = -self.mean_ax / 32
        self.ay_offset = -self.mean_ay / 32
        self.az_offset = (16384 - self.mean_az) / 32

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
            x = 16384 - self.mean_az
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

        if (abs(16384 - self.mean_az) <= ACEL_DEADZONE):
            self.az_offset += 1
            ready += 1
        else:
            correction = (16384 - self.mean_az) / ACEL_DEADZONE - 1
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
            print("\nMPU6050 Calibration Sketch")
            print("\nYour MPU6050 should be placed in horizontal position," +
                  "with package letters facing up. \nDon't touch it until " +
                  "you see a finish message.\n")
            # time.sleep(2)
            print("\nReading sensors for first time...")
            self.meansensors()
            time.sleep(1)

            # PASO 2: Calcula los posibles offsets
            print("\nCalculating offsets...")
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



#Para iniciar calibrando el sensor 1>
#x = calibracion_Gy521(1)
# para sensor #1
#
#x.set_offset(-2635,-359, 1034,58,-227,385)

#x.start()

