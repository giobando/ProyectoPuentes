# -*- coding: utf-8 -*-
import smbus
import time

# import RPi.GPIO as gpio

# ==============ACELEROMETRO ==============
PWR_M = 0x6B
DIV = 0x19
CONFIG = 0x1A
GYRO_CONFIG = 0x1B
INT_EN = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X = 0x43
GYRO_Y = 0x45
GYRO_Z = 0x47
TEMP = 0x41
bus = smbus.SMBus(1)
Device_Address = 0x68   # device address

AxCal = 0
AyCal = 0
AzCal = 0
GxCal = 0
GyCal = 0
GzCal = 0


def InitMPU():
    bus.write_byte_data(Device_Address, DIV, 7)
    bus.write_byte_data(Device_Address, PWR_M, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    bus.write_byte_data(Device_Address, INT_EN, 1)
    time.sleep(1)


def display(x, y, z):
    x = x * 100
    y = y * 100
    z = z * 100
    x = "%d" % x
    y = "%d" % y
    z = "%d" % z
    print("X     Y     Z", x, y, z)


def readMPU(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value


def accel():
    x = readMPU(ACCEL_X)
    y = readMPU(ACCEL_Y)
    z = readMPU(ACCEL_Z)

#    Ax = (x / 16384.0 - AxCal)
#    Ay = (y / 16384.0 - AyCal)
#    Az = (z / 16384.0 - AzCal)

    #  RECOMENDACION POR ANGEL NAVARRO!!
    Ax = (x / 16384.0) / AxCal
    Ay = (y / 16384.0) / AyCal
    Az = (z / 16384.0) / AzCal

    # print "X="+str(Ax)
    display(Ax, Ay, Az)
    time.sleep(.01)


def gyro():
    global GxCal
    global GyCal
    global GzCal
    x = readMPU(GYRO_X)
    y = readMPU(GYRO_Y)
    z = readMPU(GYRO_Z)
    Gx = x / 131.0 - GxCal
    Gy = y / 131.0 - GyCal
    Gz = z / 131.0 - GzCal

    # print "X="+str(Gx)
    display(Gx, Gy, Gz)
    time.sleep(.01)


def temp():
    tempRow = readMPU(TEMP)
    tempC = (tempRow / 340.0) + 36.53
    tempC = "%.2f" % tempC
    print("temp: ", tempC)
    time.sleep(.2)


def calibrate():
    print("Calibrate")
    global AxCal
    global AyCal
    global AzCal
    precision = 2000

    x = 0
    y = 0
    z = 0
    for i in range(precision):
        if(i > 100):
            x = x + readMPU(ACCEL_X)
            y = y + readMPU(ACCEL_Y)
            z = z + readMPU(ACCEL_Z)
            time.sleep(2/1000)

    # NOMRALIZACION RECOMENDADA POR ANGEL!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    x = x / (precision-100)
    y = y / (precision-100)
    z = z / (precision-100)
    AxCal = x / 16384.0
    AyCal = y / 16384.0
    AzCal = z / 16384.0

    print("AxCal", AxCal)
    print("AyCal", AyCal)
    print("AzCal", AzCal)

    global GxCal
    global GyCal
    global GzCal
    x = 0
    y = 0
    z = 0
    for i in range(precision):
        x = x + readMPU(GYRO_X)
        y = y + readMPU(GYRO_Y)
        z = z + readMPU(GYRO_Z)
    x = x / precision
    y = y / precision
    z = z / precision
    GxCal = x / 131.0
    GyCal = y / 131.0
    GzCal = z / 131.0

    print("GxCal", GxCal)
    print("GyCal", GyCal)
    print("GzCal", GzCal)


print("MPU6050 Interface")
print("Circuit Digest")
time.sleep(2)
InitMPU()
calibrate()
while 1:
    InitMPU()
#    for i in range(20):
#        temp()

    print("\n===================== Accel =====================")
    time.sleep(1)
    for i in range(30):
        accel()
    print("===================== Gyro =====================")
    time.sleep(1)
    for i in range(30):
        gyro()
