# -*- coding: utf-8 -*-

# en teoria la visualización de datos no debe se verse en los nodos segundarios


# tecnica efectiva para hacer graficos apartir de archivos de texto.
# https://www.youtube.com/watch?v=ZmYPzESC5YY
# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl  # para modificar colores de grafica en general

from matplotlib import style


class grafica:
    dataFiles = None

    style.use('fivethirtyeight')
    fig = plt.figure()

    # primero grafico
    grafica1 = fig.add_subplot(1, 1, 1)

    # redefine el grosor de las lineas de forma general.
    mpl.rcParams['lines.linewidth'] = 0.5

    def __init__(self, nameFile):
        self.dataFiles = nameFile

    def animate(self, i):
        try:
            graph_data = open(self.dataFiles, 'r').read()
            lines = graph_data.split('\n')
            ejeXs = []
            ejeYs = []
            ejeZs = []

            for line in lines:
                if len(line) > 1:
                    x, y, z = line.split(',')
                    ejeXs.append(x)
                    ejeYs.append(y)
                    ejeZs.append(z)

            self.grafica1.clear()

            self.grafica1.plot(ejeYs, label='ejeY')
            self.grafica1.plot(ejeXs, label='ejeX')
            self.grafica1.plot(ejeZs, label='ejeZ')

            self.grafica1.legend()

        except IOError:
            print("No se pudo leer datos")

    def start(self, interval):
        # interval is miliseconds
        ani = animation.FuncAnimation(self.fig, self.animate, interval)#=45.45)
        plt.show()


# PARA CORRER!!!
x = grafica("vibracion.txt")
# recibe milisengundos
x.start(45)
