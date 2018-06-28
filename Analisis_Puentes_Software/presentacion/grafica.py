# -*- coding: utf-8 -*-

# en teoria la visualización de datos no debe se verse en los nodos segundarios


# tecnica efectiva para hacer graficos apartir de archivos de texto.
# https://www.youtube.com/watch?v=ZmYPzESC5YY
# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl  # para modificar colores de grafica en general

from matplotlib import style
import os
import time


class grafica:
    dataFiles = None

    style.use('fivethirtyeight')
    fig = plt.figure()

    # primero grafico
    grafica1 = fig.add_subplot(1, 1, 1) # fig.add_subplot(111, projection = 'polar')

    # redefine el grosor de las lineas de forma general.
    mpl.rcParams['lines.linewidth'] = 0.5

    '''
    Constructor que recibe:
        nombrePrueba: <<String>>
        nombreSensor: <<String>>
        intervalo:      <<float>>
                        Representa los milisegundos
        if Prueba = true:
            La direccion de los archivos se debe hacer con respecto a este archivo
        else:
            la direccion de los archivos se debe hacer con respecto al archivo de donde se llame este.
            

    '''
    def __init__(self, nombrePrueba, nombreSensor, intervalo,Prueba=False):
        carpeta = "AlmacenPruebas/" + nombrePrueba + "/" 
        arch_acc = nombreSensor + "_Aceleracion.txt"

        if(Prueba):
             carpeta = "../AlmacenPruebas/" + nombrePrueba + "/" 
             arch_acc = nombreSensor + "_Aceleracion.txt"
             
        direcc = carpeta + arch_acc
        self.dataFiles = direcc
        
        self.start(intervalo)
        
    
#    def __init__(self):
#        
#        carpeta = "presentacion/sensor1_Aceleracion.txt"
#        print(os.getcwd())
#        filePath = os.path.relpath(carpeta)
#
#        self.dataFiles = filePath
#        self.start(45)

    def animate(self, i):
        try:
            arch = open(self.dataFiles, 'r')
            graph_data = arch.read()
            lines = graph_data.split('\n')
            arch.close()

            ejeXs = []
            ejeYs = []
            ejeZs = []

##            lista = [4,5,50] #lista[contador] #['a','b','c']
            tiempo = []
            contador = 0
            
            for line in lines:
                if len(line) > 1:
                    x, y, z, t = line.split(',')
                    ejeXs.append(x)
                    ejeYs.append(y)
                    ejeZs.append(z)
                    tiempo.append(t)

##                    contador  +=1

            self.grafica1.clear()

            self.grafica1.plot(tiempo,ejeYs, label='ejeY')
            self.grafica1.plot(tiempo,ejeXs, label='ejeX')
            self.grafica1.plot(tiempo,ejeZs, label='ejeZ')

            self.grafica1.legend()

        except IOError:
            print("error grfica", IOError)

    def start(self, interval):
        # interval is miliseconds
        ani = animation.FuncAnimation(self.fig, self.animate, interval)#=45.45)
        plt.show()

        # https://matplotlib.org/api/_as_gen/matplotlib.animation.FuncAnimation.html?highlight=funcanimation
        # to save: https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/


## PARA CORRER!!!
####
##time.sleep(3)
x = grafica("Prueba #11","sensor2",30,1)

