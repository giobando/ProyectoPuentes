#!/usr/bin/python

import MPU6050
import math
import time
import numpy

#TargetSampleNumber= 1024
#TargetRate =  33    # frequency =  8000 / ( integr value + 1)  minimum frequency=32,25

InputSampleRate=raw_input("Sample Rate(32.25 ... 2000) ?")  
InputSampleNumber=raw_input("Number of sample to take ?")    

TargetSampleNumber= int(InputSampleNumber)  # Cantidad muestras para calcular fourier
TargetRate= float(InputSampleRate)          # Frecuencia Muestreo


#============================================================================================
#                                1. INICIALIZAR MPU6050
#============================================================================================
mpu6050 = MPU6050.MPU6050()

mpu6050.setup()
mpu6050.setGResolution(2)
mpu6050.setSampleRate(TargetRate)
mpu6050.enableFifo(False)
time.sleep(0.01)

print "Capturing {0} samples at {1} samples/sec".format(TargetSampleNumber, mpu6050.SampleRate)
raw_input("Press enter to start")

mpu6050.resetFifo()
mpu6050.enableFifo(True)
time.sleep(0.01)

Values = []       # Guarda mediciones
Total = 0         

#============================================================================================
#               2. TOMA MEDICIONES hasta llegar a tener "TargetSampleNumber"
#============================================================================================
while True:
 if mpu6050.fifoCount == 0:
     Status= mpu6050.readStatus()

     # print "Status",Status
     if (Status & 0x10) == 0x10 :
        print "Overrun Error! Quitting.\n"
        quit()

     if (Status & 0x01) == 0x01:
        Values.extend(mpu6050.readDataFromFifo())
 
 else:
        Values.extend(mpu6050.readDataFromFifo())

 #read Total number of data taken
 Total = len(Values)/14       # se divide entre 14 porque eso parece que se reciben de datospor cada muestra con fourier.
 # print Total
 if Total >= TargetSampleNumber :
   break;

 #now that we have the data let's write the files

#============================================================================================
#                      3. CALCULAR FOURIER apartir del txt 
#============================================================================================
if Total > 0:
  Status = mpu6050.readStatus()
  # print "Status",Status
  if (Status & 0x10) == 0x10 :
    print "Overrun Error! Quitting.\n"
    quit()
  print "Saving RawData.txt  file."
  
  FO = open("RawData.txt","w")                   # 1. Guardamos las aceleraciones en TXT
  FO.write("GT\tGx\tGy\tGz\tTemperature\tGyrox\tGyroy\tGyroz\n")
  fftdata = []  # lista para guardar vectorACC que sera para fourier
  for loop in range (TargetSampleNumber):        # 2. Se realiza grupos de datos para calcular fourier
    SimpleSample = Values[loop*14 : loop*14+14]  # 3. Se obtiene el primer grupo de datos del buffer
    I = mpu6050.convertData(SimpleSample)        # convierte list de raw a m/s2 y grados/s
    CurrentForce = math.sqrt( (I.Gx * I.Gx) + (I.Gy * I.Gy) +(I.Gz * I.Gz)) 
    fftdata.append(CurrentForce)                 # 4. agrega datos a la lista para calcular fourier
    FO.write("{0:6.3f}\t{1:6.3f}\t{2:6.3f}\t{3:6.3f}\t".format(CurrentForce, I.Gx , I.Gy, I.Gz))       # 5. Guardar en TXT
    FO.write("{0:5.1f}\t{1:6.3f}\t{2:6.3f}\t{3:6.3f}\n".format(I.Temperature,I.Gyrox,I.Gyroy,I.Gyroz))
  FO.close()

  print "Calculate FFT"

  fourier = numpy.fft.fft(fftdata)  # 6. se calcula fourier del grupo anterior

  print "Save FFTData.txt file"
  FO = open("FFTData.txt","w")      
  fftData = numpy.abs(fourier[0:len(fourier)/2+1])/TargetSampleNumber # 2. se aplica valor abs para obtener magnitud
  frequency = [] # lista de frecuencia
  FO.write( "Frequency\tFFT\n")
  Peak=0
  PeakIndex=0;
  for loop in range(TargetSampleNumber/2 +1):
    frequency.append( loop * TargetRate/ TargetSampleNumber) 
    FO.write("{0}\t{1}\n".format(frequency[loop],fftData[loop])) # 3. guardamos la frecuencia calculada con el fourier
    if loop>0:
       if fftData[loop] > Peak :      # 4. obtenemos el pico maximo 
         Peak=fftData[loop]
         PeakIndex=loop

  print "Peak at {0}Hz = {1}".format(frequency[PeakIndex],Peak)
   

print "Done!"
