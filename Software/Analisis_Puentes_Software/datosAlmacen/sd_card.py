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
#            print txt
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
#                    print palabrasPorLinea
                    return palabrasPorLinea
                    break

    def crearCarpeta(self, ruta):
        try:
            os.mkdir(ruta)

        except OSError:
            return "carpeta ya existe"
           # print("Carpeta ya existe")

    #  escribe exista o no, pero no borra
    def escribir(self, txt):
        self.file = open(self.nameTXT,'a')
        self.file.write(txt)
        self.cerrar()



# para correr
#'''SIEMPRE DEBE DE CERRARSE DESPUES DE ABRIRSE PARA NO CONSUMIR MEMORIA'''
#carpeta = "prueba" #"../Analisis_Puentes_Software/datosAlmacen/prueba"
#arch = "h.txt"
#
#x = sd_card(arch)
#x.crearCarpeta(carpeta)
#x.escribir("sfdf")
#x.cerrar()
