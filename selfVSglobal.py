class probando:
  num1 = 1
  num2 = 2

  def __init__(self,num1, num2):
    self.num1 = num1
    self.num2 = num2
    
  def modificar():
    num1 = num1 + 1

  def printer():
    num1 = 56
    print("num1,  num2",self.num1, self.num2)


##x = probando(2,2)
##


en resumen
usar self cuando los valores son independientes con los valores de otras instancias
usar global si todas las clases comparten el mismo valor.
