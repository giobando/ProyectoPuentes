# -*- coding: utf-8 -*-

import unittest    # 1. llamar libreria
from dispositivo.gestorSensor import gestorSensor
import time
#from takeSamples import test


class TestCalibracion(unittest.TestCase):  # 3. heredar esto

    '''
    Este metodo asegura que cada prueba se hara con una instancia nueva de
    sensor   '''
    def setUp(self):
        print "\nPreparando contexto para prueba de frecuencia de muestreo"
        nameSensor = "sensor1"
        portConected = 1
        sensibilidadSensor = 2

        # instancia del sensor inicializado
        self.sensor = gestorSensor(nameSensor,
                                   portConected,
                                   sensibilidadSensor)

    def test_FrecuenciaConFiltro(self):
        print("Iniciando prueba configuracion de frecuencia con filtro")
        # Frecuencias que permite configurar correctamente
        frequenciesExactly = [4, 5,8, 10,15, 20,25,30,35, 40, 45, 50, 55,62, 66,71, 76,83,90, 100, 125, 166, 200, 250, 333, 500, 1000]
        # ejemplo de frecuencias que se intenta configurar y no se permite!
        frequenciesNotExactly = [1,2,6,7,9,11,33,53,95,115,180,350,400,450,600,700,800]
        # lista de frecuencias a probar
        frecuenciesTest = [4,10,60,95,115,180,333,350,400,500,600,800]

        sensorObject = self.sensor.getSensorObject()
        getFrequencyExactly = []
        sensorObject.set_filtroPasaBaja(4) # o y 7 desactivan el filtro

        for n in frecuenciesTest:
            sensorObject.set_frecMuestreoAcc(n)
#            print("frec", n,"smplrt:",sensorObject.get_rate())
            getFrequencyExactly.append(sensorObject.get_frecMuestreoAcc())
        self.assertEqual(getFrequencyExactly, frecuenciesTest)
        '''
        con este se comprueba que configura adecuadamente con ciertas frecuencias
#        '''

    def test_FrecuenciaSinFiltro(self):
        print("Iniciando prueba configuracion de frecuencia sin filtro")
        # Frecuencias que permite configurar correctamente
        frequenciesExactly = [4, 5,8, 10,15, 20,25,30,35, 40, 45, 50, 55,62, 66,71, 76,83,90, 100, 125, 166, 200, 250, 333, 500, 1000]
        # ejemplo de frecuencias que se intenta configurar y no se permite!
        frequenciesNotExactly = [1,2,6,7,9,11,33,53,95,115,180,350,400,450,600,700,800]
        # lista de frecuencias a probar
        frecuenciesTest = [4,10,60,95,115,180,333,350,400,500,600,800]

        sensorObject = self.sensor.getSensorObject()
        getFrequencyExactly = []
        sensorObject.set_filtroPasaBaja(0) # o y 7 desactivan el filtro

        for n in frecuenciesTest:
            sensorObject.set_frecMuestreoAccSinFiltro(n)
            print("frec", n,"smplrt:",sensorObject.get_rate())
            getFrequencyExactly.append(sensorObject.get_frecMuestreoAccSinFiltro())
        self.assertEqual(getFrequencyExactly, frecuenciesTest)
        '''
        con este se comprueba que configura adecuadamente con ciertas frecuencias
        '''

    def test_contadorMuestrasSinFiltro(self):
        sensorObject = self.sensor.getSensorObject()
        frequencies = [4,10,15,20,30,40,50 ,66,71,100,115,200,250,350,500,700,800,1000 ]
        tiempoMuestreo = 1.0  # segundos
        print("filtro", 0)
        print("Frec(Hz) \t Muest / smplr  frec Tiempo(s): " + str(tiempoMuestreo))
        sensorObject.set_filtroPasaBaja(0)  # 0 y 7 estan desactivados

        for n in frequencies:
#            sensorObject.set_frecMuestreoAccSinFiltro(n)
            sensorObject.set_frecMuestreoAcc(n)
            startTime = time.time()
            finalTime = 0
            muestrasAcc = []
            ultimoValor = 0

            # tomando muestras del acelerometro + gyro + temperatura
            while(finalTime < tiempoMuestreo):
                acc = sensorObject.get_acc_data(True)  # True: g units
                ax = acc['x']

                if(ultimoValor != ax):
                    ultimoValor = ax
                    muestrasAcc.append(ax)
                finalTime = time.time() - startTime
            smplrt = sensorObject.get_rate()
            numMuestras = len(muestrasAcc)
            frec = sensorObject.get_frecMuestreoAccSinFiltro()
            print(str(n) + "  \t \t" + str(numMuestras) + "\t" + str(smplrt)+"   "+str(frec))

    def test_contadorMuestras_con_Filtro(self):
        sensorObject = self.sensor.getSensorObject()
        frequencies = [4,10,15,20,30,40,50 ,66,71,100,115,200,250,350,500,700,800,1000 ]
        tiempoMuestreo = 1.0  # segundos
        print("filtro", 4)
        print("Frec(Hz) \t Muest / smplr   frec Tiempo(s): " + str(tiempoMuestreo))
        sensorObject.set_filtroPasaBaja(4)  # 0 y 7 estan desactivados

        for n in frequencies:
            sensorObject.set_frecMuestreoAcc(n)
            startTime = time.time()
            finalTime = 0
            muestrasAcc = []
            ultimoValor = 0

            # tomando muestras del acelerometro + gyro + temperatura
            while(finalTime < tiempoMuestreo):
                acc = sensorObject.get_acc_data(True)  # True: g units
                ax = acc['x']

                if(ultimoValor != ax):
                    ultimoValor = ax
                    muestrasAcc.append(ax)
                finalTime = time.time() - startTime
            smplrt = sensorObject.get_rate()
            numMuestras = len(muestrasAcc)
            frec = sensorObject.get_frecMuestreoAcc()
            print(str(n) + "  \t \t" + str(numMuestras) + "\t" + str(smplrt) +"   "+str(frec))

    def tearDown(self):
        print "Desconstruyendo contexto de las prueba de calibracion"
        del self.sensor

if __name__ == '__main__':
    unittest.main()


'''
any member function whose name begins with test in a class deriving from "unittest.TestCase" will be run

This abbreviated output includes the amount of time the tests took,
Tests have 3 possible outcomes:
    ok
    The test passes.

    FAIL
    The test does not pass, and raises an AssertionError exception.

    ERROR
    The test raises an exception other than AssertionError.
'''
