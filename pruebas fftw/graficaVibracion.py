# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib as mpl  # para modificar colores de grafica en general

from matplotlib import style
import os
import time

class grafica:
    dataFiles = None
    
    # https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
    style.use('seaborn-dark') # unos de los mejores!!  

    fig = plt.figure()
    
    mpl.rcParams['savefig.bbox']='standard'
    
    mpl.rcParams['axes.grid']=True
    mpl.rcParams['grid.linestyle']=':'
    mpl.rcParams['grid.linewidth']=0.1
    mpl.rcParams['grid.color']='k'       
    mpl.rcParams['axes.edgecolor']='black'
    mpl.rcParams['axes.linewidth']=1
    mpl.rcParams['figure.figsize'] = [100,100]
    mpl.rcParams['figure.dpi'] = 80
    
    grafica = fig.add_subplot(111)
    
    # redefine el grosor de las lineas de forma general.
    mpl.rcParams['lines.linewidth'] = 0.5     
    
    nombreSensor = ""
    
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
        self.fig.canvas.set_window_title(nombrePrueba)
        arch_acc = "sensor_"+nombreSensor + "_Aceleracion.txt"
        self.nombreSensor = nombreSensor
        self.dataFiles = arch_acc #direcc        
        self.start(intervalo)        

    def graficar(self, grafica, nombreEje, DatosX, DatosY):
        grafica.plot(DatosX, DatosY)
        grafica.set_xlabel('Time (s)', fontsize=8)
        grafica.set_ylabel('Vibration (g)', fontsize=8)
        grafica.set_title(nombreEje, fontsize=8)
    
    def animate(self, i):
        try:
            arch = open(self.dataFiles, 'r')
            graph_data = arch.read()
            lines = graph_data.split('\n')
            arch.close()

            ejeXs = []
            ejeYs = []
            ejeZs = []
            tiempo = []
            ejeARms = []
            
            contador = 0
            
            for line in lines:
                if len(line) > 1:
                    x, y, z, aRms, t = line.split(',')
                    ejeXs.append(x)
                    ejeYs.append(y)
                    ejeZs.append(z)
                    ejeARms.append(aRms)
                    tiempo.append(t)
            
            #--------------- Para un grafico -----------------      
            self.grafica.clear()
            self.grafica.plot(tiempo,ejeYs, label="ejeY")
            self.grafica.plot(tiempo,ejeXs, label="ejeX")

            self.grafica.plot(tiempo,ejeARms, label="AccRms")
            self.grafica.plot(tiempo,ejeZs, label="ejeZ")
            
            # Etiquetas
            self.grafica.set_title("Dominio del tiempo. Sensor:"+self.nombreSensor , fontsize='large')
            self.grafica.set_xlabel("Tiempo (s)")
            self.grafica.set_ylabel("Vibracion (g)")       
            leg = self.grafica.legend(loc='best', fontsize = "small", frameon = True, fancybox=True,framealpha = 0.3, ncol =2, edgecolor = "k",  borderpad=0.3)
            for line in leg.get_lines():
                line.set_linewidth(4.0)
                
 
        except IOError:
            print("error grfica", IOError)

    def start(self, interval):
        # interval is miliseconds
        ani = animation.FuncAnimation(self.fig, self.animate, interval)#=45.45)
        
        plt.show()
       
## PARA CORRER!!!
####
##time.sleep(3)
x = grafica("5Agosto","sensor1",1000,1)

