import os


try:
  os.mkdir("../LibrosA")

except OSError:
  print("Carpeta ya existe")
