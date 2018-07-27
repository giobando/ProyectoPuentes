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

    def visualizarGrafico(self):
        nodo = self.comboBox_nombreNodo.currentText()

        x = self.checkBox_EjeX.isChecked()
        y = self.checkBox_EjeY .isChecked()
        z = self.checkBox_EjeZ.isChecked()
        acc = self.checkBox_AccVector.isChecked()
        axisChecked = {"x": x, "y": y, "z": z, "rms": acc}

        vib = self.checkBox_VibracionesVisualizar.isChecked()
        fou = self.checkBox_FourierVisualizar.isChecked()

        uds_acc = "g"
        if (self.radioButton_gUnitsACC.isChecked()): # Unidades g
            uds_acc = "g"
        else:
            uds_acc = "m/s2"

        if( not self.checkBox_FourierVisualizar.isChecked() and not self.checkBox_VibracionesVisualizar.isChecked() ):
            self.actualizar_barStatus("ERROR! Seleccione un tipo de grafica!",3,True)
        elif (not x and not y and not z and not acc):
            self.actualizar_barStatus("ERROR! Seleccione al menos un eje!",3, True)
        else:
            if (vib):
                x = graficarVibracion("Prueba 1", "sensor1", uds_acc, axisChecked, 30, 0)
                x.start()
            if (fou):
                y = graficarVibracion("Prueba 1", "sensor1", uds_acc, axisChecked, 30, 0)
                y.start()

    def iniciar_clicked(self):
        nodo = self.comboBox_nombreNodo.currentText()
        tiempoPrueba = self.horizontalSlider_Duracion.value() # tiempo escogido

        if(nodo != ""):
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

            self.comunicacion.solicitarDatos(tiempoPrueba)
        else:
            self.actualizar_barStatus("Error, no hay nodos conectados, Actualice!",5,True)

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
