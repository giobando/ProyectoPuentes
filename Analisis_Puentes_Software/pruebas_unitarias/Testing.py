# -*- coding: utf-8 -*-

import unittest
import probando.py

#https://cgoldberg.github.io/python-unittest-tutorial/
#Todos los métodos que comiencen con el nombre test serán ejecutados.



#probando testing
class TestUM(unittest.TestCase):
 
    def test_numbers_3_4(self):
        #self.assertEqual( multiply(3,4), 12)4
        self.assertEqual()
        
    def test(self):
       # a = hola()
       a = probando.hola()
       self.assertEqual(a, "hola a todos")
        

        
if __name__ == '__main__':
    unittest.main()
    