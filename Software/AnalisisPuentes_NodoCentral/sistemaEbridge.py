# -*- coding: utf-8 -*-
# https://nikolak.com/pyqt-qt-designer-getting-started/
from PyQt4 import QtGui #PyQt4 import QtGui # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
import time


from modulo.comunicacion.logicaNRF24L01 import logicaNRF24L01

from presentacion import interfaz as interfaz

class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
    comunicacion = None #logicaNRF24L01()
    progress = None #QtGui.QProgressBar()

    # agregar a interfaz> self.setWindowIcon(QtGui.QIcon('pythonlogo.png'))

    def __init__(self):
        # INTERFAZ
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.progress = QtGui.QProgressBar()
        self.progress.setValue(0)

        self.comunicacion = logicaNRF24L01(self.progress)

#        self.pushButton_Iniciar.clicked.connect(self.iniciar_clicked)
        self.pushButton_actualizarNodos.clicked.connect(self.actualizar_Clicked)

    def actualizar_barStatus(self, msg, time):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(msg, time) # tarda time seg

    def progress_barStatus(self,msg, value):
        label = QtGui.QLabel()
        label.setText(msg)
        self.statusBar.addPermanentWidget(label)
        self.statusBar.addPermanentWidget(self.progress)
        self.progress.setValue(value)

    def iniciar_clicked(self):
        print("se presionó iniciar")
        # obtener texto:
##        user = str(self.line_user.text() ) # para obtener
##        print("user:", user)
##        self.line_password.setText("hola")  # para colocar
##
##        # cambiando texto a qlabel
##        self.label_password.setText("Password")
##        self.label_user.setText("")
        self.statusBar.showMessage("Calibrando...",5000) # se borrara en 5 seg
#        self.statusBar.showMessage("hola...")

    def actualizar_Clicked(self):
        #agregando progreso
        self.actualizar_barStatus("Buscando Nodos",7000)
#        label = QtGui.QLabel()
#        label.setText("Buscando Nodos: ")
#        self.statusBar.addPermanentWidget(label)
        self.statusBar.addPermanentWidget(self.progress)

        # COMUNICACION
        self.comunicacion.buscarNodosActivos() # busca nodos y actualiza progreso

        self.statusBar.removeWidget(self.progress) # elimina la barra progreso
        msg = self.comunicacion.get_Estado()
        self.actualizar_barStatus(msg,15000)


def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
