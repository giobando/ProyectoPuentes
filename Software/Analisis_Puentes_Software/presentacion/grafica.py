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
    
    # https://tonysyu.github.io/raw_content/matplotlib-style-gallery/gallery.html
    style.use('seaborn-dark') # unos de los mejores!!  
##    style.use("seaborn-white")
        
    fig = plt.figure()
##    fig.subplots_adjust(hspace=0.4, wspace=0.2)
    mpl.rcParams['savefig.bbox']='standard'
    
    mpl.rcParams['axes.grid']=True
    mpl.rcParams['grid.linestyle']=':'
    mpl.rcParams['grid.linewidth']=0.1
    mpl.rcParams['grid.color']='k'       
    mpl.rcParams['axes.edgecolor']='black'
    mpl.rcParams['axes.linewidth']=1
    mpl.rcParams['figure.figsize'] = [100,100]
    mpl.rcParams['figure.dpi'] = 80
    
    # si quiero un unico grafico
    plt.rc('xtick', color='black', labelsize='medium', direction='out')
    plt.rc('ytick', color='black', labelsize='medium', direction='out')
    plt.xlabel('Time(s)')
    plt.ylabel('Vibration')
##
    grafica = fig.add_subplot(111)  # fig.add_subplot(111, projection = 'polar')

    #si deseo varios graficos
##    graficaX = fig.add_subplot(221)
##    graficaY = fig.add_subplot(222)
##    graficaZ = fig.add_subplot(223)
##    graficaRMS = fig.add_subplot(224)

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
        carpeta = "AlmacenPruebas/" + nombrePrueba + "/" 
        arch_acc = nombreSensor + "_Aceleracion.txt"
        self.nombreSensor = nombreSensor
        
        if(Prueba):
             carpeta = "../AlmacenPruebas/" + nombrePrueba + "/" 
             arch_acc ="sensor_" +nombreSensor + "_Aceleracion.txt"
             
        direcc = carpeta + arch_acc
        self.dataFiles = direcc        
        self.start(intervalo)        
    
#    def __init__(self):
#        
#        carpeta = "presentacion/sensor1_Aceleracion.txt"
#        print(os.getcwd())
#        filePath = os.path.relpath(carpeta)
#        self.dataFiles = filePath
#        self.start(45)

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

##                    contador  +=1
            
            #--------------- Para un grafico -----------------      
            self.grafica.clear()
            self.grafica.plot(tiempo,ejeYs, label="ejeY")
            self.grafica.plot(tiempo,ejeXs, label="ejeX")

##            plt.ylim(ymax=1.01)
##            plt.ylim(ymin=0.99)
            self.grafica.plot(tiempo,ejeARms, label="AccRms")
            self.grafica.plot(tiempo,ejeZs, label="ejeZ")
            
            # Etiquetas
            self.grafica.set_title(self.nombreSensor +": Dominio del tiempo", fontsize='large')
            self.grafica.set_xlabel("Tiempo (s)")
            self.grafica.set_ylabel("Vibracion (g)")       
##            leg = self.grafica.legend(loc='best', fontsize = "small", frameon = False, fancybox=True, ncol =2, framealpha=0.5,facecolor ="xkcd:navy", edgecolor = "k",  shadow=True, borderpad=0.6)
            leg = self.grafica.legend(loc='best', fontsize = "small", frameon = True, fancybox=True,framealpha = 0.3, ncol =2, edgecolor = "k",  borderpad=0.3)
            for line in leg.get_lines():
                line.set_linewidth(4.0)
                
            # ------------- para varios graficos -------------
##            self.graficar(self.graficaY, "eje Y", tiempo,ejeYs)
##            self.graficar(self.graficaX, "eje X", tiempo,ejeXs)
##            self.graficar(self.graficaZ, "eje Z", tiempo,ejeZs)
##            self.graficar(self.graficaRMS, "Vector Acc",tiempo,ejeARms)
            
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
x = grafica("7Agosto","sensor1",30,1)

