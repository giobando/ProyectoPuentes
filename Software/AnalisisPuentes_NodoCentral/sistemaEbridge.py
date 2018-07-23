# -*- coding: utf-8 -*-
# https://nikolak.com/pyqt-qt-designer-getting-started/
from PyQt4 import QtGui #PyQt4 import QtGui # Import the PyQt4 module we'll need
import sys # We need sys so that we can pass argv to QApplication
#import time

from presentacion import interfaz as interfaz

class sistemaEbrigde(QtGui.QMainWindow, interfaz.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        self.pushButton_Iniciar.clicked.connect(self.iniciar_Presionado)
        self.pushButton_actualizarNodos.clicked.connect(self.botonActualizarPresionado)

    def iniciar_Presionado(self):
        print("se presionó inicar")
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

    def botonActualizarPresionado(self):
        print("se presiono actualizar")
        self.statusBar.showMessage("Buscando Nodos...",5000) # se borrara en 5 seg


def main():
    app = QtGui.QApplication(sys.argv)
    form = sistemaEbrigde()
    form.show()                         # Show the form
    app.exec_()                         # and execute the app


if __name__ == '__main__':              # if we're running file directly and not importing it
    main()                              # run the main function
