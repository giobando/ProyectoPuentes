
#tecnica efectiva para hacer graficos apartir de archivos de texto.
# https://www.youtube.com/watch?v=ZmYPzESC5YY

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style

style.use('fivethirtyeight')
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)


def animate(i):
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
    ax1.plot(xs,label = 'ejeX')
    ax1.plot(ys,label = 'ejeY')
    ax1.plot(zs,label = 'ejeZ')

##    ax1.xlabel("x label")
##    ax1.ylabel("y label")
##    ax1.title('aceleracion [g]')
##    ax.legend(loc='center left', bbox_to_anchor=(0.9, 0.5))
    ax1.legend()

ani = animation.FuncAnimation(fig, animate,interval = 45.45) # interval is miliseconds
plt.show()
