# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl

from matplotlib import style
import os
import time


class graficarVibracion:
    dataFiles = None
    style.use("seaborn-white")

    mpl.rcParams['savefig.bbox']='standard'
    mpl.rcParams['axes.grid']=True
    mpl.rcParams['grid.linestyle']='-'
    mpl.rcParams['grid.linewidth']=0.2
    mpl.rcParams['grid.color']='k'
    mpl.rcParams['axes.edgecolor']='black'
    mpl.rcParams['axes.linewidth']=1
    mpl.rcParams['figure.figsize'] = [5.0, 6.0]
    mpl.rcParams['figure.dpi'] = 80
    mpl.rcParams['lines.linewidth'] = 0.5 # redefine el grosor de las lineas

    nombreSensor = ""
    units = ""
    diccAxisChecked = None
    interval = 30
    nombrePrueba = None
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
    def __init__(self, nombrePrueba, nombreSensor,unidades, diccEjesChecked, intervalo,Prueba=False):

        self.nombrePrueba = nombrePrueba
        carpeta = "almacenPruebas/" + nombrePrueba + "/"
        arch_acc = nombreSensor + "_Aceleracion.txt"
        self.nombreSensor = nombreSensor
        self.units = unidades
        self.diccAxisChecked = diccEjesChecked

        if(Prueba):
             carpeta = "../almacenPruebas/" + nombrePrueba + "/"
             arch_acc = nombreSensor + "_Aceleracion.txt"

        direcc = carpeta + arch_acc
        self.dataFiles = direcc
        self.interval = intervalo

#    def __init__(self):
#
#        carpeta = "presentacion/sensor1_Aceleracion.txt"
#        print(os.getcwd())
#        filePath = os.path.relpath(carpeta)
#        self.dataFiles = filePath
#        self.start(45)

    def graficar(self, grafica, nombreEje,  DatosX, DatosY):
        grafica.plot(DatosX, DatosY)
        grafica.set_xlabel('Time (s)', fontsize=8)
        titulo = 'Vibration (' + self.units + ')'
        grafica.set_ylabel(titulo, fontsize=8)
        grafica.set_title(nombreEje, fontsize=8)

    def insertAxis(self, graph_data):
        lines = graph_data.split('\n')
        ejeXs = []
        ejeYs = []
        ejeZs = []
        tiempo = []
        ejeARms = []

        for line in lines:
            if len(line) > 1:
                x, y, z, aRms, t = line.split(',')
                ejeXs.append(x)
                ejeYs.append(y)
                ejeZs.append(z)
                ejeARms.append(aRms)
                tiempo.append(t)

        self.grafica.clear()
        if(self.diccAxisChecked["x"]):
            self.grafica.plot(tiempo,ejeXs, label="ejeX")
        if(self.diccAxisChecked["y"]):
            self.grafica.plot(tiempo,ejeYs, label="ejeY")
        if(self.diccAxisChecked["z"]):
            self.grafica.plot(tiempo,ejeZs, label="ejeZ")
        if(self.diccAxisChecked["rms"]):
            self.grafica.plot(tiempo,ejeARms, label="AccRms")

    def animate(self, i):
        try:
            arch = open(self.dataFiles, 'r')
            graph_data = arch.read()
            arch.close()
            self.insertAxis(graph_data) # habilitar ejes escogidos

            # Etiquetas
            self.grafica.set_title(self.nombreSensor +": Dominio del tiempo", fontsize='large')
            self.grafica.set_xlabel("Tiempo (s)", fontsize='medium')
            self.grafica.set_ylabel("Vibracion ("+ self.units + ')', fontsize='medium')
            leg = self.grafica.legend(loc='best', fontsize = "small", frameon = True, fancybox=True,framealpha = 0.3, ncol =2, edgecolor = "k",  borderpad=0.3)
            for line in leg.get_lines():
                line.set_linewidth(4.0)

        except IOError:
            print("error grfica", IOError)

    def handle_close(self,evt):
        plt.close(self.fig)

    def start(self):
        self.fig = plt.figure()
        self.grafica = self.fig.add_subplot(111)  # fig.add_subplot(111, projection = 'polar')
        self.fig.canvas.set_window_title(self.nombrePrueba)
        self.fig.canvas.mpl_connect('close_event', self.handle_close)

        ani = animation.FuncAnimation(self.fig, self.animate, self.interval) # interval en milisegundos
        plt.show()
        # to save: https://jakevdp.github.io/blog/2012/08/18/matplotlib-animation-tutorial/

x = graficarVibracion("Prueba 1", "sensor1", "g", "x", 30, 0)
x.start()
