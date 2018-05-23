# -*- coding: utf-8 -*-
# esta funcion puede usarse para modificar el archivo de configuraci[on de sensores

 
import Tkinter
from Tkinter import *
import codecs
import os
 
v0 = Tkinter.Tk()
v0.config(bg="black")
v0.resizable(0,0)
 
def doit(f): v0.after(100, f)
def imprimir(textcontrol): print textcontrol.get('1.0', END+'-1c')
 
def escribir_en_archivo(enlace):
    f = codecs.open(enlace,"w","utf-8")
    texto = t1.get('1.0', END+'-1c')
    f.write(texto)
    f.close()
 
def abrir_archivo(enlace):
    if os.path.exists(enlace):
        f = open(enlace,"r")
        h= f.read()
        t1.insert(END,h)
        f.close()
 
t1=Text(v0)
t1.config(bg="black",fg="white")
t1.pack()
 
b1 = Button(v0,text="<< SAVE >>",command=lambda: doit(escribir_en_archivo('C:\hola.txt')))
b1.config(bg="black",fg="white")
b1.pack()
 
abrir_archivo('C:\hola.txt')
v0.mainloop()
