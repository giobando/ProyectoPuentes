# -*- coding: utf-8 -*-
# http://librosweb.es/libro/python/capitulo_3/creando_modulos_empaquetados.html
'''
    Para importar constantes sin el "namespace"
    from constantes.const import constante1, constante2, contante3
    para implementar todas las constantes:
'''
# from Constantes.const import *
# PARA IMPLEMENTAR ALGUNAS CONSTANTES: Y DE PASO Q SE PUEDA VAPLIDAR POR PEP8
from constantes.const import DIRECTION


def hola():
    print "hola a tojdos"
    print "\n imprimeindo constantes"
    print DIRECTION


hola()
