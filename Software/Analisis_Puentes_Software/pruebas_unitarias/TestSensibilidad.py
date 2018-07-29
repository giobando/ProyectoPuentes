# -*- coding: utf-8 -*-

import unittest
from dispositivo.gestorSensor import gestorSensor


class TestCalibracion(unittest.TestCase):

    '''
    este metodo asegura que cada prueba se hara con una instancia nueva de
    sensor   '''
    def setUp(self):
        print "\nPreparando contexto para prueba de sensibilidad"
        nameSensor = "sensor1"
        portConected = 1
        sensibilidadSensor = 2

        self.sensor = gestorSensor(nameSensor,
                                   portConected,
                                   sensibilidadSensor)

    def test_setSensibilidadAcc(self):
        newSensibilidad = [2,4,8]
        sensorObject = self.sensor.getSensorObject()

        getSensibilidad = []
        for n in newSensibilidad:
            sensorObject.set_sensibilidad_acc(n)
            getSensibilidad.append(sensorObject.get_sensiblidad_acc())
        self.assertEqual(getSensibilidad, newSensibilidad)

    def tearDown(self):
        print "Desconstruyendo contexto de las prueba de calibracion"
        del self.sensor


if __name__ == '__main__':
    unittest.main()
