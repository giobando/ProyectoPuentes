# -*- coding: utf-8 -*-
# https://nikolak.com/pyqt-qt-designer-getting-started/
from PyQt4 import QtGui
import sys
import time

from modulo.comunicacion.logicaNRF24L01 import logicaNRF24L01
from presentacion import interfaz as interfaz

class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
    comunicacion = logicaNRF24L01()

    def __init__(self):
        super(self.__class__, self).__init__()      # INTERFAZ
        self.setupUi(self)

        # Eventos
        self.pushButton_Iniciar.clicked.connect(self.iniciar_clicked)
        self.pushButton_actualizarNodos.clicked.connect(self.actualizarNodos)

    def actualizar_barStatus(self, msg, duracion):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(msg, duracion)  # tarda time seg

#    def progress_barStatus(self, progressBar):
##        label = QtGui.QLabel()
##        label.setText(msg)
##        self.statusBar.addPermanentWidget(label)
#        self.statusBar.addPermanentWidget(progressBar)
#        self.statusBar.removeWidget(progressBar)

    def iniciar_clicked(self):
        print("se presionó iniciar")
        '''# obtener texto:
##        user = str(self.line_user.text() ) # para obtener
##        print("user:", user)
##        self.line_password.setText("hola")  # para colocar
##
##        # cambiando texto a qlabel
##        self.label_password.setText("Password")
##        self.label_user.setText("")'''
        self.statusBar.showMessage("Calibrando...", 5000)

    def actualizarNodos(self):
        self.pushButton_actualizarNodos.setEnabled(False)
        self.actualizar_barStatus("Buscando Nodos...", 7000)
        progressBar = QtGui.QProgressBar()
        self.statusBar.addPermanentWidget(progressBar)

        # COMUNICACION
        self.comunicacion.buscarNodosActivos(progressBar)   # busca nodos y actualiza progreso
        self.statusBar.removeWidget(progressBar)    # elimina la barra progreso
        msg = self.comunicacion.get_Estado()
        self.actualizar_barStatus(msg, 15000)       # Resultado de busqueda

        # obtener IDs e incorporarlos
        nodosActivos = self.comunicacion.get_listNodosObjectActivos()
        for nodo in nodosActivos:
            self.comboBox_nombreNodo.addItem(nodo.getNameID())

        self.pushButton_actualizarNodos.setEnabled(True)


def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()
