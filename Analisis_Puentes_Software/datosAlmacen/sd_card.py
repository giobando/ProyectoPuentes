'''
    TITLE:      sd_card
    CREATED:    Wed Apr 25 16:34:28 2018
    AUTOR:      Gilbert Obando Quesada  <gilobaqu@gmail.com>


    OBJECTIVE
        + Read txt
        + Write txt
        + Open txt
        + close txt

    NOTES:
        + It is recomendable calibrate this sensor on the temperature where you
          will work.
        + When this sketch is calibrating:
            - Don't touch the sensor.
            - The sensor should be placed in horizontal position.
'''
# https://programminghistorian.org/es/lecciones/trabajar-con-archivos-de-texto

import os


class sd_card:

    # crear y escribir un archivo txt
    nameTXT = None
    file = None

    # se debe de inicializar con el nombre y la extencion del txt
    def __init__(self, name):
        self.nameTXT = name

    # crea nuevo, si existe le pasa por encima
    def crearNuevoTxt(self):
        self.file = open(self.nameTXT, 'w')

    # abre un archivo, si no existe lo crea
#    si no existe no pasa nada
    def abrirTxt(self):
        self.file = open(self.nameTXT)

    def cerrar(self):
        self.file.close()

    # lee documentos existentes!
    def leer(self):
        try:
            self.file = open(self.nameTXT, 'r')
            txt = self.file.read()
            print txt
            return txt

        except IOError:
            print "no existe documento"

    # devuelve la linea de la palabra que se encontro
    def buscar(self, palabraABuscar):
        # lista de oraciones
        linesTotal = self.file.readlines()

        for line in linesTotal:
            # lista de eleentos separados por un espacio o coma
            palabrasPorLinea = line.split(' ')

            for palabra in palabrasPorLinea:
                if(palabraABuscar == palabra):
                    print "Encontrada"
#                    print palabrasPorLinea
#                    return palabrasPorLinea
                    break

    # devuelve la linea de la palabra que se encontro
    def devolverLineaDePalabraEncontrada(self, palabraABuscar):
        # lista de oraciones
        linesTotal = self.file.readlines()

        for line in linesTotal:
            # lista de eleentos separados por un espacio o coma
            palabrasPorLinea = line.split(' ')

            for palabra in palabrasPorLinea:
                if(palabraABuscar == palabra):
                    # remuevo la palabra y el signo = para dejar solo numeros
                    print "\n Encontrada"
                    print palabrasPorLinea
                    return palabrasPorLinea
                    break

    def crearCarpeta(self, ruta):
        try:
            os.mkdir(ruta)

        except OSError:
            print("Carpeta ya existe")

#    //escribe exista o no, pero no borra
    def escribir(self, txt):
        self.file = open(self.nameTXT,'a')
        self.file.write(txt)

##    # colocar este metodo dentro del principal donde se carga los sensores
#    def extraerConfiguracionSensor(self, line):
##        line.remove(palabra)
##        line.remove("=")
#
#        # se recibe una lista de palabras, enteoria unavaribles con valores
#        # luego se une todo es una sola linea para dividirlo por el =
#
#        numeros = "".join(line).split('=')
#        # luego se elimina el nombre de la variable y se deja los numeros
#        numeros.pop(0)
##        print(numeros)
#        datos = []
#        numeros = numeros[0].split(',')
#        for numero in numeros:
#            datos.append(int(numero))
#        print(datos)


# para correr
#'''SIEMPRE DEBE DE CERRARSE DESPUES DE ABRIRSE PARA NO CONSUMIR MEMORIA'''
carpeta = "/home/pi/Desktop/ProyectoPUentes/Analisis_Puentes_Software/datosAlmacen/prueba"
arch = "h.txt"

x = sd_card(arch)
x.crearCarpeta(carpeta)
#### x.cerrar()
#x.abrirTxt()
x.escribir("sfdf")
#### x.crearNuevoTxt()
###x.leer()
#y = x.devolverLineaDePalabraEncontrada("sensor2")
#print("extrayendo numeros")
##x.extraerConfiguracionSensor(y)
x.cerrar()
