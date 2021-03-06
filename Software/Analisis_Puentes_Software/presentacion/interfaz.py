# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'interfazNodoCentral.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from constantes.const import CORRECTION
from PyQt4 import QtCore, QtGui


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.setEnabled(True)
        MainWindow.resize(450, 410-CORRECTION)  # 27
        font = QtGui.QFont()
        font.setKerning(True)
        MainWindow.setFont(font)
        #  MainWindow.setAutoFillBackground(False)
        MainWindow.setWindowIcon(QtGui.QIcon('../AnalisisPuentes_NodoCentral/imagenes/bridge.png'))
        MainWindow.setStyleSheet(
                _fromUtf8("#MainWindow{\n"
                            "    \n"
                            "    background-color: rgb(227, 227, 227);\n"
                            "}\n"
                            "\n"
                            "QStatusBar{\n"
                            "    background-color: rgb(213, 213, 213);\n"
                            "} QComboBox{text-align: left;}\n"
                            "    \n"
                            "    border: 1px solid  rgb(179, 179, 179);\n"
                            "    \n"
                            ""))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.tabWidget_system = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget_system.setGeometry(
                QtCore.QRect(10, 10, 422, 371-CORRECTION))
        self.tabWidget_system.setObjectName(_fromUtf8("tabWidget_system"))
        self.tab_pruebas = QtGui.QWidget()
        self.tab_pruebas.setObjectName(_fromUtf8("tab_pruebas"))
        self.groupBox = QtGui.QGroupBox(self.tab_pruebas)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 400, 318-CORRECTION))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred,
                                       QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
                self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setStyleSheet(_fromUtf8("#groupBox{\n"
"    border: 1px solid gray;     \n"
"    background-color: rgb(249, 249, 249);\n"
"    border-radius: 3px; \n"
"}"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_titulo1 = QtGui.QLabel(self.groupBox)
        self.label_titulo1.setGeometry(QtCore.QRect(100, 10, 200, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_titulo1.setFont(font)
        self.label_titulo1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_titulo1.setObjectName(_fromUtf8("label_titulo1"))
#        self.label_Titulo2 = QtGui.QLabel(self.groupBox)
#        self.label_Titulo2.setGeometry(QtCore.QRect(80, 30, 79, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
#        self.label_Titulo2.setFont(font)
#        self.label_Titulo2.setAlignment(QtCore.Qt.AlignCenter)
#        self.label_Titulo2.setObjectName(_fromUtf8("label_Titulo2"))
        self.checkBox_FourierVisualizar = QtGui.QCheckBox(self.groupBox)
        self.checkBox_FourierVisualizar.setEnabled(False)
        self.checkBox_FourierVisualizar.setGeometry(QtCore.QRect(305, 115,
                                                                 65, 20))
        self.checkBox_FourierVisualizar.setObjectName(
                _fromUtf8("checkBox_FourierVisualizar"))
        self.label_tituloVisualizarGrafica = QtGui.QLabel(self.groupBox)
        self.label_tituloVisualizarGrafica.setGeometry(QtCore.QRect(210, 36,
                                                                    161, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_tituloVisualizarGrafica.setFont(font)
        self.label_tituloVisualizarGrafica.setObjectName(
                _fromUtf8("label_tituloVisualizarGrafica"))
        self.checkBox_VibracionesVisualizar = QtGui.QCheckBox(self.groupBox)
        self.checkBox_VibracionesVisualizar.setGeometry(QtCore.QRect(225, 115,
                                                                     88, 20))
        self.checkBox_VibracionesVisualizar.setChecked(True)
        self.checkBox_VibracionesVisualizar.setObjectName(
                _fromUtf8("checkBox_VibracionesVisualizar"))
        self.horizontalSlider_Duracion = QtGui.QSlider(self.groupBox)
        self.horizontalSlider_Duracion.setEnabled(True)
        self.horizontalSlider_Duracion.setGeometry(QtCore.QRect(10, 170,
                                                                355, 20))
        self.horizontalSlider_Duracion.setMinimum(1)
        self.horizontalSlider_Duracion.setMaximum(500)
        self.horizontalSlider_Duracion.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_Duracion.setObjectName(
                _fromUtf8("horizontalSlider_Duracion"))
        self.label_DuracionDatos = QtGui.QLabel(self.groupBox)
        self.label_DuracionDatos.setGeometry(QtCore.QRect(375, 180, 31, 16))
        self.label_DuracionDatos.setObjectName(
                _fromUtf8("label_DuracionDatos"))
        self.label_tituloDatosVisualizar = QtGui.QLabel(self.groupBox)
        self.label_tituloDatosVisualizar.setGeometry(QtCore.QRect(10, 36,
                                                                  106, 18))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.label_tituloDatosVisualizar.setFont(font)
        self.label_tituloDatosVisualizar.setObjectName(
                _fromUtf8("label_tituloDatosVisualizar"))
        self.pushButton_actualizarNodos = QtGui.QPushButton(self.groupBox)
        self.pushButton_actualizarNodos.setGeometry(QtCore.QRect(60, 115,
                                                                 61, 23))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.pushButton_actualizarNodos.setFont(font)
        self.pushButton_actualizarNodos.setObjectName(
                _fromUtf8("pushButton_actualizarNodos"))
        self.label_SensorNombre = QtGui.QLabel(self.groupBox)
        self.label_SensorNombre.setGeometry(QtCore.QRect(21, 90, 38, 16))
        self.label_SensorNombre.setObjectName(_fromUtf8("label_SensorNombre"))
        self.label_NodoNombre = QtGui.QLabel(self.groupBox)
        self.label_NodoNombre.setGeometry(QtCore.QRect(21, 63, 29, 16))
        self.label_NodoNombre.setObjectName(_fromUtf8("label_NodoNombre"))
        self.comboBox_nombreNodo = QtGui.QComboBox(self.groupBox)
        self.comboBox_nombreNodo.setGeometry(QtCore.QRect(57, 63, 70, 21))
        self.comboBox_nombreNodo.setObjectName(
                _fromUtf8("comboBox_nombreNodo"))
        self.comboBox_nombreSensor = QtGui.QComboBox(self.groupBox)
        self.comboBox_nombreSensor.setGeometry(QtCore.QRect(57, 90, 70, 22))
        self.comboBox_nombreSensor.setObjectName(
                _fromUtf8("comboBox_nombreSensor"))
        self.pushButton = QtGui.QPushButton(self.groupBox)
        self.pushButtonGraficFile = QtGui.QPushButton(self.groupBox)
        self.pushButton.setGeometry(QtCore.QRect(305, 145, 83, 18))
        self.pushButtonGraficFile.setGeometry(QtCore.QRect(220, 145, 78, 18))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButtonGraficFile.setObjectName(
                _fromUtf8("pushButtonGrafFile"))
        self.pushButton.setEnabled(False)
        self.checkBox_EjeX = QtGui.QCheckBox(self.groupBox)
        self.checkBox_EjeX.setGeometry(QtCore.QRect(205, 63, 55, 17))
        self.checkBox_EjeX.setChecked(True)
        self.checkBox_EjeX.setObjectName(_fromUtf8("checkBox_EjeX"))
        self.checkBox_EjeY = QtGui.QCheckBox(self.groupBox)
        self.checkBox_EjeY.setGeometry(QtCore.QRect(270, 63, 55, 17))
        self.checkBox_EjeY.setChecked(True)
        self.checkBox_EjeY.setObjectName(_fromUtf8("checkBox_EjeY"))
        self.checkBox_EjeZ = QtGui.QCheckBox(self.groupBox)
        self.checkBox_EjeZ.setGeometry(QtCore.QRect(335, 63, 55, 17))
        self.checkBox_EjeZ.setChecked(True)
        self.checkBox_EjeZ.setObjectName(_fromUtf8("checkBox_EjeZ"))
        self.checkBox_AccVector = QtGui.QCheckBox(self.groupBox)
        self.checkBox_AccVector.setEnabled(False)
        self.checkBox_AccVector.setGeometry(QtCore.QRect(205, 88, 116, 16))
        self.checkBox_AccVector.setChecked(True)
        self.checkBox_AccVector.setObjectName(_fromUtf8("checkBox_AccVector"))
        self.radioButtonTiempoContinuo = QtGui.QRadioButton(self.groupBox)
        self.radioButtonTiempoContinuo.setGeometry(QtCore.QRect(140, 145,
                                                                91, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonTiempoContinuo.setFont(font)
        self.radioButtonTiempoContinuo.setObjectName(
                _fromUtf8("radioButtonTiempoContinuo"))
        self.label_VerificaOpcAvanzadas = QtGui.QLabel(self.groupBox)
        self.label_VerificaOpcAvanzadas.setEnabled(True)
        self.label_VerificaOpcAvanzadas.hide()

        self.label_VerificaOpcAvanzadas.setGeometry(QtCore.QRect(50, 180,
                                                                 161, 16))
        font = QtGui.QFont()
        font.setKerning(True)
        self.label_VerificaOpcAvanzadas.setFont(font)
        self.label_VerificaOpcAvanzadas.setObjectName(
                _fromUtf8("label_VerificaOpcAvanzadas"))
        self.radioButtonDuracion = QtGui.QRadioButton(self.groupBox)
        self.radioButtonDuracion.setGeometry(QtCore.QRect(10, 145, 120, 18))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.radioButtonDuracion.setFont(font)
        self.radioButtonDuracion.setChecked(True)
        self.radioButtonDuracion.setObjectName(
                _fromUtf8("radioButtonDuracion"))
        self.checkBox_EjeX.raise_()
        self.checkBox_EjeY.raise_()
        self.checkBox_EjeZ.raise_()
        self.checkBox_AccVector.raise_()
        self.label_SensorNombre.raise_()
        self.label_NodoNombre.raise_()
        self.comboBox_nombreNodo.raise_()
        self.comboBox_nombreSensor.raise_()
        self.label_tituloDatosVisualizar.raise_()
        self.label_titulo1.raise_()
        self.checkBox_FourierVisualizar.raise_()
        self.label_tituloVisualizarGrafica.raise_()
        self.checkBox_VibracionesVisualizar.raise_()
        self.horizontalSlider_Duracion.raise_()
        self.label_DuracionDatos.raise_()
        self.pushButton_actualizarNodos.raise_()
        self.pushButton.raise_()
        self.pushButtonGraficFile.raise_()
        self.radioButtonTiempoContinuo.raise_()
        self.label_VerificaOpcAvanzadas.raise_()
        self.radioButtonDuracion.raise_()
        self.tabWidget_system.addTab(self.tab_pruebas, _fromUtf8(""))
        self.tab_FiltroFrec = QtGui.QWidget()
        self.tab_FiltroFrec.setObjectName(_fromUtf8("tab_FiltroFrec"))
        self.groupBox_FrecCorte = QtGui.QGroupBox(self.tab_FiltroFrec)
        self.groupBox_FrecCorte.setGeometry(QtCore.QRect(10, 60, 221, 51))
        font = QtGui.QFont()
        font.setKerning(True)
        self.groupBox_FrecCorte.setFont(font)
        self.groupBox_FrecCorte.setTitle(_fromUtf8(""))
        self.groupBox_FrecCorte.setObjectName(_fromUtf8("groupBox_FrecCorte"))
        self.label_FrecCorte = QtGui.QLabel(self.groupBox_FrecCorte)
        self.label_FrecCorte.setGeometry(QtCore.QRect(5, 10, 101, 16))
        self.label_FrecCorte.setObjectName(_fromUtf8("label_FrecCorte"))
        self.comboBox_FrecFiltroON = QtGui.QComboBox(self.groupBox_FrecCorte)

        self.comboBox_FrecFiltroON.setEnabled(True)
        self.comboBox_FrecFiltroON.setGeometry(QtCore.QRect(100, 10, 66, 25))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.comboBox_FrecFiltroON.setFont(font)
        self.comboBox_FrecFiltroON.setCursor(
                QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # self.comboBox_FrecFiltroON.setAccessibleDescription(_fromUtf8(""))
        self.comboBox_FrecFiltroON.setAutoFillBackground(False)
        self.comboBox_FrecFiltroON.setInputMethodHints(QtCore.Qt.ImhNone)
        self.comboBox_FrecFiltroON.setEditable(False)
        self.comboBox_FrecFiltroON.setObjectName(
                _fromUtf8("comboBox_FrecFiltroON"))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.comboBox_FrecFiltroON.addItem(_fromUtf8(""))
        self.groupBox_Filtro = QtGui.QGroupBox(self.tab_FiltroFrec)
        self.groupBox_Filtro.setGeometry(QtCore.QRect(10, 10, 221, 61))
        self.groupBox_Filtro.setObjectName(_fromUtf8("groupBox_Filtro"))
        self.label_FiltroPasaBaja = QtGui.QLabel(self.groupBox_Filtro)
        self.label_FiltroPasaBaja.setGeometry(QtCore.QRect(5, 30, 82, 16))
        self.label_FiltroPasaBaja.setObjectName(
                _fromUtf8("label_FiltroPasaBaja"))
        self.radioButton_filtroOn = QtGui.QRadioButton(self.groupBox_Filtro)
        self.radioButton_filtroOn.setGeometry(QtCore.QRect(80, 30, 43, 20))
        self.radioButton_filtroOn.setAcceptDrops(False)
        self.radioButton_filtroOn.setAutoFillBackground(False)
        self.radioButton_filtroOn.setChecked(True)
        self.radioButton_filtroOn.setObjectName(
                _fromUtf8("radioButton_filtroOn"))
        self.radioButton_filtroOff = QtGui.QRadioButton(self.groupBox_Filtro)
        self.radioButton_filtroOff.setGeometry(QtCore.QRect(120, 30, 45, 20))
        self.radioButton_filtroOff.setObjectName(
                _fromUtf8("radioButton_filtroOff"))
        self.groupBox_FrecMuestreo = QtGui.QGroupBox(self.tab_FiltroFrec)
        self.groupBox_FrecMuestreo.setGeometry(QtCore.QRect(200, 10, 211, 61))
        self.groupBox_FrecMuestreo.setObjectName(
                _fromUtf8("groupBox_FrecMuestreo"))

        self.comboBox_FrecMuestreoOFF = QtGui.QComboBox(
                self.groupBox_FrecMuestreo)
        self.comboBox_FrecMuestreoOFF.setEnabled(True)
        self.comboBox_FrecMuestreoOFF.setGeometry(QtCore.QRect(120, 20,
                                                               61, 25))
        self.comboBox_FrecMuestreoOFF.setFrame(True)
        self.comboBox_FrecMuestreoOFF.setObjectName(
                _fromUtf8("comboBox_FrecMuestreoOFF"))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoOFF.addItem(_fromUtf8(""))
        self.label_asteriscos = QtGui.QLabel(self.groupBox_FrecMuestreo)
        self.label_asteriscos.setGeometry(QtCore.QRect(190, 20, 16, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_asteriscos.setFont(font)
        self.label_asteriscos.setAlignment(QtCore.Qt.AlignCenter)
        self.label_asteriscos.setObjectName(_fromUtf8("label_asteriscos"))
        self.label_FrecMuestreo = QtGui.QLabel(self.groupBox_FrecMuestreo)
        self.label_FrecMuestreo.setGeometry(QtCore.QRect(10, 20, 101, 21))
        self.label_FrecMuestreo.setObjectName(_fromUtf8("label_FrecMuestreo"))
        self.comboBox_FrecMuestreoON = QtGui.QComboBox(
                self.groupBox_FrecMuestreo)
        self.comboBox_FrecMuestreoON.setEnabled(True)
        self.comboBox_FrecMuestreoON.setGeometry(QtCore.QRect(120, 20, 61, 25))
        self.comboBox_FrecMuestreoON.setStyleSheet(
                _fromUtf8("#comboBox_FrecMuestreoON{\n"
                                                    "    \n"
                            "    background-color: rgb(245, 245, 245);\n"
                            "}"))
        self.comboBox_FrecMuestreoON.setFrame(True)
        self.comboBox_FrecMuestreoON.setObjectName(
                _fromUtf8("comboBox_FrecMuestreoON"))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))

        self.label_asteriscos.raise_()
        self.label_FrecMuestreo.raise_()
        self.comboBox_FrecMuestreoOFF.raise_()
        self.comboBox_FrecMuestreoON.raise_()
        self.label_FiltroConFrecuencia = QtGui.QLabel(self.tab_FiltroFrec)
        self.label_FiltroConFrecuencia.setGeometry(QtCore.QRect(200, 70,
                                                                201, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label_FiltroConFrecuencia.setFont(font)
        self.label_FiltroConFrecuencia.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_FiltroConFrecuencia.setObjectName(
                _fromUtf8("label_FiltroConFrecuencia"))
        self.label_teoremaNyquist = QtGui.QLabel(self.tab_FiltroFrec)
        self.label_teoremaNyquist.setGeometry(QtCore.QRect(80, 130, 251, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_teoremaNyquist.setFont(font)
        self.label_teoremaNyquist.setObjectName(
                _fromUtf8("label_teoremaNyquist"))
        self.tabWidget_system.addTab(self.tab_FiltroFrec, _fromUtf8(""))
        self.tab_unidades = QtGui.QWidget()
        self.tab_unidades.setObjectName(_fromUtf8("tab_unidades"))
        self.groupBox_UnidadesTemperatura = QtGui.QGroupBox(self.tab_unidades)
        self.groupBox_UnidadesTemperatura.setGeometry(QtCore.QRect(220, 13,
                                                                   201, 58))
        self.groupBox_UnidadesTemperatura.setObjectName(
                _fromUtf8("groupBox_UnidadesTemperatura"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(
                self.groupBox_UnidadesTemperatura)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_UnitsTemperatura = QtGui.QLabel(
                self.groupBox_UnidadesTemperatura)
        self.label_UnitsTemperatura.setObjectName(
                _fromUtf8("label_UnitsTemperatura"))
        self.gridLayout_4.addWidget(self.label_UnitsTemperatura, 0, 0, 1, 1)
        self.radioButton_CUnitsTemperatura = QtGui.QRadioButton(
                self.groupBox_UnidadesTemperatura)
        self.radioButton_CUnitsTemperatura.setCheckable(True)
        self.radioButton_CUnitsTemperatura.setChecked(True)
        self.radioButton_CUnitsTemperatura.setObjectName(
                _fromUtf8("radioButton_CUnitsTemperatura"))
        self.buttonGroup_Temperatura = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_Temperatura.setObjectName(
                _fromUtf8("buttonGroup_Temperatura"))
        self.buttonGroup_Temperatura.addButton(
                self.radioButton_CUnitsTemperatura)
        self.gridLayout_4.addWidget(
                self.radioButton_CUnitsTemperatura, 0, 1, 1, 1)
        self.radioButton_FUnitsTemperatura = QtGui.QRadioButton(
                self.groupBox_UnidadesTemperatura)
        self.radioButton_FUnitsTemperatura.setEnabled(False)
        self.radioButton_FUnitsTemperatura.setObjectName(
                _fromUtf8("radioButton_FUnitsTemperatura"))
        self.buttonGroup_Temperatura.addButton(
                self.radioButton_FUnitsTemperatura)
        self.gridLayout_4.addWidget(
                self.radioButton_FUnitsTemperatura, 0, 2, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_4)
        self.groupBox_UnidadesAcelerometro = QtGui.QGroupBox(self.tab_unidades)
        self.groupBox_UnidadesAcelerometro.setGeometry(QtCore.QRect(15, 12,
                                                                    231, 101))
        self.groupBox_UnidadesAcelerometro.setObjectName(
                _fromUtf8("groupBox_UnidadesAcelerometro"))
        self.layoutWidget = QtGui.QWidget(self.groupBox_UnidadesAcelerometro)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 10, 201, 74))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_UnitsAcc = QtGui.QLabel(self.layoutWidget)
        self.label_UnitsAcc.setObjectName(_fromUtf8("label_UnitsAcc"))
        self.gridLayout_3.addWidget(self.label_UnitsAcc, 0, 0, 1, 1)
        self.radioButton_gUnitsACC = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_gUnitsACC.setChecked(True)
        self.radioButton_gUnitsACC.setObjectName(
                _fromUtf8("radioButton_gUnitsACC"))
        self.buttonGroup_UnitsACC = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_UnitsACC.setObjectName(
                _fromUtf8("buttonGroup_UnitsACC"))
        self.buttonGroup_UnitsACC.addButton(self.radioButton_gUnitsACC)
        self.gridLayout_3.addWidget(self.radioButton_gUnitsACC, 0, 1, 1, 2)
        self.radioButton_ms2UnitsACC = QtGui.QRadioButton(self.layoutWidget)
        self.radioButton_ms2UnitsACC.setObjectName(
                _fromUtf8("radioButton_ms2UnitsACC"))
        self.buttonGroup_UnitsACC.addButton(self.radioButton_ms2UnitsACC)
        self.gridLayout_3.addWidget(self.radioButton_ms2UnitsACC, 0, 3, 1, 2)
        self.label_sensibilidad = QtGui.QLabel(self.layoutWidget)
        self.label_sensibilidad.setObjectName(_fromUtf8("label_sensibilidad"))
        self.gridLayout_3.addWidget(self.label_sensibilidad, 1, 0, 1, 2)
        self.radioButton_sensibilidad2gACC = QtGui.QRadioButton(
                self.layoutWidget)
        self.radioButton_sensibilidad2gACC.setChecked(True)
        self.radioButton_sensibilidad2gACC.setObjectName(
                _fromUtf8("radioButton_sensibilidad2gACC"))
        self.buttonGroup_sensibilidad = QtGui.QButtonGroup(MainWindow)
        self.buttonGroup_sensibilidad.setObjectName(
                _fromUtf8("buttonGroup_sensibilidad"))
        self.buttonGroup_sensibilidad.addButton(
                self.radioButton_sensibilidad2gACC)
        self.gridLayout_3.addWidget(
                self.radioButton_sensibilidad2gACC, 1, 2, 1, 2)
        self.radioButton_sensibilidad8gACC = QtGui.QRadioButton(
                self.layoutWidget)
        self.radioButton_sensibilidad8gACC.setObjectName(
                _fromUtf8("radioButton_sensibilidad8gACC"))
        self.buttonGroup_sensibilidad.addButton(
                self.radioButton_sensibilidad8gACC)
        self.gridLayout_3.addWidget(self.radioButton_sensibilidad8gACC, 1, 4,
                                    1, 1)
        self.radioButton_sensibilidad4gACC = QtGui.QRadioButton(
                self.layoutWidget)
        self.radioButton_sensibilidad4gACC.setObjectName(
                _fromUtf8("radioButton_sensibilidad4gACC"))
        self.buttonGroup_sensibilidad.addButton(
                self.radioButton_sensibilidad4gACC)
        self.gridLayout_3.addWidget(self.radioButton_sensibilidad4gACC, 2, 2,
                                    1, 2)
        self.radioButton_sensibilidad16gACC = QtGui.QRadioButton(
                self.layoutWidget)
        self.radioButton_sensibilidad16gACC.setObjectName(
                _fromUtf8("radioButton_sensibilidad16gACC"))
        self.buttonGroup_sensibilidad.addButton(
                self.radioButton_sensibilidad16gACC)
        self.gridLayout_3.addWidget(
                self.radioButton_sensibilidad16gACC, 2, 4, 1, 1)
        self.groupBox_UnidadesGiroscopio = QtGui.QGroupBox(self.tab_unidades)
        self.groupBox_UnidadesGiroscopio.setGeometry(QtCore.QRect(20, 85,
                                                                  231, 101))
        self.groupBox_UnidadesGiroscopio.setObjectName(
                _fromUtf8("groupBox_UnidadesGiroscopio"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_UnidadesGiroscopio)
        self.layoutWidget1.setGeometry(QtCore.QRect(1, 10, 224, 74))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_UnitsGyro = QtGui.QLabel(self.layoutWidget1)
        self.label_UnitsGyro.setObjectName(_fromUtf8("label_UnitsGyro"))
        self.gridLayout_2.addWidget(self.label_UnitsGyro, 0, 0, 1, 1)
        self.label_sensibilidadGyro = QtGui.QLabel(self.layoutWidget1)
        self.label_sensibilidadGyro.setObjectName(
                _fromUtf8("label_sensibilidadGyro"))
        self.gridLayout_2.addWidget(self.label_sensibilidadGyro, 1, 0, 1, 2)
        self.radioButton_sensibilidad2gGyro = QtGui.QRadioButton(
                self.layoutWidget1)
        self.radioButton_sensibilidad2gGyro.setChecked(False)
        self.radioButton_sensibilidad2gGyro.setObjectName(
                _fromUtf8("radioButton_sensibilidad2gGyro"))
        self.gridLayout_2.addWidget(self.radioButton_sensibilidad2gGyro, 1, 2,
                                    1, 1)
        self.radioButton_sensibilidad8gGyro = QtGui.QRadioButton(
                self.layoutWidget1)
        self.radioButton_sensibilidad8gGyro.setChecked(True)
        self.radioButton_sensibilidad8gGyro.setObjectName(
                _fromUtf8("radioButton_sensibilidad8gGyro"))
        self.gridLayout_2.addWidget(self.radioButton_sensibilidad8gGyro, 1, 3,
                                    1, 1)
        self.radioButton_sensibilidad4gGyro = QtGui.QRadioButton(
                self.layoutWidget1)
        self.radioButton_sensibilidad4gGyro.setObjectName(
                _fromUtf8("radioButton_sensibilidad4gGyro"))
        self.gridLayout_2.addWidget(self.radioButton_sensibilidad4gGyro, 2, 2,
                                    1, 1)
        self.radioButton_sensibilidad16gGyro = QtGui.QRadioButton(
                self.layoutWidget1)
        self.radioButton_sensibilidad16gGyro.setObjectName(
                _fromUtf8("radioButton_sensibilidad16gGyro"))
        self.gridLayout_2.addWidget(self.radioButton_sensibilidad16gGyro, 2, 3,
                                    1, 1)
        self.checkBox_UnitsGyro = QtGui.QCheckBox(self.layoutWidget1)
        self.checkBox_UnitsGyro.setEnabled(False)
        self.checkBox_UnitsGyro.setCheckable(True)
        self.checkBox_UnitsGyro.setChecked(True)
        self.checkBox_UnitsGyro.setObjectName(_fromUtf8("checkBox_UnitsGyro"))
        self.gridLayout_2.addWidget(self.checkBox_UnitsGyro, 0, 1, 1, 2)
        self.label = QtGui.QLabel(self.tab_unidades)
        self.label.setGeometry(QtCore.QRect(80, 170, 241, 20))
        font = QtGui.QFont()
        font.setPointSize(7)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.tabWidget_system.addTab(self.tab_unidades, _fromUtf8(""))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.label_4 = QtGui.QLabel(self.tab)
        self.label_4.setGeometry(QtCore.QRect(20, 40, 120, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.doubleSpinBox_AccMinima = QtGui.QDoubleSpinBox(self.tab)
        self.doubleSpinBox_AccMinima.setEnabled(False)
        self.doubleSpinBox_AccMinima.setGeometry(QtCore.QRect(150, 35, 62, 27))
#        self.doubleSpinBox_AccMinima.setToolTip(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))
        self.comboBox_FrecMuestreoON.addItem(_fromUtf8(""))

        self.doubleSpinBox_AccMinima.setDecimals(2)
        self.doubleSpinBox_AccMinima.setMinimum(0.0)
        self.doubleSpinBox_AccMinima.setMaximum(10.0)
        self.doubleSpinBox_AccMinima.setSingleStep(0.01)
        self.doubleSpinBox_AccMinima.setObjectName(
                _fromUtf8("doubleSpinBox_AccMinima"))
        self.textBrowser = QtGui.QTextBrowser(self.tab)
        self.textBrowser.setEnabled(False)
        self.textBrowser.setGeometry(QtCore.QRect(30, 70, 360, 90))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser.setFont(font)
        self.textBrowser.setAcceptDrops(False)
        self.textBrowser.setFrameShape(QtGui.QFrame.StyledPanel)
        self.textBrowser.setFrameShadow(QtGui.QFrame.Sunken)
        self.textBrowser.setLineWidth(0)
        self.textBrowser.setObjectName(_fromUtf8("textBrowser"))
        self.layoutWidget2 = QtGui.QWidget(self.tab)
        self.layoutWidget2.setGeometry(QtCore.QRect(10, 00, 300, 51))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_2 = QtGui.QLabel(self.layoutWidget2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
#        self.label_3 = QtGui.QLabel(self.layoutWidget2)
#        self.label_3.setObjectName(_fromUtf8("label_3"))
#        self.verticalLayout.addWidget(self.label_3)
        self.tabWidget_system.addTab(self.tab, _fromUtf8(""))
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setGeometry(QtCore.QRect(110, 360-CORRECTION, 210, 20))
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.pushButton_Detener = QtGui.QPushButton(self.splitter)
        self.pushButton_Detener.setObjectName(_fromUtf8("pushButton_Detener"))
        self.pushButton_Detener.setEnabled(False)
        self.pushButton_Iniciar = QtGui.QPushButton(self.splitter)
        self.pushButton_Iniciar.setToolTip(_fromUtf8(""))
        self.pushButton_Iniciar.setShortcut(_fromUtf8(""))
        self.pushButton_Iniciar.setObjectName(_fromUtf8("pushButton_Iniciar"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        self.tabWidget_system.setCurrentIndex(0)

        # Evento Iniciar / Detener
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.pushButton_Detener.setEnabled(False))
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.pushButton_Iniciar.setEnabled(True))
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.pushButton.setEnabled(False))
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.radioButtonTiempoContinuo.setEnabled(True))
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.radioButtonDuracion.setEnabled(True))
        QtCore.QObject.connect(
                self.pushButton_Detener,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.pushButton_actualizarNodos.setEnabled(True))

        # Frecuencia de corte
        QtCore.QObject.connect(self.radioButton_filtroOn,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.groupBox_FrecCorte.show)
        QtCore.QObject.connect(self.radioButton_filtroOff,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.groupBox_FrecCorte.hide)
        QtCore.QObject.connect(self.radioButton_filtroOff,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.comboBox_FrecMuestreoOFF.show)
        QtCore.QObject.connect(self.radioButton_filtroOn,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.comboBox_FrecMuestreoOFF.hide)
        QtCore.QObject.connect(self.radioButton_filtroOn,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.comboBox_FrecMuestreoON.show)
        QtCore.QObject.connect(self.radioButton_filtroOff,
                               QtCore.SIGNAL(_fromUtf8("clicked()")),
                               self.comboBox_FrecMuestreoON.hide)

        # Duracion
        QtCore.QObject.connect(
                self.horizontalSlider_Duracion,
                QtCore.SIGNAL(_fromUtf8("sliderMoved(int)")),
                self.label_DuracionDatos.setNum)
        QtCore.QObject.connect(
                self.radioButtonTiempoContinuo,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.horizontalSlider_Duracion.hide)
        QtCore.QObject.connect(
                self.radioButtonTiempoContinuo,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.label_DuracionDatos.clear)
        QtCore.QObject.connect(
                self.radioButtonTiempoContinuo,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.label_VerificaOpcAvanzadas.show)
#        QtCore.QObject.connect(self.radioButtonTiempoContinuo, QtCore.SIGNAL(_fromUtf8("clicked()")), self.doubleSpinBox_AccMinima.show)
        QtCore.QObject.connect(
                self.radioButtonTiempoContinuo,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.doubleSpinBox_AccMinima.setEnabled(True))
        QtCore.QObject.connect(
                self.radioButtonDuracion,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.horizontalSlider_Duracion.show)
        QtCore.QObject.connect(
                self.radioButtonDuracion,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                self.label_VerificaOpcAvanzadas.hide)
        QtCore.QObject.connect(
                self.radioButtonDuracion,
                QtCore.SIGNAL(_fromUtf8("clicked()")),
                lambda: self.doubleSpinBox_AccMinima.setEnabled(False))
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow",
                                             "E-Bridge System", None))
        self.label_titulo1.setText(_translate("MainWindow",
                                              "Sistema Monitoreo E-bridge",
                                              None))
#        self.label_Titulo2.setText(_translate("MainWindow", "E-Bridge", None))
        self.checkBox_FourierVisualizar.setText(_translate("MainWindow",
                                                           "Fourier", None))
        self.label_tituloVisualizarGrafica.setText(
                _translate("MainWindow", "Visualizar grafica:", None))
        self.checkBox_VibracionesVisualizar.setText(
                _translate("MainWindow", "Vibraciones", None))
        self.label_DuracionDatos.setText(
                _translate("MainWindow", "1", None))
        #self.label_DuracionTexto.setText(_translate("MainWindow","Duracion (min):",None))
        self.label_tituloDatosVisualizar.setText(
                _translate("MainWindow", "Datos a Visualizar", None))
        self.pushButton_actualizarNodos.setText(
                _translate("MainWindow", "Actualizar", None))
        self.label_SensorNombre.setText(
                _translate("MainWindow", "Sensor:", None))
        self.label_NodoNombre.setText(
                _translate("MainWindow", "Nodo:", None))
        self.pushButton.setText(
                _translate("MainWindow", "ver Mediciones!", None))
        self.pushButtonGraficFile.setText(_translate("MainWindow",
                                                     "Graficar file", None))
        self.checkBox_EjeX.setText(_translate("MainWindow", "Eje X", None))
        self.checkBox_EjeY.setText(_translate("MainWindow", "Eje Y", None))
        self.checkBox_EjeZ.setText(_translate("MainWindow", "Eje Z", None))
        self.checkBox_AccVector.setText(
                _translate("MainWindow", "Vector Acc", None))
        self.radioButtonTiempoContinuo.setText(
                _translate("MainWindow", "Continuo", None))
        self.label_VerificaOpcAvanzadas.setText(
                _translate("MainWindow", "Verfique las opciones avanzadas",
                           None))
        self.radioButtonDuracion.setText(
                _translate("MainWindow", "Duración (minutos)", None))
        self.tabWidget_system.setTabText(
                self.tabWidget_system.indexOf(self.tab_pruebas),
                _translate("MainWindow", "Pruebas", None))
        self.label_FrecCorte.setText(_translate("MainWindow",
                                                "Frecuencia de Corte", None))
        self.comboBox_FrecFiltroON.setItemText(0,
                                               _translate("MainWindow",
                                                          "5 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(1,
                                               _translate("MainWindow",
                                                          "10 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(2,
                                               _translate("MainWindow",
                                                          "21 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(3,
                                               _translate("MainWindow",
                                                          "44 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(4,
                                               _translate("MainWindow",
                                                          "94 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(5,
                                               _translate("MainWindow",
                                                          "184 Hz", None))
        self.comboBox_FrecFiltroON.setItemText(6,
                                               _translate("MainWindow",
                                                          "260 Hz", None))
        self.groupBox_Filtro.setTitle(
                _translate("MainWindow", "Filtro Pasa Baja", None))
        self.label_FiltroPasaBaja.setText(
                _translate("MainWindow", "Filtro Pasa Baja:", None))
        self.radioButton_filtroOn.setText(
                _translate("MainWindow", "On", None))
        self.radioButton_filtroOff.setText(
                _translate("MainWindow", "Off", None))

        self.groupBox_FrecMuestreo.setTitle(
                _translate("MainWindow",
                           "Frecuencia Muestreo",
                           None))
        self.comboBox_FrecMuestreoOFF.setItemText(0,
                                                  _translate("MainWindow",
                                                             "32", None))
        self.comboBox_FrecMuestreoOFF.setItemText(1,
                                                  _translate("MainWindow",
                                                             "35", None))
        self.comboBox_FrecMuestreoOFF.setItemText(2,
                                                  _translate("MainWindow",
                                                             "40", None))
        self.comboBox_FrecMuestreoOFF.setItemText(3,
                                                  _translate("MainWindow",
                                                             "45", None))
        self.comboBox_FrecMuestreoOFF.setItemText(4,
                                                  _translate("MainWindow",
                                                             "50", None))
        self.comboBox_FrecMuestreoOFF.setItemText(5,
                                                  _translate("MainWindow",
                                                             "55", None))
        self.comboBox_FrecMuestreoOFF.setItemText(6,
                                                  _translate("MainWindow",
                                                             "62", None))
        self.comboBox_FrecMuestreoOFF.setItemText(7,
                                                  _translate("MainWindow",
                                                             "65", None))
        self.comboBox_FrecMuestreoOFF.setItemText(8,
                                                  _translate("MainWindow",
                                                             "71", None))
        self.comboBox_FrecMuestreoOFF.setItemText(9,
                                                  _translate("MainWindow",
                                                             "75", None))
        self.comboBox_FrecMuestreoOFF.setItemText(10,
                                                  _translate("MainWindow",
                                                             "85", None))
        self.comboBox_FrecMuestreoOFF.setItemText(11,
                                                  _translate("MainWindow",
                                                             "90", None))
        self.comboBox_FrecMuestreoOFF.setItemText(12,
                                                  _translate("MainWindow",
                                                             "95", None))
        self.comboBox_FrecMuestreoOFF.setItemText(13,
                                                  _translate("MainWindow",
                                                             "100", None))
        self.comboBox_FrecMuestreoOFF.setItemText(14,
                                                  _translate("MainWindow",
                                                             "110", None))
        self.comboBox_FrecMuestreoOFF.setItemText(15,
                                                  _translate("MainWindow",
                                                             "121", None))
        self.comboBox_FrecMuestreoOFF.setItemText(16,
                                                  _translate("MainWindow",
                                                             "131", None))
        self.comboBox_FrecMuestreoOFF.setItemText(17,
                                                  _translate("MainWindow",
                                                             "140", None))
        self.comboBox_FrecMuestreoOFF.setItemText(18,
                                                  _translate("MainWindow",
                                                             "150", None))
        self.comboBox_FrecMuestreoOFF.setItemText(19,
                                                  _translate("MainWindow",
                                                             "160", None))
        self.comboBox_FrecMuestreoOFF.setItemText(20,
                                                  _translate("MainWindow",
                                                             "170", None))
        self.comboBox_FrecMuestreoOFF.setItemText(21,
                                                  _translate("MainWindow",
                                                             "181", None))
        self.comboBox_FrecMuestreoOFF.setItemText(22,
                                                  _translate("MainWindow",
                                                             "190", None))
        self.comboBox_FrecMuestreoOFF.setItemText(23,
                                                  _translate("MainWindow",
                                                             "200", None))
        self.comboBox_FrecMuestreoOFF.setItemText(24,
                                                  _translate("MainWindow",
                                                             "250", None))
        self.comboBox_FrecMuestreoOFF.setItemText(25,
                                                  _translate("MainWindow",
                                                             "307", None))
        self.comboBox_FrecMuestreoOFF.setItemText(26,
                                                  _translate("MainWindow",
                                                             "400", None))
        self.comboBox_FrecMuestreoOFF.setItemText(27,
                                                  _translate("MainWindow",
                                                             "500", None))
        self.comboBox_FrecMuestreoOFF.setItemText(28,
                                                  _translate("MainWindow",
                                                             "615", None))
        self.comboBox_FrecMuestreoOFF.setItemText(29,
                                                  _translate("MainWindow",
                                                             "800", None))
        self.comboBox_FrecMuestreoOFF.setItemText(30,
                                                  _translate("MainWindow",
                                                             "888", None))
        self.comboBox_FrecMuestreoOFF.setItemText(31,
                                                  _translate("MainWindow",
                                                             "1000", None))
        self.label_asteriscos.setText(_translate("MainWindow", "**", None))

        self.label_FrecMuestreo.setText(
                _translate("MainWindow", "Frec. Muestreo (Hz)", None))
        self.comboBox_FrecMuestreoON.setItemText(0,
                                                 _translate("MainWindow",
                                                            "4", None))
        self.comboBox_FrecMuestreoON.setItemText(1,
                                                 _translate("MainWindow",
                                                            "6", None))
        self.comboBox_FrecMuestreoON.setItemText(2,
                                                 _translate("MainWindow",
                                                            "8", None))
        self.comboBox_FrecMuestreoON.setItemText(3,
                                                 _translate("MainWindow",
                                                            "10", None))
        self.comboBox_FrecMuestreoON.setItemText(4,
                                                 _translate("MainWindow",
                                                            "12", None))
        self.comboBox_FrecMuestreoON.setItemText(5,
                                                 _translate("MainWindow",
                                                            "14", None))
        self.comboBox_FrecMuestreoON.setItemText(6,
                                                 _translate("MainWindow",
                                                            "16", None))
        self.comboBox_FrecMuestreoON.setItemText(7,
                                                 _translate("MainWindow",
                                                            "18", None))
        self.comboBox_FrecMuestreoON.setItemText(8,
                                                 _translate("MainWindow",
                                                            "20", None))
        self.comboBox_FrecMuestreoON.setItemText(9,
                                                 _translate("MainWindow",
                                                            "22", None))
        self.comboBox_FrecMuestreoON.setItemText(10,
                                                 _translate("MainWindow",
                                                            "24", None))
        self.comboBox_FrecMuestreoON.setItemText(11,
                                                 _translate("MainWindow",
                                                            "26", None))
        self.comboBox_FrecMuestreoON.setItemText(12,
                                                 _translate("MainWindow",
                                                            "28", None))
        self.comboBox_FrecMuestreoON.setItemText(13,
                                                 _translate("MainWindow",
                                                            "30", None))
        self.comboBox_FrecMuestreoON.setItemText(14,
                                                 _translate("MainWindow",
                                                            "35", None))
        self.comboBox_FrecMuestreoON.setItemText(15,
                                                 _translate("MainWindow",
                                                            "40", None))
        self.comboBox_FrecMuestreoON.setItemText(16,
                                                 _translate("MainWindow",
                                                            "45", None))
        self.comboBox_FrecMuestreoON.setItemText(17,
                                                 _translate("MainWindow",
                                                            "50", None))
        self.comboBox_FrecMuestreoON.setItemText(18,
                                                 _translate("MainWindow",
                                                            "55", None))
        self.comboBox_FrecMuestreoON.setItemText(19,
                                                 _translate("MainWindow",
                                                            "62", None))
        self.comboBox_FrecMuestreoON.setItemText(20,
                                                 _translate("MainWindow",
                                                            "100", None))
        self.comboBox_FrecMuestreoON.setItemText(21,
                                                 _translate("MainWindow",
                                                            "125", None))
        self.comboBox_FrecMuestreoON.setItemText(22,
                                                 _translate("MainWindow",
                                                            "200", None))
        self.comboBox_FrecMuestreoON.setItemText(23,
                                                 _translate("MainWindow",
                                                            "250", None))
        self.comboBox_FrecMuestreoON.setItemText(24,
                                                 _translate("MainWindow",
                                                            "333", None))
        self.comboBox_FrecMuestreoON.setItemText(25,
                                                 _translate("MainWindow",
                                                            "500", None))
        self.comboBox_FrecMuestreoON.setItemText(26,
                                                 _translate("MainWindow",
                                                            "1000", None))

        mensjae = "** Frec.Bajas solo si El filtro pasa baja esta activado."
        self.label_FiltroConFrecuencia.setText( _translate("MainWindow",
                                                           mensjae, None))
        self.label_teoremaNyquist.setText(
                _translate("MainWindow",
                           "** Recuerde aplicar el teorema de Nyquist.", None))
        self.tabWidget_system.setTabText(
                self.tabWidget_system.indexOf(self.tab_FiltroFrec),
                _translate("MainWindow", "Filtro/Frec.", None))
        self.groupBox_UnidadesTemperatura.setTitle(
                _translate("MainWindow", "Temperatura", None))
        self.label_UnitsTemperatura.setText(
                _translate("MainWindow", "Unidades", None))
        self.radioButton_CUnitsTemperatura.setText(
                _translate("MainWindow", "C", None))
        self.radioButton_FUnitsTemperatura.setText(
                _translate("MainWindow", "F", None))
        self.groupBox_UnidadesAcelerometro.setTitle(
                _translate("MainWindow", "Acelerómetro", None))
        self.label_UnitsAcc.setText(
                _translate("MainWindow", "Unidades", None))
        self.radioButton_gUnitsACC.setText(
                _translate("MainWindow", "g", None))
        self.radioButton_ms2UnitsACC.setText(
                _translate("MainWindow", "m/s2", None))
        self.label_sensibilidad.setText(
                _translate("MainWindow", "Sensibilidad", None))
        self.radioButton_sensibilidad2gACC.setText(
                _translate("MainWindow", "2 g", None))
        self.radioButton_sensibilidad8gACC.setText(
                _translate("MainWindow", "8 g", None))
        self.radioButton_sensibilidad4gACC.setText(
                _translate("MainWindow", "4 g", None))
        self.radioButton_sensibilidad16gACC.setText(
                _translate("MainWindow", "16 g", None))
        self.groupBox_UnidadesGiroscopio.setTitle(
                _translate("MainWindow", "Giroscopio", None))
        self.label_UnitsGyro.setText(
                _translate("MainWindow", "Unidades", None))
        self.label_sensibilidadGyro.setText(
                _translate("MainWindow", "Sensib(grados) ", None))
        self.radioButton_sensibilidad2gGyro.setText(
                _translate("MainWindow", "250", None))
        self.radioButton_sensibilidad8gGyro.setText(
                _translate("MainWindow", "1000", None))
        self.radioButton_sensibilidad4gGyro.setText(
                _translate("MainWindow", "500", None))
        self.radioButton_sensibilidad16gGyro.setText(
                _translate("MainWindow", "2000", None))
        self.checkBox_UnitsGyro.setText(
                _translate("MainWindow", "Grados/seg", None))
        msj2 = "Sensibilidad nuevaimplica que se calibrará nuevamente."
        self.label.setText(_translate("MainWindow", msj2, None))
        self.tabWidget_system.setTabText(
                self.tabWidget_system.indexOf(self.tab_unidades),
                _translate("MainWindow", "Unidades", None))
        self.label_4.setText(
                _translate("MainWindow", "Acceleración Mínima (g)", None))
        self.textBrowser.setHtml(
                _translate("MainWindow",
                           "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'PibotoLt\'; font-size:8pt; font-weight:600; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">La aceleración minima le indica al sistema a partir de que valor empieza a almacenar datos. Asi se reduce los datos no importantes para el usuario, ahorrando almacenamiento y calculando mejores espectros de Fourier.</p></body></html>", None))
        msj3 = "Estas opciones se habilitan al activar \"Duración continua\""
        self.label_2.setText(_translate("MainWindow", msj3, None))
        self.tabWidget_system.setTabText(
                self.tabWidget_system.indexOf(self.tab),
                _translate("MainWindow", "OpcAvanzada", None))
        self.pushButton_Detener.setText(
                _translate("MainWindow", "Detener", None))
        self.pushButton_Iniciar.setText(
                _translate("MainWindow", "Iniciar", None))
