# -*- coding: utf-8 -*-
import unittest
import spidev


class spi_test(unittest.TestCase):
    '''
    Para la siguiente prueba es necesario conectar los puertos mosi y miso con un
    cable entre ellos.
    '''

    def setUp(self):
        self.spi = spidev.SpiDev()
        self.spi.open(0, 0)


    def test_speed(self):
        speed = [244*1000*1000]#[125000000]  #,62500000,31200000,15600000,780000,3900000,1953000,976000,488000,244000,122000,61000,35000,30500,15200,8000,7629]

        buf = [0x05, 0xFF]
        buf2 = [0x25, 0x60]
        buf3 = [0x05, 0xFF]

        total = buf+buf2+buf3
        respEsperada = []
        respObtenida = []

        # creado para comparar todos los rsultados con este
        for n in speed:
            respEsperada.append([n,total])

        print("Evaluando el siguiente envio:",total)
        for frec in speed:
            self.spi.max_speed_hz = frec    # Config de frecuencia
            resp = self.spi.xfer2(buf)      # SPI Response
            resp2 = self.spi.xfer2(buf2)
            resp3 = self.spi.xfer2(buf3)
            respObtenida.append([frec,resp+resp2+resp3])

        self.assertEqual(respEsperada, respObtenida)


    def tearDown(self):
        print "Desconstruyendo contexto de las prueba"
        del self.spi


if __name__ == '__main__':
    unittest.main()
