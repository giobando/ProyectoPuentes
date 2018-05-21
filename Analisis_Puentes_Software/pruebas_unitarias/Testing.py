# -*- coding: utf-8 -*-

import unittest
import probando

# https://cgoldberg.github.io/python-unittest-tutorial/
# Todos los métodos que comiencen con el nombre test serán ejecutados.


# probando testing
class TestUM(unittest.TestCase):

#    def test_numbers_3_4(self):
#        # self.assertEqual( multiply(3,4), 12)4
#        self.assertEqual(7, 3+4)
#
    def testProbando(self):
        # a = hola()
        a = probando.probando()
        b = a.hola()
        
        self.assertEqual(b, "hola a todos")


if __name__ == '__main__':
    unittest.main()
