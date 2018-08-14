# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys
import time

from modulo.comunicacion.logicaNRF24L01 import logicaNRF24L01
from presentacion import interfaz as interfaz
from presentacion.graficaACC import graficarVibracion
#from presentacion.graficaFourier import fourier

class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
    comunicacion = logicaNRF24L01()

    def __init__(self):
        super(self.__class__, self).__init__()      # INTERFAZ
        self.setupUi(self)

        # Eventos
        self.pushButton_Iniciar.clicked.connect(self.iniciar_clicked)
        self.pushButton_actualizarNodos.clicked.connect(self.actualizarNodos)
        self.pushButton.clicked.connect(self.visualizarGrafico)

    def actualizar_barStatus(self, msg, duracion, color=False): # (string, segundos(int))
        self.statusBar.clearMessage()
        self.statusBar.showMessage(msg, duracion*1000)  # recibe milisegundos
        if(color):
            self.statusBar.setStyleSheet("color: red;\n font-weight: bold;");
        else:
            self.statusBar.setStyleSheet("color: black;\n font-weight: normal;");

#    def progress_barStatus(self, progressBar):
##        label = QtGui.QLabel()
##        label.setText(msg)
##        self.statusBar.addPermanentWidget(label)
#        self.statusBar.addPermanentWidget(progressBar)
#        self.statusBar.removeWidget(progressBar)

    def get_parametrosConfiguracion(self):
        durac = self.horizontalSlider_Duracion.value()
        filtro = self.radioButton_filtroOn.isChecked()
        frecCorte = self.comboBox_FrecFiltroON.currentText()
        frecMuestreoON = self.comboBox_FrecMuestreoON.currentText()
        frecMuestreoOff = self.comboBox_FrecMuestreoOFF.currentText()
        gUnits = self.radioButton_gUnitsACC.isChecked()

        if(self.radioButton_sensibilidad2gACC.isChecked()):
            sensibAcc = 2
        elif (self.radioButton_sensibilidad4gACC .isChecked()):
            sensibAcc = 4
        elif (self.radioButton_sensibilidad8gACC.isChecked()):
            sensibAcc = 8
        else:
            sensibAcc = 16

        if(self.radioButton_sensibilidad2gGyro.isChecked()):
            sensiGyro = 250
        elif (self.radioButton_sensibilidad4gGyro .isChecked()):
            sensiGyro = 500
        elif (self.radioButton_sensibilidad8gGyro.isChecked()):
            sensiGyro = 1000
        else:
            sensiGyro = 2000

        parametros = {"durac":durac, "filtro":filtro, "frecCorte":frecCorte,
                      "fMuestOn":frecMuestreoON, "fMuestOff":frecMuestreoOff,
                      "gUnits":gUnits, "sensibAcc":sensibAcc, "sensiGyro":sensiGyro,}
        print(parametros)
#        return parametros

    def get_parametrosVisualizacion(self):
        x = self.checkBox_EjeX.isChecked()
        y = self.checkBox_EjeY.isChecked()
        z = self.checkBox_EjeZ.isChecked()
        acc = self.checkBox_AccVector.isChecked()
        vib = self.checkBox_VibracionesVisualizar.isChecked()
        fou = self.checkBox_FourierVisualizar.isChecked()

        return {"x": x, "y": y, "z": z, "rms": acc, "vibrac":vib,"fourier":fou}

    def visualizarGrafico(self):
        opcVisual = self.get_parametrosVisualizacion()
        uds_acc = self.get_parametrosConfiguracion()

        if (uds_acc["g"]): uds_acc = "unidades g"
        else: uds_acc = "m/s2"

        if( not opcVisual["fourier"] and not opcVisual["vibrac"] ):
            msg = "ERROR! Seleccione un tipo de grafica!"
            self.actualizar_barStatus(msg,3,True)

        elif (not opcVisual["x"] and not opcVisual["y"] and not opcVisual["z"] and not opcVisual["rms"]):
            self.actualizar_barStatus("ERROR! Seleccione al menos un eje!",3, True)
        else:
            if (opcVisual["vibrac"]):
                x = graficarVibracion("Prueba 1", "sensor1", uds_acc, opcVisual, 30, 0)
                x.start()
            if (opcVisual["fourier"]):
                y = graficarVibracion("Prueba 1", "sensor1", uds_acc, opcVisual, 30, 0)
                y.start()

    def iniciar_clicked(self):

        self.get_parametrosConfiguracion()
#        if(nodo != ""):
        self.actualizar_barStatus("Recibiendo datos...", 25)
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

#        self.comunicacion.solicitarDatos(tiempoPrueba)


#    def iniciar_clicked(self):
#        nodo = self.comboBox_nombreNodo.currentText()
#        tiempoPrueba = self.horizontalSlider_Duracion.value() # tiempo escogido
#
#        if(nodo != ""):
#            self.actualizar_barStatus("Recibiendo datos...", 25)
#            self.groupBox_UnidadesAcelerometro.setEnabled(False)
#            self.groupBox_UnidadesGiroscopio.setEnabled(False)
#            self.groupBox_FrecMuestreo.setEnabled(False)
#            self.groupBox_FrecCorte.setEnabled(False)
#            self.groupBox_Filtro.setEnabled(False)
#            self.horizontalSlider_Duracion.setDisabled(True)
#            self.pushButton_Iniciar.setEnabled(False)
#            self.pushButton_Detener.setEnabled(True)
#            self.pushButton_actualizarNodos.setEnabled(False)
#            self.pushButton.setEnabled(True)
#
#            self.comunicacion.solicitarDatos(tiempoPrueba) cambiar por parametros
#        else:
#            self.actualizar_barStatus("Error, no hay nodos conectados, Actualice!",5,True)

        '''# obtener texto:
##        user = str(self.line_user.text() ) # para obtener
##        print("user:", user)
##        self.line_password.setText("hola")  # para colocar
##
##        # cambiando texto a qlabel
##        self.label_password.setText("Password")
##        self.label_user.setText("")'''

    def actualizarNodos(self):
        self.pushButton_Iniciar.setEnabled(False)
        self.pushButton_actualizarNodos.setEnabled(False)
        self.actualizar_barStatus("Buscando Nodos...", 15)
        progressBar = QtGui.QProgressBar()
        self.statusBar.addPermanentWidget(progressBar)

        # COMUNICACION
        # busca nodos y actualiza progreso
        self.comunicacion.buscarNodosActivos(progressBar)
        self.statusBar.removeWidget(progressBar) # elimina la barra progreso
        msg = self.comunicacion.get_Estado()     # Resultado de busqueda
        self.actualizar_barStatus(msg, 15)

        # obtener IDs e incorporarlos
        nodosActivos = self.comunicacion.get_listNodosObjectActivos()
        for nodo in nodosActivos:
            self.comboBox_nombreNodo.addItem(nodo.getNameID())
#        self.comboBox_nombreNodo.addItem('12')
        self.pushButton_actualizarNodos.setEnabled(True)
        self.pushButton_Iniciar.setEnabled(True)

def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
