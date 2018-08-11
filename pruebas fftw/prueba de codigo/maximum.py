
import numpy as np
import time
import random

cantidadMuestras = 2 ** 15
list1 = random.sample(range(cantidadMuestras), cantidadMuestras)
list2 = np.linspace(0.0, 100, 100)


def get_PeakFFT( dataMagFourierList, frecuencyList, save=True):  
    peakIndex = 0
    peak = 0
    
    for loop in range(cantidadMuestras):
      if loop > 0:
         if dataMagFourierList[loop] > peak :    
           peak = dataMagFourierList[loop]
           peakIndex = loop    
    return peakIndex

print('muestras', cantidadMuestras)

start = time.time()
x = get_PeakFFT(list1,list2)
final = time.time() - start
print("tiempo funcion local:"+str(final*1000))
print("max in",x)
start = time.time()
y = np.argmax(list1)
final = time.time() - start
print("\ntiempo funcion np:"+str(final*1000))
print("max in",y)
