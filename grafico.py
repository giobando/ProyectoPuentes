#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Carga de los mÃ³dulos necesarios
##import scipy as sp
##import matplotlib.pyplot as plt

### Creamos el array x de cero a cien con cien puntos
##x = sp.linspace(25, 30, 10)
##
### Creamos el array y conde cada punto es el seno de cada elemento de x
##y = sp.#sin(x)
##
### Creamos una figura
##plt.figure()
##
### Representamos
##plt.plot(x

##import numpy as np
##import matplotlib.pyplot as plt
##
### Compute the x and y coordinates for points on a sine curve
##x = np.arange(0, 3 * np.pi, 0.1)
##y = np.sin(x)
##
### Plot the points using matplotlib
##plt.plot(x, y)
##plt.show()  # You must call plt.show() to make graphics appear.

 # You must call plt.show() to make graphics appear.
 # You must call plt.show() to make graphics appear.
 # You must call plt.show() to make graphics appear.

 # ====================== Opcion 1 ==============================
##import numpy as np
##import matplotlib.pyplot as plt
##
### [ Xinicial, Xfinal, Yinicial, Yfinal
##plt.axis([0, 15, 0, 99])
##
##for i in range(10):
##    y = np.random.random()
##    plt.scatter(i, y)
##    plt.pause(0.05)
##
##plt.show()

# ====================== Opcion 2 ==============================
import matplotlib.pyplot as plt
import numpy as np
plt.ion() ## Note this correction
fig=plt.figure()
plt.axis([0,1000,0,1])

i=0
x=list()
y=list()

while i <1000:
    temp_y=np.random.random();
    x.append(i);
    y.append(temp_y);
    plt.scatter(i,temp_y);
    i+=1;
    plt.show()
    plt.pause(0.0001) #Note this correction, seconds
