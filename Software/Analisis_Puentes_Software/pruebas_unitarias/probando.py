# -*- coding: utf-8 -*-
# http://librosweb.es/libro/python/capitulo_3/creando_modulos_empaquetados.html
'''
    Para importar constantes sin el "namespace"
    from constantes.const import constante1, constante2, contante3
    para implementar todas las constantes:
'''
# from Constantes.const import *
# PARA IMPLEMENTAR ALGUNAS CONSTANTES: Y DE PASO Q SE PUEDA VAPLIDAR POR PEP8
from constantes.const import *
import time
# import constantes.const as CONST
# from constantes.const import constante as c1, constante2 as c2


class probando:
    def hola(self):
        print "\nhola a tojdos2"
        print "\n imprimeindo constantes"
        print I2C_ARM
        return "hola a todos"

    def sumando(self, a, b):
        print "sumando"
        time.sleep(3)
        res = a + b
        return res




#x = probando()
#x.hola()
