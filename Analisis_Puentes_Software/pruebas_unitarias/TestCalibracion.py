# -*- coding: utf-8 -*-

import unittest    # 1. llamar libreria
from dispositivo.gestorSensor import gestorSensor
import math


class TestCalibracion(unittest.TestCase): # 3. heredar esto

    '''
    este metodo asegura que cada prueba se hara con una instancia nueva de
    sensor   '''
    def setUp(self):
        print "\nPreparando contexto para prueba calibrar"
        nameSensor = "sensor1"
        portConected = 1
        sensibilidadSensor = 2

        # instancia del sensor inicializado
#        self.sensor = gestorSensor(nameSensor,
#                                   portConected,
#                                   sensibilidadSensor)

    '''
       La calibracion sera exitosa si se obtiene una aceleracio RMS en:
       '1' (en g) o '9.8' (en m/2), Tome en cuenta que estos resultados
       unicamente se obtienen si no hay pertubaciones
    '''
    def test_Calibrar(self):
        # recordar que los parametros de calibrar estan en const.py
        print("Test calibrar")
        sensorObject = self.sensor.getSensorObject()
        self.sensor.calibrarDispositivo()

        # tomar medidas para calcular un promedio
        promedioARMS = 0
        contador = 0
        numMuestras = 100

        while(contador < numMuestras):
            acc = sensorObject.get_acc_data(True)  # true: para unidades en g
            aRMS = math.pow(acc['x'], 2) + math.pow(acc['y'], 2) + math.pow(acc['z'], 2)
            promedioARMS += math.sqrt(aRMS) / numMuestras
            contador += 1

        print("valor promedio acc RMS: ", promedioARMS)
        aRMS_Ideal = 1  # se espera que se tenga un RMS aproximado a 1

        # por lo que la precisión de lo obtenido con lo ideal sera de un 80%
        self.assertAlmostEqual(promedioARMS, aRMS_Ideal, delta = 0.2)

    def tearDown(self):
        print "Desconstruyendo contexto de las prueba de calibracion"
        del self.sensor


if __name__ == '__main__':  # 6. escribir un main
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
