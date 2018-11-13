# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys
import datetime
import time
import threading

from datosAlmacen.sd_card import sd_card
#from modulo.comunicacion.logicaNRF24L01 import logicaNRF24L01
from takeSamples import gui
from presentacion import interfaz as interfaz
from presentacion.graficaACC import graficarVibracion
from constantes.const import NAME_NODE
from constantes.const import DIRECC_TO_SAVE
from constantes.const import CALIBRATED
# from presentacion.graficaFourier import fourier
from multiprocessing import Process


class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
#    comunicacion = logicaNRF24L01()
    takeSamples = gui()
    nameTest = ""
    arch_parameters = "" # arch para guardar configuracion
    calibrado = CALIBRATED

    def __init__(self):
        super(self.__class__, self).__init__()      # INTERFAZ
        self.setupUi(self)

        # Eventos
        self.pushButton_Iniciar.clicked.connect(self.iniciarButton_clicked)
        self.pushButton_actualizarNodos.clicked.connect(self.actualizarNodo)
        self.pushButton.clicked.connect(self.visualizarGrafico)

    # (string, segundos(int))
    def actualizar_barStatus(self, msg, duracion, color=False):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(msg, duracion*1000)  # recibe milisegundos
        if(color):
            formato = "color: red;\n font-weight: bold;"
            self.statusBar.setStyleSheet(formato)
        else:
            formato = "color: black;\n font-weight: normal;"
            self.statusBar.setStyleSheet(formato)

#    def progress_barStatus(self, progressBar):
##        label = QtGui.QLabel()
##        label.setText(msg)
##        self.statusBar.addPermanentWidget(label)
#        self.statusBar.addPermanentWidget(progressBar)
#        self.statusBar.removeWidget(progressBar)

    def get_parametrosSensibilidadAceleracion(self):
        sensibAcc = 2

        if(self.radioButton_sensibilidad2gACC.isChecked()):
            sensibAcc = 2
        elif (self.radioButton_sensibilidad4gACC .isChecked()):
            sensibAcc = 4
        elif (self.radioButton_sensibilidad8gACC.isChecked()):
            sensibAcc = 8
        else:
            sensibAcc = 16
        self.saveParameters("Sensibilidad de giroscopio",
                            str(sensibAcc)+"g")
        return sensibAcc

    def get_parametrosSensibilidadGyro(self):
        sensiGyro = 250

        if(self.radioButton_sensibilidad2gGyro.isChecked()):
            sensiGyro = 250
        elif (self.radioButton_sensibilidad4gGyro.isChecked()):
            sensiGyro = 500
        elif (self.radioButton_sensibilidad8gGyro.isChecked()):
            sensiGyro = 1000
        else:
            sensiGyro = 2000
        self.saveParameters("Sensibilidad del acelerometro",
                            str(sensiGyro))
        return sensiGyro

    def get_parametroFrecuenciaMuestreo(self):
        frecMuestreo = 10
        if(self.radioButton_filtroOn.isChecked()):
            frecMuestreo = self.comboBox_FrecMuestreoON.currentText()
            self.saveParameters("Frec. de muestreo", str(frecMuestreo) +"Hz" )
        else:
            frecMuestreo = self.comboBox_FrecMuestreoOFF.currentText()
            self.saveParameters("Frec. de muestreo", str(frecMuestreo) +"Hz")

        return int(frecMuestreo)

    def get_parametrosFrecCorte(self):
        frecCorte = -1
        if(self.radioButton_filtroOn.isChecked()):
            frecCorte = self.comboBox_FrecFiltroON.currentText()
            self.saveParameters("Frec. de corte", str(frecCorte))
        else:
            self.saveParameters("Frec. de corte", "Desactivado")
            frecCorte = -1
        return frecCorte

    def get_parametrosDuracion(self):
        durac = -1

        if(self.radioButtonDuracion.isChecked()):
            durac = self.horizontalSlider_Duracion.value()
            self.saveParameters("Duracion", str(durac)+"min")
        else:
            self.saveParameters("Duracion","Continuo")
            self.saveParameters("\tPor tanto, aceleracion minima es",
                                str(self.doubleSpinBox_AccMinima.value())+"g")
            durac = -1

        return durac

    def get_parametroUnidadesAceleracion(self):
        if(self.radioButton_gUnitsACC.isChecked()):
            self.saveParameters("Unidades de aceleracion","g")
        else:
            self.saveParameters("Unidades de aceleracion", "m/s2")


    def get_parametrosConfiguracion(self):
        frecCorte = self.get_parametrosFrecCorte()
        gUnits = self.radioButton_gUnitsACC.isChecked()
        sensibAcc = self.get_parametrosSensibilidadAceleracion()
        sensiGyro = self.get_parametrosSensibilidadGyro()
        frecMuestreo = self.get_parametroFrecuenciaMuestreo()
        durac = self.get_parametrosDuracion()

        parametros = {"durac": durac,               # int
                      "frecCorte": str(frecCorte),  # string
                      "fMuestOn": frecMuestreo,     # int
                      "gUnits": gUnits,             # boolean
                      "sensAcc": sensibAcc,         # int
                      "sensGyro": sensiGyro,        # int
                      "nameTest": self.nameTest
                      }
        return parametros

    def get_parametrosVisualizacion(self):
        x = self.checkBox_EjeX.isChecked()
        y = self.checkBox_EjeY.isChecked()
        z = self.checkBox_EjeZ.isChecked()
        acc = self.checkBox_AccVector.isChecked()
        vib = self.checkBox_VibracionesVisualizar.isChecked()
        fou = self.checkBox_FourierVisualizar.isChecked()

        return {"x": x, "y": y, "z": z,
                "rms": acc, "vibrac": vib,
                "fourier": fou}

    # falta incluir la grafica de fourier!
    def visualizarGrafico(self):
        opcVisual = self.get_parametrosVisualizacion()
        uds_acc = self.get_parametrosConfiguracion()
        nameTest = self.nameTest
        sensorName = self.comboBox_nombreSensor.currentText()
        nombreNodo = self.comboBox_nombreNodo.currentText()

        if (uds_acc["gUnits"]):
            uds_acc = "g"
        else:
            uds_acc = "m/s2"

        if(not opcVisual["fourier"] and not opcVisual["vibrac"]):
            msg = "ERROR! Seleccione un tipo de grafica!"
            self.actualizar_barStatus(msg, 3, True)
        elif (not opcVisual["x"] and
              not opcVisual["y"] and
              not opcVisual["z"] and
              not opcVisual["rms"]):
            msg = "ERROR! Seleccione al menos un eje!"
            self.actualizar_barStatus(msg, 3, True)
#        else:
#            if (opcVisual["vibrac"]):
#                x = graficarVibracion("Prueba 1", "sensor1",
#                                      uds_acc, opcVisual, 0)
#                x.start()
            # se desactiva porque es mas util ver vibraciones.
#            if (opcVisual["fourier"]):
#            vibracion = graficarVibracion(nameTest, nombreNodo, sensorName,
#                                          uds_acc, opcVisual, False)
#            vibracion.start()

    ''' define la cantidad de caracteres de un numero:
        si el numero es mas largo que el limite indicado no se corta'''
    def trunk(self, numero, cantEnteros=1, cantDecimales=4):
        cantEnteros = cantEnteros + cantDecimales  # cantidad de digitos
#        string = "%"+str(enteros)+"."+str(decimales)+"f"
        string = "%."+str(cantDecimales)+"f"
        string = string % float(numero)
        string = str(string).zfill(cantEnteros)
        return string

    def get_time(self):
        dt = datetime.datetime.now()
        day = self.trunk(dt.day, 2, 0)
        month = self.trunk(dt.month, 2, 0)
        hour = self.trunk(dt.hour, 2, 0)
        year = self.trunk(dt.year, 2, 0)
        minute = self.trunk(dt.minute, 2, 0)
        second = self.trunk(dt.second, 2, 0)
        #time = day + "-" + month + "-" + year + "_" + hour + "." + minute + "." + second
        return day + month + year + "_" + hour +  minute + second

    def saveParameters(self, variable, atributo):
        txt = variable + "\t:" + atributo + "\n"
        saveMuestra = sd_card(self.arch_parameters)
        saveMuestra.escribir(txt)

    def crearCarpeta(self):
        saveMuestra = sd_card('')
        carpetaNueva = self.nameTest
        saveMuestra.crearCarpeta(DIRECC_TO_SAVE + carpetaNueva)

    def crearArchParameters(self):
        self.arch_parameters = DIRECC_TO_SAVE + self.nameTest + "/"
        self.arch_parameters += "ConfiguracionAlmacenada"

        txt = "\tPARAMETROS DE CONFIGURACION\n\n"
        saveMuestra = sd_card(self.arch_parameters)
        saveMuestra.escribir(txt)

    def deshabilitarBotones(self, deshabilitar=True):
        if(deshabilitar):
            self.groupBox_UnidadesAcelerometro.setEnabled(False)
            self.groupBox_UnidadesGiroscopio.setEnabled(False)
            self.groupBox_FrecMuestreo.setEnabled(False)
            self.groupBox_FrecCorte.setEnabled(False)
            self.groupBox_Filtro.setEnabled(False)
            self.horizontalSlider_Duracion.setDisabled(True)
            self.pushButton_Iniciar.setEnabled(False)
            self.pushButton_Detener.setEnabled(True)
            self.pushButton_actualizarNodos.setEnabled(False)
            self.pushButton.setEnabled(True)
            self.radioButtonDuracion.setEnabled(False)
            self.radioButtonTiempoContinuo.setEnabled(False)
        else:
            self.groupBox_UnidadesAcelerometro.setEnabled(True)
            self.groupBox_UnidadesGiroscopio.setEnabled(True)
            self.groupBox_FrecMuestreo.setEnabled(True)
            self.groupBox_FrecCorte.setEnabled(True)
            self.groupBox_Filtro.setEnabled(True)
            self.horizontalSlider_Duracion.setDisabled(False)
            self.pushButton_Iniciar.setEnabled(True)
            self.pushButton_Detener.setEnabled(False)
            self.pushButton_actualizarNodos.setEnabled(True)
            self.pushButton.setEnabled(False)
            self.radioButtonDuracion.setEnabled(True)
            self.radioButtonTiempoContinuo.setEnabled(True)
            self.pushButton_Detener.setEnabled(False)

    def iniciarButton_clicked(self):
        nodo = self.comboBox_nombreNodo.currentText()
        sensor = self.comboBox_nombreSensor.currentText()

        if(nodo != "" or sensor != ""):
            self.configurarEntorno()
#            threading.Thread(target= self.visualizarGrafico ).start()
#            hilo22 = threading.Thread(target= self.takeSamples.runTakeSample,
#                                       args=(parametros,))

#            self.visualizarGrafico()
        else:
            msg = "Error, no hay sensores conectados, Actualice!"
            self.actualizar_barStatus(msg, 5, True)

    def configurarEntorno(self):
        detener = False

#        self.deshabilitarBotones()
        self.deshabilitarBotones()
        self.actualizar_barStatus("Iniciando toma de muestras...", 1)
        self.nameTest = self.get_time()
        self.crearCarpeta()
        self.crearArchParameters()

        threading.Thread(target=self.IniciarPrueba).start()

    def IniciarPrueba(self):
        parametros = self.get_parametrosConfiguracion()
#        self.deshabilitarBotones(False)
        detener = False

        # iniciar datos
        detener = self.takeSamples.runTakeSample(parametros)

        if(detener):
            self.actualizar_barStatus("Muestras Finalizado", 2)
            self.deshabilitarBotones(False)

    def get_sensorConectado(self):
        msg = ""

        # OBTENER SENSORES CONECTADOS
        self.comboBox_nombreSensor.clear()
        if(not self.takeSamples.booleanPort1 and
           not self.takeSamples.booleanPort2):
            msg = "Sensores no conectados"
        else:
            if(self.takeSamples.booleanPort1):
                self.comboBox_nombreSensor.addItem(
                        self.takeSamples.nameSensor1)
            else:
                msg = "Sensor 1 no conectado"

            if(self.takeSamples.booleanPort2):
                self.comboBox_nombreSensor.addItem(
                        self.takeSamples.nameSensor2)
            else:
                msg = "Sensor 2 no conectado"
        self.actualizar_barStatus(msg, 2)

    def actualizarNodo(self):
        global calibrado
        try:
            self.takeSamples = gui()
            self.pushButton_Iniciar.setEnabled(False)
            self.pushButton_actualizarNodos.setEnabled(False)
            self.actualizar_barStatus("Actualizando sensores...", 2)
#            progressBar = QtGui.QProgressBar()
#            self.statusBar.addPermanentWidget(progressBar)
            self.get_sensorConectado()
#            self.statusBar.removeWidget(progressBar)  # remove progress bar

            # obtener ID
            self.comboBox_nombreNodo.clear()
            self.comboBox_nombreNodo.addItem(str(NAME_NODE))
            self.pushButton_actualizarNodos.setEnabled(True)
            self.pushButton_Iniciar.setEnabled(True)
        except:
            msg = "Error, intentelo de nuevo!"
            self.actualizar_barStatus(msg, 5, True)
            self.pushButton_Iniciar.setEnabled(True)
            self.pushButton_actualizarNodos.setEnabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
