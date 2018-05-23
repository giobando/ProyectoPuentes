
#tecnica efectiva para hacer graficos apartir de archivos de texto.
# https://www.youtube.com/watch?v=ZmYPzESC5YY
# https://matplotlib.org/tutorials/introductory/usage.html#sphx-glr-tutorials-introductory-usage-py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import  matplotlib as mpl # para modificar colores de grafica en general 
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()

# primero grafico
# add subplot with red background
##fig.add_subplot(212, facecolor='r')
# https://matplotlib.org/api/_as_gen/matplotlib.figure.Figure.html?highlight=add_subplot#matplotlib.figure.Figure.add_subplot
# add a polar subplot

# este podria ser util para los angulos
##ax1 = fig.add_subplot(111, projection='polar')

# es como un mapa mundi con sus angulos
##ax1 = fig.add_subplot(111, projection='hammer')
##ax1 = fig.add_subplot(111, projection='aitoff')
##ax1 = fig.add_subplot(111, projection='lambert')

# si no se indica viene este por defaul
##ax1 = fig.add_subplot(111, projection='rectilinear')
# grafico de lineas
ax1 = fig.add_subplot(1,1,1)
 

# redefine el grosor de las lineas de forma general.
mpl.rcParams['lines.linewidth'] = 0.5


def animate(i):
  try:
    graph_data = open('vibracion.txt', 'r').read()
    lines = graph_data.split('\n')
    xs = []
    ys = []
    zs = []

    for line in lines :
        if len(line)>1 :
            x, y, z = line.split(',')
            xs.append(x)
            ys.append(y)
            zs.append(z)

    ax1.clear()
    
    
##    ax1.plot(xs,ys,zs)
##    ax1.plot(xs,label = 'ejeX', linewidth = 4, color = 'green')
    ax1.plot(ys,label = 'ejeY')
    ax1.plot(xs,label = 'ejeX')
    ax1.plot(zs,label = 'ejeZ')


##    ax1.xlabel("x label")
##    ax1.ylabel("y label")
##    ax1.title('aceleracion [g]')
##    ax.legend(loc='center left', bbox_to_anchor=(0.9, 0.5))
    ax1.legend()

  except IOError:
    print("No se pudo leer datos")
    

ani = animation.FuncAnimation(fig, animate,interval = 45.45) # interval is miliseconds
plt.show()
