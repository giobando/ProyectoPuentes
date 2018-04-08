#!/usr/bin/python
# -*- coding: utf-8 -*-

#https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/

import smbus
import math
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c

#caracteristica del sensor en la raspberry.
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect, registro ubicado para el sensor.
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def printTable(gyroX, gyroY, gyroZ, gyroScaleX,gyroScaleY,gyroScaleZ, accX, accY, accZ, accScaleX, accScaleY, accScaleZ, rotX, rotY):
    print ("%6d" % accX), "/",("%1.4f" % accScaleX), "/",("%1.4f" % rotX), ("%10d" % accY), "/", ("%1.4f" % accScaleY), "/",("%1.4f" % rotY), ("%10d" % accZ), "/", ("%1.4f" %  accScaleZ), "/",("%1.4f" % 0), ("%9d" % gyroX), " / ", gyroScaleX , ("%11d" % gyroY), " / ", gyroScaleY,("%11d" % gyroZ), " / ", gyroScaleZ 
    
    
def run():
     
    # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)


##    print "Gyroskop:"
    #Giroscopio
    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)
    gyroScaX = (gyroskop_xout / 131)
    gyroScaY = (gyroskop_yout / 131)
    gyroScaZ = (gyroskop_zout / 131)
    
    print "gyroskop_xout: ", ("%5d" % gyroskop_xout), " escalado: ", (gyroskop_xout / 131)
    print "gyroskop_yout: ", ("%5d" % gyroskop_yout), " escalado: ", (gyroskop_yout / 131)
    print "gyroskop_zout: ", ("%5d" % gyroskop_zout), " escalado: ", (gyroskop_zout / 131)
     
    print "accelerometer:" 

    #acelerometro 
    acelerometer_xout = read_word_2c(0x3b)
    acelerometer_yout = read_word_2c(0x3d)
    acelerometer_zout = read_word_2c(0x3f)

    #escalado de acelerometro
    acelerometer_xout_skaliert = acelerometer_xout / 16384.0
    acelerometer_yout_skaliert = acelerometer_yout / 16384.0
    acelerometer_zout_skaliert = acelerometer_zout / 16384.0

    #rotacion del acelerometro
    rotacionX = get_x_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
    rotacionY = get_y_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
     
    print "xout: ", ("%6d" % acelerometer_xout), " escalado: ", acelerometer_xout_skaliert
    print "yout: ", ("%6d" % acelerometer_yout), " escalado: ", acelerometer_yout_skaliert
    print "zout: ", ("%6d" % acelerometer_zout), " escalado: ", acelerometer_zout_skaliert     
    print "X Rotation: " , get_x_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
    print "Y Rotation: " , get_y_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)


##     %6d MINIMO NUMERO DE ESPACIO EN BLANCO ANTES DEL NUMERO
    print "|-----------------------------------------------------------------------------------------------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro \t\t\t\t\t\t||\t\t\t Gyroscopio \t\t\t|"
    print "|  X_out / Scale / rotac \t  Y_out / Scale / rotac \tZ_out / Scale / rotacZ \t||   X_out / Scale \t Y_out / Scale \t Z_out / Scale\t|"
    print "|---------------------------------------------------------------------------------------||------------------------------------------------------|"
    

    printTable(gyroskop_xout,gyroskop_yout,gyroskop_zout,gyroScaX,gyroScaY,gyroScaZ,acelerometer_xout,acelerometer_yout,acelerometer_zout, acelerometer_xout_skaliert,acelerometer_yout_skaliert,acelerometer_zout_skaliert,rotacionX,rotacionY)  
   


   
    

    

run()
