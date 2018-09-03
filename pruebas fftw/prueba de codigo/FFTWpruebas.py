# -*- coding: utf-8 -*-
import numpy as np
import threading
from scipy.fftpack import fft
import pyfftw
import time
import multiprocessing as mp

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

cantidadMuestras = 2 **17
print("cantidad de datos:"+ str(cantidadMuestras))
promedio = 0
totalIntentos = 10
_threads = mp.cpu_count()
datos = np.linspace(0.0, 1, cantidadMuestras)

# ================= BUILDER =================
##print("builder fftw3")
##aux = pyfftw.empty_aligned(cantidadMuestras, dtype="float")

##pyfftw.interfaces.cache.enable()
##print("cpus: ",mp.cpu_count())
##
##
##for i in range(totalIntentos):
##    start = time.time()
##
##    fft1 = pyfftw.builders.fft(aux,
##                               planner_effort = 'FFTW_MEASURE',
##                               threads = _threads)
##
##
##    #pyfftw.builders.fft(aux, threads = _threads)
##    aux[:] = datos
##    resultado1 = fft1()
##
##    final = time.time() - start
##    if(i != 0):
##        promedio += final
##
##promedio = promedio / (totalIntentos-1)
##print "duracion {0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000, promedio*1000, cantidadMuestras, _threads)


# ================= NUMPY interface fft w=================
def numpyFftw3(x=False):
    print("\n\tNUMPY interface fftw3")
    promedio = 0
    if(x):
        print("\ncon hilo")
    else:
        print("\nsin hilo")
        
    for i in range(totalIntentos):
        start = time.time()

        # PRIMERO SE LLENA Y SE ALINEA LA LISTA DE RESULTADOS
        a = pyfftw.empty_aligned(cantidadMuestras, dtype='float64', n=16)
        a[:] = datos

        # SEGUNDO SE CALCULA FFT

        resultado2 = pyfftw.interfaces.numpy_fft.fft(a, threads = _threads)
        pyfftw.interfaces.cache.enable()

        final = time.time() - start
        if(i != 0):
            promedio += final

    promedio = promedio / (totalIntentos-1)
    if(x):
        print "\tDuracion con hilo{0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000,promedio*1000, cantidadMuestras, _threads)
    else:
        print "\tDuracion sin hilo{0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000,promedio*1000, cantidadMuestras, _threads)

hilo1 = threading.Thread(target= numpyFftw3, args=(True,))
hilo1.start()
numpyFftw3()

# ================= NUMPY =================
##print("\n NUMPY ")
##promedio = 0
##for i in range(totalIntentos):
##    start = time.time()
##
##    # PRIMERO SE LLENA Y SE ALINEA LA LISTA DE RESULTADOS
###    b = pyfftw.empty_aligned(cantidadMuestras, dtype='complex128', n=16)
##    b = datos
##
##    # SEGUNDO SE CALCULA FFT
##    resultado3 = np.fft.fft(b)
##
##    final = time.time() - start
##    if(i != 0):
##        promedio += final
##
##promedio = promedio / (totalIntentos-1)
##print "duracion {0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000,promedio*1000, cantidadMuestras, _threads)

# ================= NUMPY =================
##print("\n spicy")
##promedio = 0
##for i in range(totalIntentos):
##    start = time.time()
##    resultado4 = fft(datos)
##
##    final = time.time() - start
##    if(i!=0):
##        promedio += final
##
##promedio = promedio / (totalIntentos-1)
##print "duracion {0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000, promedio*1000, cantidadMuestras, _threads)

# ================= fftw =================
#print("\n pyfftw")
#promedio = 0
#for i in range(totalIntentos):
#    start = time.time()
#    resultado4 = fft(datos)
#    a3 = pyfftw.empty_aligned( cantidadMuestras, dtype='complex')
#    b3 = pyfftw.empty_aligned( cantidadMuestras, dtype='float64')
#    resultado5 = pyfftw.FFTW(a3, b3) #, threads = _threads)
#    resultado5 = b3
#    final = time.time() - start
#
#    if(i!=0):
#        promedio += final
#
#promedio = promedio / (totalIntentos-1)
#print "duracion {0:.3f}ms, promedio: {1:.3f}, muestras:{2}, hilos: {3} ".format(final*1000, promedio*1000, cantidadMuestras, _threads)
#
#




# COMPARACION

##print( "results 1 con 4: " + str(np.allclose(resultado4, resultado1)))
##print( "results 2 con 4: " + str(np.allclose(resultado4, resultado2)))
##print( "results 3 con 4: " + str(np.allclose(resultado4, resultado3)))

#   por tanto parece que el mejor es el numpy interface fftw3


