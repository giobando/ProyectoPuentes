from MPU6050 import MPU6050
import time
# //////////////////////////////   CONFIGURATION   //////////////////////////
i2c_bus = 1
device_address = 0x68

# Modifique estas 3 variables si ud quiere precision a sus necesidades.
'''cantidad de lecturas para calcular el promedio
Un valor alto hara la presicion mejor pero sera mas lento.
'''
buffer_size = 1000

'''
error acelerometro permitido, entre mas pequeno mas preciso sera,
pero es posible que el sketch no converja: default 85
'''
acel_deadzone = 20

'''
error gyro permitido, entre mas pequeno mas preciso sera pero es posible
que el sketch no converja. default: 1
'''
giro_deadzone = 10

# deadzone: cantidad de variacion entre 2 mediciones consecutivas
# valores raw
ax = 0
ay = 0
az = 0
gx = 0
gy = 0
gz = 0

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

ax = 0
ay = 0
zy = 0


# ////////////////////////////   FUNCTIONS   ///////////////////////////
def meansensors():
    i = 0
    buff_ax = 0
    buff_ay = 0
    buff_az = 0
    buff_gx = 0
    buff_gy = 0
    buff_gz = 0

    global ax
    global ay
    global az

    global mean_ax
    global mean_ay
    global mean_az
    global mean_gx
    global mean_gy
    global mean_gz

    while (i < (buffer_size + 101)):
        #  read raw accel/gyro measurements from device
        accel_reading = accelgyro.get_acceleration()
        x_accel_reading = accel_reading[0]
        y_accel_reading = accel_reading[1]
        z_accel_reading = accel_reading[2]

        gyro_reading = accelgyro.get_rotation()
        x_gyro_reading = gyro_reading[0]
        y_gyro_reading = gyro_reading[1]
        z_gyro_reading = gyro_reading[2]

        # First 100 measures are discarded
        if (i > 100 and i <= (buffer_size + 100)):
            buff_ax = buff_ax + x_accel_reading
            buff_ay = buff_ay + y_accel_reading
            buff_az = buff_az + z_accel_reading
            buff_gx = buff_gx + x_gyro_reading
            buff_gy = buff_gy + y_gyro_reading
            buff_gz = buff_gz + z_gyro_reading

        if (i == (buffer_size + 100)):
            mean_ax = buff_ax / buffer_size
            mean_ay = buff_ay / buffer_size
            mean_az = buff_az / buffer_size
            mean_gx = buff_gx / buffer_size
            mean_gy = buff_gy / buffer_size
            mean_gz = buff_gz / buffer_size
        i += 1
        time.sleep(2/1000)  # Needed so we don't get repeated measures

    print("meansensor ofsset", mean_ax, mean_ay, mean_az)


# def calibration():
#    global ax_offset
#    global ay_offset
#    global az_offset
#
#    global gx_offset
#    global gy_offset
#    global gz_offset
#
#    ax_offset = -mean_ax / 8
#    ay_offset = -mean_ay / 8
#    az_offset = (16384 - mean_az) / 8
#    print("calibrando offset:", ax_offset, ay_offset, az_offset)
#
#    gx_offset = -mean_gx / 4
#    gy_offset = -mean_gy / 4
#    gz_offset = -mean_gz / 4
#
#    while (1):
#        ready = 0
#        accelgyro.set_x_accel_offset(ax_offset)  # setXAccelOffset(ax_offset)
#        accelgyro.set_y_accel_offset(ay_offset)  # setYAccelOffset(ay_offset)
#        accelgyro.set_z_accel_offset(az_offset)  # setZAccelOffset(az_offset)
#
#        accelgyro.set_x_gyro_offset(gx_offset)  # setXGyroOffset(gx_offset)
#        accelgyro.set_y_gyro_offset(gy_offset)  # setYGyroOffset(gy_offset)
#        accelgyro.set_z_gyro_offset(gz_offset)  # setZGyroOffset(gz_offset)
#
#        meansensors()
#
#        print("")
#        print("Redifiniendo")
#        x = 16384 - mean_az
#        print("meanX: ", mean_ax, "meanY:", mean_ay, "meanZ:", x)
#        print("mean_gx: ", mean_gx, "mean_gy:", mean_gy, "mean_gz:", mean_gz)
#        print("offset acc x, y,z", ax_offset, ay_offset, az_offset,
#              "offset gyro x,y,z", gx_offset, gy_offset, gz_offset)
#
#        if (abs(mean_ax) <= acel_deadzone):
#            ready += 1
#        else:
#            ax_offset = ax_offset-mean_ax / acel_deadzone
#
#        if (abs(mean_ay) <= acel_deadzone):
#            ready += 1
#        else:
#            ay_offset = ay_offset - mean_ay / acel_deadzone
#
#        if (abs(16384-mean_az) <= acel_deadzone):
#            ready += 1
#        else:
#            az_offset = az_offset+(16384-mean_az) / acel_deadzone
#
#        if (abs(mean_gx) <= giro_deadzone):
#            ready += 1
#        else:
#            gx_offset = gx_offset-mean_gx / (giro_deadzone+1)
#
#        if (abs(mean_gy) <= giro_deadzone):
#            ready += 1
#        else:
#            gy_offset = gy_offset-mean_gy / (giro_deadzone+1)
#
#        if (abs(mean_gz) <= giro_deadzone):
#            ready += 1
#        else:
#            gz_offset = gz_offset-mean_gz / (giro_deadzone+1)
#
#        if (ready == 6):
#            return True

def calibration():
    global ax_offset
    global ay_offset
    global az_offset

    global gx_offset
    global gy_offset
    global gz_offset

    ax_offset = -mean_ax / 32
    ay_offset = -mean_ay / 32
    az_offset = (16384 - mean_az) / 32
    print("calibrando offset:", ax_offset, ay_offset, az_offset)

    gx_offset = -mean_gx / 8
    gy_offset = -mean_gy / 8
    gz_offset = -mean_gz / 8

    while (1):
        ready = 0
#        if(mean):
        accelgyro.set_x_accel_offset(ax_offset)  # setXAccelOffset(ax_offset)
        accelgyro.set_y_accel_offset(ay_offset)  # setYAccelOffset(ay_offset)
        accelgyro.set_z_accel_offset(az_offset)  # setZAccelOffset(az_offset)

        accelgyro.set_x_gyro_offset(gx_offset)  # setXGyroOffset(gx_offset)
        accelgyro.set_y_gyro_offset(gy_offset)  # setYGyroOffset(gy_offset)
        accelgyro.set_z_gyro_offset(gz_offset)  # setZGyroOffset(gz_offset)

        meansensors()

        print("")
        print("Redifiniendo")
        x = 16384 - mean_az
        print("meanX: ", mean_ax, "meanY:", mean_ay, "meanZ:", x)
        print("mean_gx: ", mean_gx, "mean_gy:", mean_gy, "mean_gz:", mean_gz)
        print("offset acc x, y,z", ax_offset, ay_offset, az_offset,
              "offset gyro x,y,z", gx_offset, gy_offset, gz_offset)

        if (abs(mean_ax) <= acel_deadzone):
#            ax_offset += 1
            ready += 1
        else:
            ax_offset = ax_offset-mean_ax / acel_deadzone

        if (abs(mean_ay) <= acel_deadzone):
#            ay_offset += 1
            ready += 1
        else:
            ay_offset = ay_offset - mean_ay / acel_deadzone

        if (abs(16384-mean_az) <= acel_deadzone):
#            az_offset -= 1
            ready += 1
        else:
            az_offset = az_offset+(16384-mean_az) / acel_deadzone

        if (abs(mean_gx) <= giro_deadzone):
            ready += 1
        else:
            gx_offset = gx_offset-mean_gx / (giro_deadzone+1)

        if (abs(mean_gy) <= giro_deadzone):
            ready += 1
        else:
            gy_offset = gy_offset-mean_gy / (giro_deadzone+1)

        if (abs(mean_gz) <= giro_deadzone):
            ready += 1
        else:
            gz_offset = gz_offset-mean_gz / (giro_deadzone+1)

        if (ready == 6):
            return True



# ====================== promedio ========================================
def setup():
    global accelgyro
    # Se inicializa la conexion con el sensor!
    accelgyro = MPU6050(i2c_bus, device_address, ax_offset, ay_offset,
                        az_offset, gx_offset, gy_offset, gz_offset, True)
    cont = 0
    try:
        while (True):
#            print(" medicion : " + str(cont))
            # PASO 1
            print("\nMPU6050 Calibration Sketch")
            print("\nYour MPU6050 should be placed in horizontal position," +
                  "with package letters facing up. \nDon't touch it until" +
                  "you see a finish message.\n")
#            time.sleep(2)
            print("\nReading sensors for first time...")
            meansensors()
#            time.sleep(1)

            # PASO 2
            print("\nCalculating offsets...")
            calibrar = calibration()
            if (calibrar):
                print("calibracion exitosa")
#            time.sleep(1)  # delay(1000)

            # PASO 3
            meansensors()
            print("\nFINISHED!")
            print("\nSensor readings with offsets:\t")
            print(mean_ax)
            print("\t")
            print(mean_ay)
            print("\t")
            print(mean_az)
            print("\t")
            print(mean_gx)
            print("\t")

            print(mean_gy)
            print("\t")
            print(mean_gz)
            print("Your offsets:\t")
            print(ax_offset)
            print("\t")
            print(ay_offset)
            print("\t")
            print(az_offset)
            print("\t")
            print(gx_offset)
            print("\t")
            print(gy_offset)
            print("\t")
            print(gz_offset)
            print("\nData is printed as: acelX acelY acelZ giroX giroY giroZ")
            print("Check that sensor readings are close to 0 0 16384 0 0 0")
            print("If calibration was succesful write down ur offsets so you" +
                  "can set them in your projects using something similar to " +
                  "mpu.setXAccelOffset(youroffset)")

            cont += 1

    except KeyboardInterrupt:
        pass

# se corre con setup()
