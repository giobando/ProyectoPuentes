# -*- coding: utf-8 -*-
#from dispositivo.gy521folder.gy521 import gy521
from dispositivo.gy521folder.mpu6050Hijo import mpu6050Hijo
from datosAlmacen.sd_card import sd_card
#from presentacion.grafica import grafica



from constantes.const import ADDRESS_REG_accA
from constantes.const import ADDRESS_REG_accB
from constantes.const import I2C_ARM
from constantes.const import I2C_VC


import math
import time
from time import sleep
import datetime

# esto es solo para las pruebas!!!
import threading

class modulo:

    '''------------------------------------------------------------------------
    los siguiente metodos van dentro de gestor modulo
    ------------------------------------------------------------------------'''

    bus = 1     # 1 si es i2cArm. 0 GPIO
    address = 0x68
    sensorName = None
    sensorObject = None

    def __init__(self, nombreSensor, numPortAcelerometro, I2C=True):
        '''
        si i2c = true: bus: 1
        si i2c = false: bus: 0
        '''
        try:
            self.sensorName = nombreSensor

            if(numPortAcelerometro == 1):
                # address = 0x68
                self.address = ADDRESS_REG_accA
            elif numPortAcelerometro == 2:
                # address = 0x69
                self.address = ADDRESS_REG_accB
            else:
                print("Lo siento, de momento solo se puede conectar como \n" +
                      "maximo 2 acelerómetro por puerto I2C")
            if I2C:
                self.bus = I2C_ARM
            else:
                self.bus = I2C_VC
            self.sensorObject = mpu6050Hijo(self.address, self.bus, nombreSensor) #gy521(self.address, self.bus, nombreSensor)


        except IOError:
            print("Error, verifique la conexión de los sensores")

    def getSensorObject(self):
        return self.sensorObject

    '''
    Metodo encargado de leer lineas obtenidas de txt de configuracion parametro
    Recibe: lista de palabras: ['sensor1= 1,2,3,4,5,6]
    '''
    def extraerConfiguracionSensor(self, line):
        # se recibe una lista de palabras
        # luego se une todo es una sola linea para eliminar el = y la variable
        numeros = "".join(line).split('=')

        # Se elimina el nombre de la variable y se deja los numeros
        numeros.pop(0)

        datos = []
        numeros = numeros[0].split(',')
        for numero in numeros:
            datos.append(int(numero))
#        print(datos)
        return datos


class test:

    sensorObject = None
    nameTest = None
    temperatura = -1

    def __init__(self, nombrePrueba, sensorObject):
        # ya debe de estar inicializado el sensor
        self.nameTest = nombrePrueba
        self.sensorObject = sensorObject

    def getTime(self):
        dt = datetime.datetime.now()
        return str(dt.hour)+":"+str(dt.minute)+":"+str(dt.second)

    def printTable(self, timeNow, actual_temp, contador, accTotal,
                   inclinacionX, inclinacionY,
                   gyroScaleX, gyroScaleY, gyroScaleZ, accX, accY, accZ,
                   rotX, rotY):

        print(contador, self.sensorObject.sensorName,
              (" %10.2f" % accTotal),
              (" %6.2f" % accX), ("%1.2f" % rotX),
              ("%7.2f" % accY), ("%5.2f" % rotY),
              ("%8.2f" % accZ), ("%1.0f" % 0),
              ("      %5.2f" % gyroScaleX), (" %1.2f" % gyroScaleY),
              (" %1.2f" % gyroScaleZ),
              timeNow,
              ("%1.2f" % inclinacionX), ("%1.2f" % inclinacionY),
              ("%1.2f" % actual_temp))

    '''
    Metodo encargado de calcular la aceleracion total
    Recibe: aceleracion de los 3 ejes, No importa en que unidades este.
    '''
    def calcAceleracionTotal(self, ax, ay, az):
        # para revisar la gravedad es igual 9.8 = sqrt(Ax*Ax + Ay*Ay + Az *Az)
        sumPotAcc = ax * ax + ay * ay + az * az
        return math.sqrt(sumPotAcc)

    '''
    Metodo encargado de las muestras
    Recibe:
        + frec: frecuencia de muestreo en Hz (limite max 1000Hz, mas de esto no
          es posible a menos que se use FIFO que proporciona el sensor)
    '''
    def muestra(self, numMuestra, tiempo, frec, gUnits=True, saveSample=False):

        self.sensorObject.set_frecMuestreoAcc(frec)

        acc =  self.sensorObject.get_acc_data(gUnits) # si no tiene parametros, retorna m/s2

        gyro = self.sensorObject.get_gyro_data()

        # Leyendo temperatura en grados celsius
        self.temperatura = self.sensorObject.get_temperatura()

        ''' SAMPLES '''
        ax = 0 #acc['x']
        ay = acc['y']
        az = 0 #acc['z']
        gx = gyro['x']
        gy = gyro['y']
        gz = gyro['z']

        '''ROTACION no importa en que unidades se trabaja, da el mismo valor'''
        rotX = self.sensorObject.get_x_rotation(ax, ay, az)
        rotY = self.sensorObject.get_y_rotation(ax, ay, az)
        # no se puede calcular el angulo en Z. ref:
        # https://robologs.net/2014/10/15/tutorial-de-arduino-y-mpu-6050/

        ''' INCLINACION'''
        tiltX = self.sensorObject.get_x_Tilt(ax, ay, az)
        tiltY = self.sensorObject.get_y_Tilt(ax, ay, az)

        accTotal = self.calcAceleracionTotal(ax, ay, az)


        ''' Almacenando informacion '''
        if(saveSample):
            self.saveTXT(ax, ay, az, tiempo, gx, gy, gz, tiltX, tiltY)

#        self.printTable(timeNow, tempEscalado, numMuestra, accTotal,
#                        tiltX, tiltY,
#                        gx, gy, gz, ax, ay, az,
#                        rotX, rotY)

    def saveTXT(self, ax, ay, az, timeNow, rotX_gyro, rotY_gyro, rotZ_gyro, tiltX, tiltY):
        saveMuestra = sd_card(self.sensorObject.sensorName)

        # creando carpeta
        carpetaNueva = self.nameTest
        direcCarpeta = "../Analisis_Puentes_Software/AlmacenPruebas/"
        saveMuestra.crearCarpeta(direcCarpeta + carpetaNueva)

        # Creando archivo para aceleraciones
        arch_Acc = direcCarpeta +self.nameTest +"/"+self.sensorObject.sensorName +"_Aceleracion.txt"
        saveMuestra = sd_card(arch_Acc)
        # guardando aceleraciones en txt
        txt_acc = ""
        txt_acc = str(ax) + "," + str(ay) + "," + str(az) + "," + str(timeNow) + "\n"
        saveMuestra.escribir(txt_acc)
        saveMuestra.cerrar()

        # Creando archivo para gyroscopio
        arch_Gyro = direcCarpeta +self.nameTest +"/"+self.sensorObject.sensorName +"_Gyro.txt"
        saveMuestra2 = sd_card(arch_Gyro)

        # guardando gyroscopio data
        txt_gyro = ""
        txt_gyro = txt_gyro + str(rotX_gyro) + "," + str(rotY_gyro) + ","+ str(rotZ_gyro) + ","
        txt_gyro = txt_gyro +  str(tiltX) + "," + str(tiltY)
        txt_gyro = txt_gyro +  "l" + ","
        txt_gyro = txt_gyro +  "\n"
        saveMuestra2.escribir(txt_gyro)
        saveMuestra2.cerrar()


def printHeader():
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"
    print "|\t\t\t\tAcelerometro\t\t\t\t\t\t\t  ||\t\t\t  Gyroscopio \t\t\t\t\t   |"
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"
    print "|(#) \t   \t\t(g-m/s2)    (g-m/s2) (degree)\t    (g-m/s2) (degree)    (g-m/s2)  \t  ||   \t\t\t\t"+u'\u00b0'+ "/s"+"      \t\t   \t"+ u'\u00b0'+"\t   |"
    print "|contador   sensor \tg_total\t X_out / rotacX\t      Y_out / rotac \tZ_out / rotacZ \t\t  ||   X_out\tY_out \t Z_out \t  Time   |" +"Inclicacion x/y\t temp"
    print "|-------------------------------------------------------------------------------------------------||-----------------------------------------------------------------------|"


def graficar(nombreSensor, nombrePrueba):
    from presentacion.grafica import grafica
    # los graficos no se pueden leer junto con el codigo en esta aplicacion
    grafico_sensor1 = grafica() #"Prueba #1", "sensor1")
#    grafico_sensor1.start(45)   # recibe milisegundos


'''
Encargado de realizar el muestreo
Recibe:
        objecto Prueba (test)
        frecuencia Hz
        duracion (s)
        gUnits = indicar si la aceleracion es en g
        save = para guardar en un txt
'''
def realizarMuestreo(sensorTest, frec, duracion, gUnits=True, save=True):


    contadorMuestras = 0
    print("frecuencia", frec,"Periodo", duracion)
    print("muestras totales", frec * duracion)

    start = time.time()
    tiempoTranscurrido = 0

    while( tiempoTranscurrido < duracion or duracion == -1):

        sensorTest.muestra(contadorMuestras, tiempoTranscurrido, frec, gUnits, save)

#        sleep(float(1)/frec)
        tiempoTranscurrido = time.time() - start
        contadorMuestras += 1
#        print("cantidad muestras", contador)
    print("Muestra finalizada, num de muestras:", contadorMuestras)

def inicializarSensor(sensor1Modulo, sensibilidadSensorA, numFiltro):
    sensorObject = sensor1Modulo.getSensorObject()
    sensorObject.disable_test()  # desacivar el test que viene x default

    sensorObject.set_sensibilidad_acc(sensibilidadSensorA)
    sensorObject.set_sensibilidad_gyro(500)

    # configuracion offset
    archivo = "/home/pi/Desktop/ProyectoPUentes/Analisis_Puentes_Software/configuracionSensorTXT/accelerometro.txt"
    leerConfSensor1 = sd_card(archivo)
    leerConfSensor1.abrirTxt()

    # busqueda del nombre del sensor
    nombreSensorA = sensor1Modulo.sensorName
    configSensor1 = leerConfSensor1.devolverLineaDePalabraEncontrada(nombreSensorA)
    leerConfSensor1.cerrar()

    offset_to_sensor1 = sensor1Modulo.extraerConfiguracionSensor(configSensor1)

    # configuracion de los offset
    offset_ax = offset_to_sensor1[0]
    offset_ay = offset_to_sensor1[1]
    offset_az = offset_to_sensor1[2]
    offset_gx = offset_to_sensor1[3]
    offset_gy = offset_to_sensor1[4]
    offset_gz = offset_to_sensor1[5]
    sensorObject.set_offset(offset_ax, offset_ay, offset_az,
                            offset_gx, offset_gy, offset_gz)

    print("nuevos offset")
    sensorObject.get_offset_acc()
    sensorObject.get_offset_gyro()

    sensorObject.set_filtroPasaBaja(numFiltro)       # pruebas


def main():
    '''========================        SENSOR 1       ========================
       --------PARAMETROS----------------------------------------------------'''

    namePrueba = "Prueba #6"    # Para almacenar datos en capeta con ese nombre

#    nombreSensorA = "sensor1"          # nombre sensor
#    puertoConectado = 2                # 1= 0x68 o 2 = 0x69
#    sensibilidadSensorA = 2            # sensiblidades 2,4,8,16

    nombreSensorA = "sensor2"           # nombre sensor
    puertoConectado = 1                 # 1= 0x68 o 2 = 0x69
    sensibilidadSensorA = 2             # sensiblidades 2,4,8,16


    '''--------CONFIGURACION e inicializacion-------------------------------'''
    sensor1Modulo = modulo(nombreSensorA, puertoConectado)

    #    Filtro pasaBaja.
    #   0= 260, 1= 184, 2= 94, 3= 44, 4= 21, 5= 10, 6= 5, 7= reserved  (Hz)
    numFiltro = 0
    frecuencia = 30                     # hz
    duracion = -1                       # -1: indefinidos


#    '''==================== HACER PRUEBAS sensor1 ========================='''
    inicializarSensor(sensor1Modulo, sensibilidadSensorA, numFiltro)
    testsensor1 = test(namePrueba, sensor1Modulo.getSensorObject())
    realizarMuestreo(testsensor1, frecuencia, duracion)










#    print("smplrt ",sensor1.get_rate() )
#    sensor1.set_frecMuestreoAcc(frecuencia) # solo fucniona si se activa el filtro
#    print("smplrt ",sensor1.get_rate() )
#    print("frecu muestre0", sensor1.get_frecMuestreoAcc())

#    print("\n Iniciando en 5 segundo, verifique la informacion anterior")
#    sleep(5)

##    grafico_sensor1 = grafica("Prueba #1", "sensor1", 45,False) #milisengudos
##    t1 = threading.Thread(target=grafica,args=("Prueba #1","sensor1",45,False,))
##    t1.start()

if __name__ == "__main__":
    main()

