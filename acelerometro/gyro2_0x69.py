#!/usr/bin/python
# -*- coding: utf-8 -*-

#https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/
# sensor: gy-521


import smbus
import math
import time
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


#caracteristica del sensor en la raspberry.
#la siguiente linea corresponde al i2c asociado
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x69 #0x68       # via i2cdetect, registro ubicado para el sensor.
 
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


######ver como borrar este y utilizar los que ya se tienen
def read_i2c_word(register):
        """Read two i2c registers and combine them.

            register -- the first register to read from.
            Returns the combined read results.
        """
        # Read the data from the registers
        high = bus.read_byte_data(address, register)
        low = bus.read_byte_data(address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

def printTable(gyroX, gyroY, gyroZ, gyroScaleX,gyroScaleY,gyroScaleZ, accX, accY, accZ, accScaleX, accScaleY, accScaleZ, rotX, rotY):
    print ("%6d" % accX), "/",("%1.4f" % accScaleX), "/",("%1.4f" % rotX), ("%10d" % accY), "/", ("%1.4f" % accScaleY), "/",("%1.4f" % rotY), ("%10d" % accZ), "/", ("%1.4f" %  accScaleZ), "/",("%1.4f" % 0), ("%9d" % gyroX), " / ", gyroScaleX , ("%11d" % gyroY), " / ", gyroScaleY,("%11d" % gyroZ), " / ", gyroScaleZ 
    
    
def run():
     
    # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)

    #Giroscopio
    gyroX = read_word_2c(0x43)
    gyroY = read_word_2c(0x45)
    gyroZ = read_word_2c(0x47)
    
    #Lo sisguiente consiste en el escalado, al ser default de -250°/s para el giroscopio, con lectura de 32768 para ese default se escala a unidadesd de giroscopio es decir a grados por seg (°/s)
    #estos valores corresponden a los valores default 
    gyroScaX = gyroX * (250 / 32768 )
    gyroScaY = gyroY * (250 / 32768 )
    gyroScaZ = gyroZ * (250 / 32768 )
##    print "gyroX: ", ("%5d" % gyroX), " escalado: ", (gyroX / 131)
##    print "gyroY: ", ("%5d" % gyroY), " escalado: ", (gyroY / 131)
##    print "gyroZ: ", ("%5d" % gyroZ), " escalado: ", (gyroZ / 131)

    

    '''----------------------ACELEROMETRO---------------------------
    Sensibilidad: 2g por default.


    '''
    #ver otros ejemplos si lo que se reciben son LSB/g para ver si habria que escalarlo.
    acelerometer_xout = read_word_2c(0x3b)
    acelerometer_yout = read_word_2c(0x3d)
    acelerometer_zout = read_word_2c(0x3f)
    
    #escalado de acelerometro: devuelve la lectura del acelerometro en unidades m/s2
    #si se cambia la sensibilidad de este sensor (2g) se debe de cambiar el 16384!!
     #para obtener el dato:https://hetpro-store.com/TUTORIALES/modulo-acelerometro-y-giroscopio-mpu6050-i2c-twi/
    #la formula se obtiene de este punto
    #ejemplo de escalado.
    #este se obtiene m/s2
    acelerometer_xout_skaliert = acelerometer_xout * (9.81 / 16384.0 ) #este valor se debe a que la sensibilidad esta en 2g que correspode a este valor en bit segun https://hetpro-store.com/TUTORIALES/modulo-acelerometro-y-giroscopio-mpu6050-i2c-twi/
    acelerometer_yout_skaliert = acelerometer_yout * (9.81 / 16384.0 )
    acelerometer_zout_skaliert = acelerometer_zout * (9.81 / 16384.0 )

    #rotacion del acelerometro
    rotacionX = get_x_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
    rotacionY = get_y_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
    rotacionZ = 0 # no se puede calcular el angulo en Z. https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

## acelerometro
##    print "xout: ", ("%6d" % acelerometer_xout), " escalado: ", acelerometer_xout_skaliert
##    print "yout: ", ("%6d" % acelerometer_yout), " escalado: ", acelerometer_yout_skaliert
##    print "zout: ", ("%6d" % acelerometer_zout), " escalado: ", acelerometer_zout_skaliert     
##    print "X Rotation: " , get_x_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)
##    print "Y Rotation: " , get_y_rotation(acelerometer_xout_skaliert, acelerometer_yout_skaliert, acelerometer_zout_skaliert)


   


    printTable(gyroX,gyroY,gyroZ,gyroScaX,gyroScaY,gyroScaZ,acelerometer_xout,acelerometer_yout,acelerometer_zout, acelerometer_xout_skaliert,acelerometer_yout_skaliert,acelerometer_zout_skaliert,rotacionX,rotacionY)  
   
def main():

##     %6d MINIMO NUMERO DE ESPACIO EN BLANCO ANTES DEL NUMERO
    print "|-----------------------------------------------------------------------------------------------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro \t\t\t\t\t\t||\t\t\t Gyroscopio \t\t\t|"
    print "|  X_out / Scale / rotac \t  Y_out / Scale / rotac \tZ_out / Scale / rotacZ \t||   X_out / Scale \t Y_out / Scale \t Z_out / Scale\t|"
    print "|---------------------------------------------------------------------------------------||------------------------------------------------------|"

    
    """
        Reads the temperature from the onboard temperature sensor of the MPU-6050.
    
        Returns the temperature in degrees Celcius.
    """
     #Rango de temperatura: -40 a 85C.
    TEMP_OUT0 = 0x41
    raw_temp = read_i2c_word(TEMP_OUT0)

    # Get the actual temperature using the formule given in the
    # MPU-6050 Register Map and Descriptions revision 4.2, page 30
    actual_temp = (raw_temp / 340.0) + 36.53

    print "temperatura actual", actual_temp

    
    while(True):
        run()
        time.sleep(1*0.045) # segundos
        

##main()






        

    

