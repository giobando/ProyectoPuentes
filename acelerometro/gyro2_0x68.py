#!/usr/bin/python
# -*- coding: utf-8 -*-

#https://tutorials-raspberrypi.com/measuring-rotation-and-acceleration-raspberry-pi/
# sensor: gy-521


import smbus
import math
import time
import datetime
 
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c


#caracteristica del sensor en la raspberry.
#la siguiente linea corresponde al i2c asociado
bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
address = 0x68       # via i2cdetect, registro ubicado para el sensor.

# ESTE YA ESTA EN EL OTRO 
def read_byte(reg):
    return bus.read_byte_data(address, reg)

# ESTE YA ESTA EN EL OTRO 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value

# ESTE YA ESTA EN EL OTRO 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))

# =======OBTIENE EL ANGULO DE ROTACION DE UN EJE POR MEDIO DE 3 EJE========
# https://www.luisllamas.es/arduino-orientacion-imu-mpu-6050/
# math.atan2( y / x ): Return atan(y / x), in radians.  
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)           # convierte a grados un angulo en radianes

def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)           

# =======OBTIENE EL ANGULO DE INCLINACION DE UN EJE POR MEDIO DE 3 EJE========
def get_y_Tilt(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return -math.degrees(radians)           

def get_x_Tilt(x,y,z): #angulo inclinacion
    radians = math.atan2(x, dist(y,z))
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

def printTable(contador,inclinacionX, inclinacionY, acc_g, acc_ms2, gyroScaleX,gyroScaleY,gyroScaleZ, accX, accY, accZ, accScaleX, accScaleY, accScaleZ, rotX, rotY):
##    timeNow = time.strftime("%H:%M:%S", time.localtime())
    
    dt = datetime.datetime.now()
##    print(contador,timeNow, str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)+str(dt.microsecond))
##    print "microsegundos", str(dt.microsecond),", segundos",str(dt.second)
            
    timeNow= str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)+":"+str(dt.microsecond)
    print contador,("  %1.2f" %acc_g ),("\t%1.2f" %acc_ms2 ),(" \t%1.2f" % accX), "/",("%1.2f" % accScaleX), "/",("%1.2f" % rotX), ("%8.2f" % accY), "/", ("%1.2f" % accScaleY), "/",("%5.2f" % rotY),("%10.2f" % accZ), "/", ("%1.2f" %  accScaleZ), "/",("%1.4f" % 0),   ("\t      %1.2f" % gyroScaleX ), ("\t%1.2f" % gyroScaleY),("   %1.2f" % gyroScaleZ ), "// ",timeNow,("\t%1.2f" % inclinacionX ),("\t%1.2f" % inclinacionY )
    
    
def run(contador):
     
    # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)

    '''GIROSCOPIO'''
    gyroX = read_word_2c(0x43)
    gyroY = read_word_2c(0x45)
    gyroZ = read_word_2c(0x47)

    # se divide 131 por el escalado
    gyroScaX = gyroX / 131 
    gyroScaY = gyroY / 131 
    gyroScaZ = gyroZ / 131     

    '''ACELEROMETRO: Sensibilidad: 2g por default, se recibe RAW (valores retornados por el mpu6050) es decir sin escalar '''
    acelerometer_xout = read_word_2c(0x3b)
    acelerometer_yout = read_word_2c(0x3d)
    acelerometer_zout = read_word_2c(0x3f)
    
    '''si se cambia la sensibilidad de este sensor (2g) se debe de cambiar el 16384!! para obtener el dato:https://hetpro-store.com/TUTORIALES/modulo-acelerometro-y-giroscopio-mpu6050-i2c-twi/'''
    #escalado en g 
    accXout_g = acelerometer_xout / 16384.0 
    accYout_g = acelerometer_yout / 16384.0
    accZout_g = acelerometer_zout / 16384.0
    #escalado en m/s2
    accXout_ms2 = acelerometer_xout * (9.81 / 16384.0 )
    accYout_ms2 = acelerometer_yout * (9.81 / 16384.0 )
    accZout_ms2 = acelerometer_zout * (9.81 / 16384.0 )

    # ROTACION no importa en que unidades se trabaja, da el mismo valor
    rotacionX = get_x_rotation(accXout_ms2, accYout_ms2, accZout_ms2)
    rotacionY = get_y_rotation(accXout_ms2, accYout_ms2, accZout_ms2)
    rotacionZ = 0 # no se puede calcular el angulo en Z. https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

    ''' INCLINACION'''
    inclinacionX = get_x_Tilt(accXout_ms2, accYout_ms2, accZout_ms2)
    inclinacionY = get_y_Tilt(accXout_ms2, accYout_ms2, accZout_ms2)
    
    #para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
    multAcc_ms2 = accXout_ms2*accXout_ms2 + accYout_ms2*accYout_ms2 + accZout_ms2*accZout_ms2
    revisandoAcc_ms2 = math.sqrt(multAcc_ms2)    
    multAcc_g = accXout_g*accXout_g + accYout_g*accYout_g + accZout_g*accZout_g
    revisandoAcc_g = math.sqrt( multAcc_g)
 
    printTable(contador, inclinacionX, inclinacionY,revisandoAcc_g,revisandoAcc_ms2,gyroScaX,gyroScaY,gyroScaZ,accXout_g,accYout_g,accZout_g, accXout_ms2,accYout_ms2,accZout_ms2,rotacionX,rotacionY)  
   
def main():
    """Reads the temperature from the onboard temperature sensor of the MPU-6050.
       Returns the temperature in degrees Celcius,Rango de temperatura: -40 a 85C.
       # Get the actual temperature using the formule given in the MPU-6050 Register Map and Descriptions revision 4.2, page 30"""     
    TEMP_OUT0 = 0x41
    raw_temp = read_i2c_word(TEMP_OUT0)
    actual_temp = (raw_temp / 340.0) + 36.53

    print "temperatura actual", actual_temp
    
##     %6d MINIMO NUMERO DE ESPACIO EN BLANCO ANTES DEL NUMERO
    print "|-------------------------------------------------------------------------------------------------||-------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro\t\t\t\t\t\t\t  ||\t\t\t  Gyroscopio \t\t\t   |"
    print "|-------------------------------------------------------------------------------------------------||-------------------------------------------------------|"
    print "|(g) \t(m/s2)    (g)  (m/s^2) (degree)\t    (g)   (m/s^2) (degree)    (g)   (m/s^2) (degree)\t  ||   \t\t\t\t"+u'\u00b0'+ "/s"+"      \t\t   |\t\t"+ u'\u00b0'
    print "|graved  graved  X_out / Scale / rotac\t    Y_out / Scale / rotac \tZ_out / Scale / rotacZ \t  ||   X_out\tY_out \t Z_out \t\t Time\t\t   |" +" \tInclicacion x/y "
    print "|-------------------------------------------------------------------------------------------------||-------------------------------------------------------|"

    contador = 0
    while(True):
        run(contador)
##        if contador ==22:
##            break
##        else:
        contador+=1
        
##        time.sleep(1/2) # segundos
        

##main()
        
