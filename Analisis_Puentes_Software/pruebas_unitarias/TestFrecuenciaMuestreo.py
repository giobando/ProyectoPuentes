# -*- coding: utf-8 -*-

import unittest    # 1. llamar libreria
from dispositivo.gestorSensor import gestorSensor


class TestCalibracion(unittest.TestCase): # 3. heredar esto

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

    def test_Frecuencia(self):
        print("Iniciando prueba")
        # Frecuencias que permite configurar correctamente
        frequenciesExactly = [4,5,8,10,15,20,25,30,35,40,45,50,
                              55,62,66,71,76,83,90,100,125,166,
                              200,250,333,500,1000]

        # ejemplo de frecuencias que se intenta configurar y no se permite!
        frequenciesNotExactly = [1,2,6,7,9,11,33,53,95,115,180,
                                 350,400,450,600,700,800]

        # lista de frecuencias a probar
        frecuenciesTest = [4,10,60,95,115,180,333,350,400,500,600,800]

        sensorObject = self.sensor.getSensorObject()
        getFrequencyExactly = []
        getFrequencyNotExactly = []
        sensorObject.set_filtroPasaBaja(4) # o y 7 desactivan el filtro
        for n in frecuenciesTest:
            sensorObject.set_frecMuestreoAcc(n)
            print("frec", n,"smplrt:",sensorObject.get_rate())
            getFrequencyExactly.append(sensorObject.get_frecMuestreoAcc())
        self.assertEqual(getFrequencyExactly, frecuenciesTest)

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
