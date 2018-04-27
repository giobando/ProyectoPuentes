#!/usr/bin/python
import time

contador = 0

while(True):
  
  print "Time: %s" % time.ctime(), ", num: %d" % contador
##  print "Start : %s" % time.ctime()
  #time.sleep( 5 ) # numeros de segundos por espera es de 5seg
  time.sleep(1/22) # 22 tomas por segund
##  print "End : %s" % time.ctime()

  if contador == 22:
    break
  else:
    contador+=1

print "fin"
