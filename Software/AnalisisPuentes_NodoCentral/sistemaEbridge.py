# -*- coding: utf-8 -*-
from PyQt4 import QtGui
import sys
import datetime

from modulo.comunicacion.logicaNRF24L01 import logicaNRF24L01
from presentacion import interfaz as interfaz
from presentacion.graficaACC import graficarVibracion
# from presentacion.graficaFourier import fourier


class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
    comunicacion = logicaNRF24L01()
    nameTest = ""

    def __init__(self):
        super(self.__class__, self).__init__()      # INTERFAZ
        self.setupUi(self)

        # Eventos
        self.pushButton_Iniciar.clicked.connect(self.iniciar_clicked)
        self.pushButton_actualizarNodos.clicked.connect(self.actualizarNodos)
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

        parametros = {"durac": durac,               # int
                      "filtro": filtro,             # bool
                      "frecCorte": str(frecCorte),  # string(string)
                      "fMuestOn": frecMuestreoON,   # string
                      "fMuestOff": frecMuestreoOff,  # string
                      "gUnits": gUnits,             # boolean
                      "sensAcc": sensibAcc,         # int
                      "sensGyro": sensiGyro,        # int
                      "nameT": self.nameTest}
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
        else:
#            if (opcVisual["vibrac"]):
#                x = graficarVibracion("Prueba 1", "sensor1",
#                                      uds_acc, opcVisual, 30, 0)
#                x.start()
            # se desactiva porque es mas util ver vibraciones.
#            if (opcVisual["fourier"]):
            y = graficarVibracion("Prueba 1", "sensor1", uds_acc, opcVisual, 30, 0)
            y.start()

    def get_time(self):
        dt = datetime.datetime.now()
        day = self.comunicacion.trunk(dt.day, 2, 0)
        month = self.comunicacion.trunk(dt.month, 2, 0)
        hour = self.comunicacion.trunk(dt.hour, 2, 0)
        minute = self.comunicacion.trunk(1, 2, 0)
        second = self.comunicacion.trunk(dt.second, 2, 0)

        return day + month + "_" + hour + minute + second
#        print("time", timeCurrent)

#   # funcion temporal para no esperar que hayan nodos conectados
#    def iniciar_clicked(self):
#        self.nameTest = self.get_time()
#        self.get_parametrosConfiguracion()
#
#        self.actualizar_barStatus("Recibiendo datos...", 25)
#        self.groupBox_UnidadesAcelerometro.setEnabled(False)
#        self.groupBox_UnidadesGiroscopio.setEnabled(False)
#        self.groupBox_FrecMuestreo.setEnabled(False)
#        self.groupBox_FrecCorte.setEnabled(False)
#        self.groupBox_Filtro.setEnabled(False)
#        self.horizontalSlider_Duracion.setDisabled(True)
#        self.pushButton_Iniciar.setEnabled(False)
#        self.pushButton_Detener.setEnabled(True)
#        self.pushButton_actualizarNodos.setEnabled(False)
#        self.pushButton.setEnabled(True)
#
#        parametros = self.get_parametrosConfiguracion()
#        self.comunicacion.solicitarDatos(parametros)

    def iniciar_clicked(self):
        nodo = self.comboBox_nombreNodo.currentText()

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
            self.nameTest = self.get_time()

            parametros = self.get_parametrosConfiguracion()
            self.comunicacion.solicitarDatos(parametros)
        else:
            msg = "Error, no hay nodos conectados, Actualice!"
            self.actualizar_barStatus(msg, 5, True)

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

        # ABRIR COMUNICACION con nodos
        self.comunicacion.buscarNodosActivos(progressBar)
        self.statusBar.removeWidget(progressBar)  # elimina la barra progreso
        msg = self.comunicacion.get_Estado()      # Resultado de busqueda
        self.actualizar_barStatus(msg, 15)

        # obtener IDs e incorporarlos
        nodosActivos = self.comunicacion.get_listNodosObjectActivos()
        self.comboBox_nombreNodo.clear()
        for nodo in nodosActivos:
            self.comboBox_nombreNodo.addItem(nodo.getNameID())
        self.pushButton_actualizarNodos.setEnabled(True)
        self.pushButton_Iniciar.setEnabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()
