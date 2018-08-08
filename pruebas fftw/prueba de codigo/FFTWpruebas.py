# -*- coding: utf-8 -*-
import numpy as np
from scipy.fftpack import fft
import pyfftw
import time

'''
 FLAGS: lista de cadenas y es un subconjunto de las banderas que FFTW permite a los planificadores:

'FFTW_ESTIMATE', 'FFTW_MEASURE', 'FFTW_PATIENT' y 'FFTW_EXHAUSTIVE'.
    Estos describen la cantidad cada vez mayor de esfuerzo invertida durante la etapa de planificación para crear la transformación más rápida posible.
    Por lo general, 'FFTW_MEASURE' es un buen compromiso. Si no se pasa ninguna bandera, se usa el valor predeterminado 'FFTW_MEASURE'.

'FFTW_UNALIGNED'.
    Esto le dice a FFTW que no asuma nada sobre la alineación de los datos y la desactivación de cualquier capacidad SIMD (ver a continuación).
    
'FFTW_DESTROY_INPUT'.
    Esto le dice a FFTW que la matriz de entrada se puede destruir durante la transformación, a veces permitiendo que se use un algoritmo más rápido.
    El comportamiento predeterminado es, si es posible, preservar la entrada.
    En el caso de la transformación real 1D hacia atrás, esto puede dar como resultado un golpe de rendimiento.
    En el caso de una transformación real hacia atrás para más de una dimensión, no es posible conservar la entrada, lo que hace que esta bandera esté implícita en ese caso.
  
'FFTW_WISDOM_ONLY'.
    Esto le dice a FFTW que genere un error si no hay un plan para esta transformación y tipo de datos en wisdom.
    Por lo tanto, proporciona un método para determinar si la planificación requeriría un esfuerzo adicional o se puede usar la wisdom en caché.
    Esta bandera debe combinarse con los diversos indicadores de esfuerzo de planificación ('FFTW_ESTIMATE', 'FFTW_MEASURE', etc.);
    si es así, se generará un error si la wisdom derivada de ese nivel de esfuerzo de planificación (o superior) no está presente.
    Si no se usa ninguna bandera de planificación de esfuerzo, se asume el valor predeterminado de 'FFTW_ESTIMATE'.
    Tenga en cuenta que la wisdom es específica para todos los parámetros, incluida la alineación de datos.
    Es decir, si se generó conocimiento con matrices de entrada / salida con una alineación específica, al usar 'FFTW_WISDOM_ONLY' para crear un plan para matrices con cualquier alineamiento diferente, la planificación 'FFTW_WISDOM_ONLY' fallará.
    Por lo tanto, es importante controlar específicamente la alineación de datos para hacer el mejor uso de 'FFTW_WISDOM_ONLY'.
'''

cantidadMuestras = 4
##datos = [0.001708984375,0.0008544921875,0.001708984375,0.00439453125]
promedio = 0
totalIntentos = 10
_threads =4

aux = pyfftw.empty_aligned(cantidadMuestras, dtype='float32')
##x = pyfftw.builders.fft(aux, planner_effort = 'FFTW_MEASURE', threads = _threads)
datos = np.linspace(0.0, 1, cantidadMuestras)


##pyfftw.interfaces.cache.enable()

for i in range(totalIntentos):
  start = time.time()  
 
##  x = fft(datos)
  
  fft = pyfftw.builders.fft(aux, threads = _threads)
  aux[:] = [0.001708984375,0.0008544921875,0.001708984375,0.00439453125]

  resultado = fft()
  final = time.time() - start
##  if(i!=0):
##    promedio += final  
print(resultado)
##promedio = promedio / (totalIntentos-1)
print "duracion {0:.3f}ms, promedio: {1}, muestras:{2}, hilos: {3} ".format(final,promedio*1000, cantidadMuestras, _threads)
