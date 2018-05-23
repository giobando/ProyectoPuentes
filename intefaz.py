import time
from datetime import datetime
from Tkinter import *
import tkMessageBox
import sys
import Tkinter
import threading



screen = Tk()
screen.title("Red de sensores e-Bridge I.T.C.R.")
##screen.geometry('500x250')

#centra la ventana al centro de la pantalla
width = 500
height = 250 
posX = screen.winfo_screenwidth()-width
posY = screen.winfo_screenheight()-height
screen.geometry("%dx%d%+d%+d" % (width,height,posX/2,posY/2))

##screen.geometry('500x250')
# evita modificar el tamano
screen.resizable(0,0)

def dataBridge( ):
      def run():
          print "corriendo"

      
def helloCallBack():
      dataBridge()
      tkMessageBox.showinfo( "ON", "Sistema iniciado")
      
def helloCallBack1():
      tkMessageBox.showinfo( "OFF", "Sistema apagado")

                   
#R = Text(top, height=20, width=55)
T = Label(screen, text="Proyecto e-Bridge-TEC CR 2017\n\nOprima el boton de Activar para encender el sistema\nde lo contrario oprima Apagar\n")

#paa acomodar mejor las posicion de los elementos>
##T.grid(row=4,column=4)

T.pack()


# http://pharalax.com/blog/python-desarrollo-de-interfaces-graficas-con-tkinter-labelsbuttonsentrys/
B = Tkinter.Button(screen, text ="Activar", command = helloCallBack,background="red")
C = Tkinter.Button(screen, text ="Apagar", command = helloCallBack1,background="black",fg="white")
B.pack()
B.place(bordermode=OUTSIDE, height=100, width=50,x=150,y=100)
C.pack()
C.place(bordermode=OUTSIDE, height=100, width=50,x=300,y=100)



#finaliza la ventana
screen.mainloop()
