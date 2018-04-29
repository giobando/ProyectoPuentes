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

# =======OBTIENE EL ANGULO DE INCLINACION DE UN EJE POR MEDIO DE 2 EJE========
# math.atan2( y / x ): Return atan(y / x), in radians.  
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)           # convierte a grados un angulo en radianes
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)           # convierte a grados un angulo en radianes


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

def printTable(acc_g, acc_ms2, gyroScaleX,gyroScaleY,gyroScaleZ, accX, accY, accZ, accScaleX, accScaleY, accScaleZ, rotX, rotY):
    print ("%1.2f" %acc_g ),("\t%1.2f" %acc_ms2 ),("\t%1.3f" % accX), "/",("%1.3f" % accScaleX), "/",("%1.3f" % rotX), ("\t%1.3f" % accY), "/", ("%1.3f" % accScaleY), "/",("%1.3f" % rotY), ("\t%1.3f" % accZ), "/", ("%1.3f" %  accScaleZ), "/",("%1.4f" % 0), ("   %1.3f" % gyroScaleX ), ("\t%1.3f" % gyroScaleY),("   %1.3f" % gyroScaleZ ), "// ",time.ctime() 
    
    
def run():
     
    # Activar para poder abordar el módulo //# Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)

    #Giroscopio
    gyroX = read_word_2c(0x43)
    gyroY = read_word_2c(0x45)
    gyroZ = read_word_2c(0x47)
    
    #Lo sisguiente consiste en el escalado, al ser default de -250°/s para el giroscopio, con lectura de 32768 para ese default se escala a unidadesd de giroscopio es decir a grados por seg (°/s)
    #estos valores corresponden a los valores default 
    gyroScaX = gyroX / 131 
    gyroScaY = gyroY / 131 
    gyroScaZ = gyroZ / 131     

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

    #este se obtiene g
    accXout_g = acelerometer_xout / 16384.0 #este valor se debe a que la sensibilidad esta en 2g que correspode a este valor en bit segun https://hetpro-store.com/TUTORIALES/modulo-acelerometro-y-giroscopio-mpu6050-i2c-twi/
    accYout_g = acelerometer_yout / 16384.0
    accZout_g = acelerometer_zout / 16384.0
    #este se obtiene m/s2
    accXout_ms2 = acelerometer_xout * (9.81 / 16384.0 ) #este valor se debe a que la sensibilidad esta en 2g que correspode a este valor en bit segun https://hetpro-store.com/TUTORIALES/modulo-acelerometro-y-giroscopio-mpu6050-i2c-twi/
    accYout_ms2 = acelerometer_yout * (9.81 / 16384.0 )
    accZout_ms2 = acelerometer_zout * (9.81 / 16384.0 )

    #rotacion del acelerometro: revisar este valor ya que se escalo los parametros que recibe!!
    rotacionX = get_x_rotation(accXout_ms2, accYout_ms2, accZout_ms2)
    rotacionY = get_y_rotation(accXout_ms2, accYout_ms2, accZout_ms2)
    rotacionZ = 0 # no se puede calcular el angulo en Z. https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

    #para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
    multAcc_ms2 = accXout_ms2*accXout_ms2 + accYout_ms2*accYout_ms2 + accZout_ms2*accZout_ms2
    revisandoAcc_ms2 = math.sqrt(multAcc_ms2)
    
    multAcc_g = accXout_g*accXout_g + accYout_g*accYout_g + accZout_g*accZout_g
    revisandoAcc_g = math.sqrt( multAcc_g)
## acelerometro
##    print "xout: ", ("%6d" % acelerometer_xout), " escalado: ", accXout_ms2
##    print "yout: ", ("%6d" % acelerometer_yout), " escalado: ", accYout_ms2
##    print "zout: ", ("%6d" % acelerometer_zout), " escalado: ", accZout_ms2     
##    print "X Rotation: " , get_x_rotation(accXout_ms2, accYout_ms2, accZout_ms2)
##    print "Y Rotation: " , get_y_rotation(accXout_ms2, accYout_ms2, accZout_ms2)


   


    printTable(revisandoAcc_g,revisandoAcc_ms2,gyroScaX,gyroScaY,gyroScaZ,accXout_g,accYout_g,accZout_g, accXout_ms2,accYout_ms2,accZout_ms2,rotacionX,rotacionY)  
   
def main():

    """Reads the temperature from the onboard temperature sensor of the MPU-6050.
       Returns the temperature in degrees Celcius."""
    
     #Rango de temperatura: -40 a 85C.
    TEMP_OUT0 = 0x41
    raw_temp = read_i2c_word(TEMP_OUT0)
    # Get the actual temperature using the formule given in the
    # MPU-6050 Register Map and Descriptions revision 4.2, page 30
    actual_temp = (raw_temp / 340.0) + 36.53

    print "temperatura actual", actual_temp
    
##     %6d MINIMO NUMERO DE ESPACIO EN BLANCO ANTES DEL NUMERO
    print "|-------------------------------------------------------------------------------------------------------||------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro \t\t\t\t\t\t\t\t||\t\t\t Gyroscopio \t\t\t|"
    print "|-------------------------------------------------------------------------------------------------------||------------------------------------------------------|"
    print "|(g) \t (m/s2)   (g)     (m/s^2)  (degree)  \t  (g)   (m/s^2) (degree)  \t  (g)   (m/s^2) (degree)|| \t\t\t\t\t\t\t|"
    print "|graved  graved  X_out / Scale / rotac  \t  Y_out / Scale / rotac \tZ_out / Scale / rotacZ \t||   X_out\t Y_out \t   Z_out \t Time\t\t|"
    print "|-------------------------------------------------------------------------------------------------------||------------------------------------------------------|"

    
    

    contador = 0
    while(True):
        run()
        if contador ==22:
            break
##        else:
##            contador+=1
        time.sleep(1/22) # segundos
        

##main()






        

    

