# -*- coding: utf-8 -*-



class nodo:
    nameID =  None
    listSensores = None
    addressComunicacion = None

    def __init__(self, name, address):
        self.nameID = name
        self.addressComunicacion = address


    def insertSensor(self, sensor):
        if(sensor not in self.listSensores):   # verifica que no se inserte el mismo sensor.
            self.listSensores.append(sensor)
        else:
            print("El sensor ya esta agregado al nodo", self.name)

    def getListSensores(self):
        return self.listSensores

    def getNameID(self):
        return self.nameID


